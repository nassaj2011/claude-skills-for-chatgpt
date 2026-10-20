#!/usr/bin/env python3
"""Read-only heuristic security check of third-party Agent Skills.

Not a sandbox, malware detector, or certification. Manual review is required.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path

# Match individual lines. Expand with tests when discovering new patterns.
PATTERNS = [
    ("remote-shell-pipe", "HIGH", re.compile(r"(?:curl|wget|\birm\b|Invoke-WebRequest).{0,180}\|\s*(?:bash|sh|zsh|iex|Invoke-Expression)\b", re.I)),
    ("unsafe-eval", "HIGH", re.compile(r"\b(?:Invoke-Expression|\biex\s*\(|eval\s*\(\s*base64\.)", re.I)),
    ("destructive-command", "HIGH", re.compile(r"\b(?:rm\s+-[a-zA-Z]*r[a-zA-Z]*f|git\s+clean\s+-[a-zA-Z]*f[a-zA-Z]*d|Remove-Item\s+[^\n]*-Recurse\s+-Force|format\s+[A-Z]:)\b", re.I)),
    ("credential-exfil", "HIGH", re.compile(r"(?:curl|wget|Invoke-WebRequest|requests\.post|fetch\().{0,180}(?:id_rsa|auth\.json|AWS_SECRET_ACCESS_KEY|GITHUB_TOKEN)", re.I)),
    ("instruction-hijack", "REVIEW", re.compile(r"(?:ignore (?:all )?(?:prior|previous|system) instructions|disable (?:all )?(?:security|safety) checks|reveal your (?:system prompt|secrets))", re.I)),
    ("credential-access", "REVIEW", re.compile(r"(?:\.ssh[/\\]id_rsa|\.aws[/\\]credentials|[/\\]auth\.json|\b(?:GITHUB_TOKEN|AWS_SECRET_ACCESS_KEY)\b)", re.I)),
    ("broad-tool-permission", "REVIEW", re.compile(r"allowed-tools:\s*.*(?:Bash\(\*\)|shell\(\*\)|\*\s*$)", re.I)),
    ("remote-code-eval", "HIGH", re.compile(r"\bexec\s*\(\s*(?:requests\.get|urllib\.request|urlopen)", re.I)),
    ("credential-upload", "HIGH", re.compile(r"(?:curl|wget|Invoke-WebRequest|requests\.post|fetch\().{0,180}(?:\.ssh|\.aws|\.env\b|secrets?[./\\])", re.I)),
    ("network-post", "REVIEW", re.compile(r"(?:curl\s+.{0,140}(?:-X\s+POST|--data(?:-binary)?)|requests\.post\s*\()", re.I)),
    ("forced-policy-disable", "HIGH", re.compile(r"(?:--dangerously-bypass-approvals-and-sandbox|disable\s+(?:audit|monitoring|logging)\s+(?:permanently|without notice)|exfiltrat(?:e|ion)\s+secrets)", re.I)),
]
TEXT_SUFFIXES = {".md", ".txt", ".py", ".ps1", ".sh", ".js", ".ts", ".mjs", ".json", ".yaml", ".yml", ".toml", ".bat", ".cmd"}
EXECUTABLE_SUFFIXES = {".exe", ".dll", ".so", ".dylib", ".jar", ".bin"}
LIMIT_BYTES = 1_000_000


def scan(root: Path) -> dict:
    root = root.expanduser().absolute()
    result: dict = {"root": str(root), "files_scanned": 0, "sha256": {}, "findings": []}
    findings: list[dict] = result["findings"]

    def flag(severity: str, rule: str, rel: str, line: int = 0, detail: str = "") -> None:
        findings.append({"severity": severity, "rule": rule, "path": rel.replace("\\", "/"), "line": line, "detail": detail})

    if not root.exists() or not root.is_dir():
        flag("HIGH", "invalid-root", ".", detail="No readable skill folder")
        return result
    if root.is_symlink() or bool(getattr(root, "is_junction", lambda: False)()):
        flag("HIGH", "linked-root", ".", detail="Root is linked; explicit trust review required")
        return result

    folders = [root] if (root / "SKILL.md").exists() else sorted(p for p in root.iterdir() if p.is_dir() or p.is_symlink())
    if not folders:
        flag("HIGH", "empty-catalog", ".", detail="No skills found")
        return result

    for folder in folders:
        relative_folder = folder.relative_to(root) if folder != root else Path(".")
        if folder.is_symlink() or bool(getattr(folder, "is_junction", lambda: False)()):
            flag("HIGH", "linked-skill", str(relative_folder), detail="Linked skill folder")
            continue
        if not (folder / "SKILL.md").is_file():
            flag("HIGH", "missing-manifest", str(relative_folder), detail="Missing SKILL.md")
        for walkroot, directories, files in os.walk(folder, followlinks=False):
            walking = Path(walkroot)
            for dirname in directories[:]:
                child = walking / dirname
                if child.is_symlink() or bool(getattr(child, "is_junction", lambda: False)()):
                    flag("HIGH", "linked-directory", str(child.relative_to(root)), detail="Linked directory not followed")
                    directories.remove(dirname)
            for filename in files:
                p = walking / filename
                rel = str(p.relative_to(root))
                if p.is_symlink():
                    flag("HIGH", "linked-file", rel, detail="Linked file not followed")
                    continue
                if not p.is_file():
                    flag("REVIEW", "non-regular-file", rel)
                    continue
                try:
                    size = p.stat().st_size
                    if size > LIMIT_BYTES:
                        flag("REVIEW", "large-file", rel, detail=f"{size} bytes; contents not inspected")
                        continue
                    data = p.read_bytes()
                except OSError as exc:
                    flag("HIGH", "unreadable-file", rel, detail=type(exc).__name__)
                    continue
                result["files_scanned"] += 1
                result["sha256"][rel.replace("\\", "/")] = hashlib.sha256(data).hexdigest()
                if p.suffix.lower() in EXECUTABLE_SUFFIXES:
                    flag("REVIEW", "binary-executable", rel, detail="Review origin and necessity")
                if p.suffix.lower() not in TEXT_SUFFIXES:
                    flag("REVIEW", "unparsed-format", rel, detail="File type not inspected")
                    continue
                try:
                    decoded = data.decode("utf-8-sig")
                except UnicodeDecodeError:
                    flag("REVIEW", "non-utf8", rel, detail="Cannot inspect as UTF-8")
                    continue
                for num, line in enumerate(decoded.splitlines(), 1):
                    for rule, severity, pattern in PATTERNS:
                        if pattern.search(line):
                            flag(severity, rule, rel, num, "Heuristic match; inspect context for examples or negation")

    result["findings"] = sorted(findings, key=lambda f: (f["path"], f["line"], f["rule"]))
    result["decision"] = "BLOCK" if any(f["severity"] == "HIGH" for f in findings) else (
        "REVIEW" if findings else "CLEAN_HEURISTIC_SCAN"
    )
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1] / "skills")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--fail-on", choices=["high", "review", "none"], default="review")
    args = parser.parse_args()
    result = scan(args.root)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"{result['decision']}: {result['files_scanned']} file(s), {len(result['findings'])} finding(s)")
        for f in result["findings"]:
            print(f"{f['severity']} {f['path']}:{f['line']} [{f['rule']}] {f['detail']}")
    if args.fail_on == "none":
        return 0
    return int(any(f["severity"] == "HIGH" or (args.fail_on == "review" and f["severity"] == "REVIEW") for f in result["findings"]))


if __name__ == "__main__":
    raise SystemExit(main())
