from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import constants
from context import get_playbook_context, get_main_page_context
from settings import settings
app = FastAPI(root_path=settings.root)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/data", StaticFiles(directory=settings.data_path), name="data")

templates = Jinja2Templates(directory="templates")


@app.get("/playbooks/", name='playbooks')
async def read_items_list(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse(
        request=request,
        name="playbooks_list.jinja2",
        context=get_main_page_context()
    )


@app.get("/playbooks/{playbook_name}/", name='get_playbook', response_class=HTMLResponse)
async def read_item(request: Request, playbook_name: str):
    if playbook_name in constants.playbook_names:
        return templates.TemplateResponse(
            request=request, name="playbook.jinja2", context=get_playbook_context(playbook_name)
        )
    else:
        raise HTTPException(status_code=404, detail="Playbook not found")
