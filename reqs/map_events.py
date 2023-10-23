from .app import app
from fastapi.responses import HTMLResponse


from func import get_events, create_map_events
# from typing import Optional
# from fastapi import Header, Body


@app.get("/map_events", tags=["map_events"], response_class=HTMLResponse)
async def return_map_events():
    """возвращает карту со случаями определенной категории"""

    df = await get_events()
    map = create_map_events(df, 'Пневмония')

    return map.get_root().render()
