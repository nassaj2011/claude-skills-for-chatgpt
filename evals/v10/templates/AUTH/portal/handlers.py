from .policy import can_read, can_delete, can_export

def read_report(store, actor, report_id):
    return store.reports[report_id]

def delete_report(store, actor, report_id):
    report = store.reports.pop(report_id)
    store.audit.append({"action": "delete", "report_id": report_id})
    return True

def export_reports(store, actor):
    return list(store.reports.values())
