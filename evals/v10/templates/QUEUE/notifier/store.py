import threading

class QueueStore:
    def __init__(self):
        self.lock = threading.RLock()
        self.jobs = {}
        self.receipts = {}
