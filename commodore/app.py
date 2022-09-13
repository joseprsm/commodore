from fastapi import FastAPI

from commodore.routers import plans, spaces, subscriptions, users


app = FastAPI()
app.include_router(users.router)
app.include_router(plans.router)
app.include_router(subscriptions.router)
app.include_router(spaces.router)
