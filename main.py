import json

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import constants
from context import get_playbook_context
from settings import settings
app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/data", StaticFiles(directory=settings.data_path), name="data")

templates = Jinja2Templates(directory="templates")


@app.get("/playbooks/{playbook_name}", response_class=HTMLResponse)
async def read_item(request: Request, playbook_name: str):
    if playbook_name in constants.playbook_names:
        return templates.TemplateResponse(
            request=request, name="playbook.jinja2", context=get_playbook_context(playbook_name)
        )
    else:
        raise HTTPException(status_code=404, detail="Playbook not found")
