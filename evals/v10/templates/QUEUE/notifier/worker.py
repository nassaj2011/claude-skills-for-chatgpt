def claim(store, now, worker, lease_seconds=30):
    for job in store.jobs.values():
        if job["state"] != "SENT":
            job["state"] = "RUNNING"
            job["worker"] = worker
            job["lease_until"] = now + lease_seconds
            job["attempts"] += 1
            return dict(job)
    return None

def ack(store, job_id, worker, receipt, verified):
    job = store.jobs[job_id]
    job["state"] = "SENT"
    store.receipts[receipt] = job_id
    return "APPLIED"

def fail(store, job_id, worker):
    job = store.jobs[job_id]
    job["state"] = "PENDING"
    return True
