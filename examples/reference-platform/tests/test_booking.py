"""Domain, authorization, idempotency and race-condition regression checks."""
from __future__ import annotations

import importlib.util
import sqlite3
import tempfile
import threading
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "booking.py"
spec = importlib.util.spec_from_file_location("booking_reference", SOURCE)
booking = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = booking
spec.loader.exec_module(booking)


class BookingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.db_path = Path(self.temp.name) / "pilot.db"
        booking.init(self.db_path)
        self.db = booking.connect(self.db_path)
        self.alice = booking.Actor("alice")
        self.bob = booking.Actor("bob")

    def tearDown(self):
        self.db.close()
        self.temp.cleanup()

    def test_reserve_and_same_request_replay(self):
        one = booking.reserve(self.db, self.alice, "slot-a", 1200, "req-1")
        again = booking.reserve(self.db, self.alice, "slot-a", 1200, "req-1")
        self.assertEqual(one, again)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM booking").fetchone()[0], 1)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM outbox").fetchone()[0], 1)

    def test_request_key_payload_collision_rejected(self):
        booking.reserve(self.db, self.alice, "slot-a", 1200, "req-1")
        with self.assertRaises(booking.Conflict):
            booking.reserve(self.db, self.alice, "slot-b", 1200, "req-1")
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM booking").fetchone()[0], 1)

    def test_cannot_double_book_slot(self):
        booking.reserve(self.db, self.alice, "slot-a", 1200, "req-a")
        with self.assertRaises(booking.Conflict):
            booking.reserve(self.db, self.bob, "slot-a", 1200, "req-b")

    def test_concurrent_clients_produce_single_booking(self):
        barrier = threading.Barrier(6)
        answers = []
        guard = threading.Lock()

        def worker(i):
            db = booking.connect(self.db_path)
            try:
                barrier.wait(timeout=5)
                try:
                    booking.reserve(db, booking.Actor(f"player-{i}"), "slot-race", 1200, f"r-{i}")
                    result = "ok"
                except booking.Conflict:
                    result = "conflict"
                with guard:
                    answers.append(result)
            finally:
                db.close()

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(6)]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=6)
        self.assertTrue(all(not t.is_alive() for t in threads))
        self.assertEqual(answers.count("ok"), 1)
        self.assertEqual(answers.count("conflict"), 5)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM booking WHERE slot_id='slot-race'").fetchone()[0], 1)

    def test_wrong_owner_cannot_pay_or_view(self):
        reservation = booking.reserve(self.db, self.alice, "slot-a", 1200, "r-a")
        self.assertEqual(booking.list_my_bookings(self.db, self.bob), [])
        with self.assertRaises(booking.Forbidden):
            booking.finalize(self.db, self.bob, reservation, "payment-1", 1200, verified=True)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM receipt").fetchone()[0], 0)

    def test_provider_validation_and_amount_required(self):
        reservation = booking.reserve(self.db, self.alice, "slot-a", 1200, "r-a")
        with self.assertRaises(booking.Forbidden):
            booking.finalize(self.db, self.alice, reservation, "payment-1", 1200, verified=False)
        with self.assertRaises(booking.Conflict):
            booking.finalize(self.db, self.alice, reservation, "payment-1", 999, verified=True)
        self.assertEqual(self.db.execute("SELECT state FROM booking WHERE id=?", (reservation,)).fetchone()[0], "reserved")

    def test_paid_replay_exact_once(self):
        reservation = booking.reserve(self.db, self.alice, "slot-a", 1200, "r-a")
        self.assertTrue(booking.finalize(self.db, self.alice, reservation, "payment-1", 1200, verified=True))
        self.assertFalse(booking.finalize(self.db, self.alice, reservation, "payment-1", 1200, verified=True))
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM receipt").fetchone()[0], 1)
        self.assertEqual(self.db.execute("SELECT COUNT(*) FROM outbox").fetchone()[0], 2)

    def test_reusing_provider_reference_for_other_booking_denied(self):
        first = booking.reserve(self.db, self.alice, "slot-a", 1200, "a")
        second = booking.reserve(self.db, self.alice, "slot-b", 1200, "b")
        booking.finalize(self.db, self.alice, first, "pay-ref", 1200, verified=True)
        with self.assertRaises(booking.Conflict):
            booking.finalize(self.db, self.alice, second, "pay-ref", 1200, verified=True)

    def test_invalid_role_and_amount(self):
        with self.assertRaises(booking.Forbidden):
            booking.reserve(self.db, booking.Actor("owner", "manager"), "slot-x", 1200, "r")
        with self.assertRaises(ValueError):
            booking.reserve(self.db, self.alice, "slot-x", True, "r")


if __name__ == "__main__":
    unittest.main()
