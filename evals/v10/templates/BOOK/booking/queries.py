def get_booking(db, tenant, booking_id):
    return db.bookings.get(booking_id)

def list_bookings(db, tenant):
    return list(db.bookings.values())
