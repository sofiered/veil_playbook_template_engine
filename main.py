import json
import pathlib

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import constants

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


@app.get("/playbooks/{playbook_name}", response_class=HTMLResponse)
async def read_item(request: Request, playbook_name: str):
    if playbook_name in constants.playbook_names:
        base_json_filename = f'{constants.jsons_path}/{constants.base_json_filename}'
        playbook_filename = f'{constants.jsons_path}/playbooks/{playbook_name}.json'
        with open(playbook_filename, "r") as playbook_file:
            playbook_context = json.load(playbook_file)
        with open(base_json_filename, "r") as base_file:
            base_context = json.load(base_file)
        return templates.TemplateResponse(
            request=request, name="playbook.jinja2", context={**base_context, **playbook_context}
        )
    else:
        raise HTTPException(status_code=404, detail="Playbook not found")
