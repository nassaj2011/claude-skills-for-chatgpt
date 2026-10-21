import threading

class MemoryDB:
    def __init__(self):
        self.lock = threading.RLock()
        self.bookings = {}
        self.slot_index = {}
        self.receipts = {}
        self.outbox = {}
