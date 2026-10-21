def counts(store):
    return {"PENDING": sum(j["state"] == "PENDING" for j in store.jobs.values()),
            "RUNNING": sum(j["state"] == "RUNNING" for j in store.jobs.values()),
            "SENT": sum(j["state"] == "SENT" for j in store.jobs.values()),
            "DEAD": sum(j["state"] == "DEAD" for j in store.jobs.values())}
