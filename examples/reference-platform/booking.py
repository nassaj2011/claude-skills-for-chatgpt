"""Illustrative booking transaction slice; not production authentication/payment.

SQLite concurrency, ownership checks, payment replay and durable event state.
No external network, credentials, background scheduler or destructive operations.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path


class Conflict(Exception):
    pass


class Forbidden(Exception):
    pass


@dataclass(frozen=True)
class Actor:
    actor_id: str
    role: str = "player"


def connect(path: Path) -> sqlite3.Connection:
    db = sqlite3.connect(str(path), isolation_level=None, timeout=5)
    db.execute("PRAGMA busy_timeout = 5000")
    db.execute("PRAGMA foreign_keys = ON")
    db.execute("PRAGMA journal_mode = WAL")
    return db


def init(path: Path) -> None:
    db = connect(path)
    try:
        db.executescript("""
            CREATE TABLE IF NOT EXISTS booking (
                id INTEGER PRIMARY KEY,
                owner_id TEXT NOT NULL,
                slot_id TEXT NOT NULL UNIQUE,
                state TEXT NOT NULL CHECK(state IN ('reserved', 'paid')),
                amount_minor INTEGER NOT NULL CHECK(amount_minor > 0)
            );
            CREATE TABLE IF NOT EXISTS booking_request (
                actor_id TEXT NOT NULL,
                request_key TEXT NOT NULL,
                booking_id INTEGER NOT NULL REFERENCES booking(id),
                PRIMARY KEY(actor_id, request_key)
            );
            CREATE TABLE IF NOT EXISTS receipt (
                provider_ref TEXT PRIMARY KEY,
                booking_id INTEGER NOT NULL UNIQUE REFERENCES booking(id),
                amount_minor INTEGER NOT NULL CHECK(amount_minor > 0)
            );
            CREATE TABLE IF NOT EXISTS outbox (
                id INTEGER PRIMARY KEY,
                event_type TEXT NOT NULL,
                subject_id INTEGER NOT NULL,
                UNIQUE(event_type, subject_id)
            );
        """)
    finally:
        db.close()


def reserve(db: sqlite3.Connection, actor: Actor, slot_id: str,
            amount_minor: int, request_key: str) -> int:
    if actor.role != "player" or not actor.actor_id or not slot_id or not request_key:
        raise Forbidden("Invalid actor, slot or idempotency key")
    if not isinstance(amount_minor, int) or isinstance(amount_minor, bool) or amount_minor <= 0:
        raise ValueError("Price must be a positive integer in minor units")
    db.execute("BEGIN IMMEDIATE")
    try:
        prior = db.execute(
            "SELECT b.id,b.slot_id,b.amount_minor FROM booking_request r "
            "JOIN booking b ON b.id=r.booking_id WHERE r.actor_id=? AND r.request_key=?",
            (actor.actor_id, request_key),
        ).fetchone()
        if prior:
            if (prior[1], prior[2]) != (slot_id, amount_minor):
                raise Conflict("Idempotency key reused with different payload")
            db.execute("COMMIT")
            return prior[0]
        cur = db.execute(
            "INSERT INTO booking(owner_id,slot_id,state,amount_minor) VALUES (?,?,'reserved',?)",
            (actor.actor_id, slot_id, amount_minor),
        )
        booking_id = cur.lastrowid
        db.execute("INSERT INTO booking_request VALUES (?,?,?)",
                   (actor.actor_id, request_key, booking_id))
        db.execute("INSERT INTO outbox(event_type,subject_id) VALUES (?,?)",
                   ("booking.reserved", booking_id))
        db.execute("COMMIT")
        return booking_id
    except sqlite3.IntegrityError as exc:
        db.execute("ROLLBACK")
        raise Conflict("Slot already reserved") from exc
    except Exception:
        db.execute("ROLLBACK")
        raise


def finalize(db: sqlite3.Connection, actor: Actor, booking_id: int,
             provider_ref: str, paid_minor: int, *, verified: bool) -> bool:
    """Caller must pass verified=True only after independent provider validation.

    Returns True for first successful confirmation, False for exact replay.
    """
    if not verified or not provider_ref:
        raise Forbidden("Provider receipt has not been verified")
    db.execute("BEGIN IMMEDIATE")
    try:
        booking = db.execute(
            "SELECT owner_id,state,amount_minor FROM booking WHERE id=?", (booking_id,)
        ).fetchone()
        if booking is None or booking[0] != actor.actor_id:
            raise Forbidden("No authorized booking")
        if (not isinstance(paid_minor, int) or isinstance(paid_minor, bool)
                or paid_minor != booking[2]):
            raise Conflict("Amount mismatch")
        receipt = db.execute(
            "SELECT booking_id,amount_minor FROM receipt WHERE provider_ref=?", (provider_ref,)
        ).fetchone()
        if receipt is not None:
            if receipt != (booking_id, paid_minor):
                raise Conflict("Receipt already bound to different purchase")
            db.execute("COMMIT")
            return False
        if booking[1] != "reserved":
            raise Conflict("Booking already paid with another reference")
        db.execute(
            "INSERT INTO receipt(provider_ref,booking_id,amount_minor) VALUES(?,?,?)",
            (provider_ref, booking_id, paid_minor))
        db.execute("UPDATE booking SET state='paid' WHERE id=?", (booking_id,))
        db.execute("INSERT INTO outbox(event_type,subject_id) VALUES (?,?)",
                   ("booking.paid", booking_id))
        db.execute("COMMIT")
        return True
    except sqlite3.IntegrityError as exc:
        db.execute("ROLLBACK")
        raise Conflict("Receipt already associated with another booking") from exc
    except Exception:
        db.execute("ROLLBACK")
        raise


def list_my_bookings(db: sqlite3.Connection, actor: Actor) -> list[tuple]:
    """Never query by caller-controlled owner IDs."""
    return db.execute("SELECT id,slot_id,state FROM booking WHERE owner_id=? ORDER BY id",
                      (actor.actor_id,)).fetchall()
