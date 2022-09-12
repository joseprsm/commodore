from fastapi import FastAPI

from commodore.app.routers import items, spaces, subscriptions, users


app = FastAPI()
app.include_router(users.router)
app.include_router(items.router)
app.include_router(subscriptions.router)
app.include_router(spaces.router)
