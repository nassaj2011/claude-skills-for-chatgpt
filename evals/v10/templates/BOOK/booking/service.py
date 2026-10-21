from .data import MemoryDB

class BookingService:
    def __init__(self, db):
        self.db = db

    def reserve(self, tenant, slot, owner, request_key, amount_minor):
        bid = tenant + ":" + slot
        if (tenant, slot) in self.db.slot_index:
            raise ValueError("slot already taken")
        record = {"id": bid, "tenant": tenant, "slot": slot,
                  "owner": owner, "request_key": request_key,
                  "amount_minor": amount_minor, "state": "PENDING", "receipt": None}
        self.db.bookings[bid] = record
        self.db.slot_index[(tenant, slot)] = bid
        return dict(record)

    def confirm(self, tenant, booking_id, receipt, amount_minor, verified):
        booking = self.db.bookings[booking_id]
        booking["state"] = "PAID"
        booking["receipt"] = receipt
        self.db.receipts[receipt] = booking_id
        event_id = str(len(self.db.outbox) + 1)
        self.db.outbox[event_id] = {"booking_id": booking_id, "kind": "payment_confirmed"}
        return "APPLIED"
