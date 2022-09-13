from fastapi import FastAPI

from commodore.routers import bookings, items, plans, spaces, subscriptions, users


app = FastAPI()
app.include_router(users.router)
app.include_router(plans.router)
app.include_router(subscriptions.router)
app.include_router(spaces.router)
app.include_router(items.router)
app.include_router(bookings.router)
