from .app import app

from base import tunnel, db
from conf import settings


@app.on_event("startup")
async def startup():
    # Start the tunnel
    tunnel.start()
    # Create a database connection
    await db.set_bind(settings.POSTGRESS_URL)


@app.on_event("shutdown")
async def shutdown():
    tunnel.stop()
