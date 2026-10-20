"""Isolated synthetic checksum-verified file restore. Not a database DR validation."""
from __future__ import annotations
import hashlib
from pathlib import Path
class IntegrityError(Exception):pass

def snapshot(source:Path)->dict[str,str]:
 if not source.is_dir() or source.is_symlink():raise ValueError("Invalid/linked source")
 result={}
 for path in sorted(source.rglob("*")):
  if path.is_symlink():raise ValueError("Linked content not supported")
  if not path.is_file():continue
  rel=path.relative_to(source).as_posix()
  result[rel]=hashlib.sha256(path.read_bytes()).hexdigest()
 if not result:raise ValueError("Empty snapshot")
 return result

def restore(source:Path,target:Path,manifest:dict[str,str])->dict:
 """Never overwrite or delete existing files; leave staging for diagnosis on errors."""
 if not isinstance(manifest,dict) or not manifest:raise ValueError("Empty manifest")
 if target.exists() or target.is_symlink():raise FileExistsError("Restore target must not exist")
 if source.is_symlink():raise ValueError("Source symlink")
 try:
  expected=snapshot(source)
 except ValueError as ex:
  raise IntegrityError("Missing or invalid source files") from ex
 if expected!=manifest:raise IntegrityError("Corrupted or missing source files")
 # Only synthetic, freshly-created directories should reach this function; secure
 # production backup/restoration requires platform-specific handling and approvals.
 target.mkdir(parents=True)
 try:
  for name in manifest:
   parts=Path(name)
   if parts.is_absolute() or ".." in parts.parts:raise ValueError("Path traversal")
   incoming=source/parts
   destination=target/parts
   destination.parent.mkdir(parents=True,exist_ok=True)
   with destination.open("xb") as f:f.write(incoming.read_bytes())
  if snapshot(target)!=manifest:raise IntegrityError("Restored data mismatch")
  return {"result":"RESTORED_SYNTHETIC_FILES","count":len(manifest),
          "warning":"Not a database restore, production RPO/RTO, key recovery or application integrity proof"}
 except Exception:
  # Intentional: no automatic removal of evidence.
  raise
