from fastapi import APIRouter

from commodore.models import Booking


router = APIRouter()


@router.post("/{space}/bookings")
async def create_booking(space: str, booking: Booking):
    return booking.create(space)


@router.get("/{space}/bookings")
def get_bookings(space: str):
    return {"bookings": Booking.list(space)}


@router.get("/{space}/bookings/{booking_id}")
def get_booking(space: str, booking_id: str):
    return Booking.get(space, booking_id)


@router.put("/{space}/bookings/{booking_id}")
def update_booking(space: str, booking_id: str, update: dict):
    return Booking.update(space, booking_id, update)


@router.delete("/{space}/bookings/{booking_id}")
def delete_booking(space, booking_id):
    Booking.delete(space, booking_id)
    return {"msg": f"Booking {booking_id} deleted"}
