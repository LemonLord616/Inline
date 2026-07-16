from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import Queue
import qrcode
from io import BytesIO
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def _share_url(request: Request, queue_id: str) -> str:
    base_url = os.getenv("BASE_URL") or f"{request.url.scheme}://{request.headers.get('host', 'localhost:9000')}"
    return f"{base_url}/join/{queue_id}"


@router.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})


@router.get("/create", response_class=HTMLResponse)
async def create_page(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})


@router.get("/join/{queue_id}", response_class=HTMLResponse)
async def join_page(request: Request, queue_id: str, db: AsyncSession = Depends(get_db)):
    queue = await db.get(Queue, queue_id)
    if not queue:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return templates.TemplateResponse("join.html", {"request": request, "queue": queue})


@router.get("/queue/{queue_id}", response_class=HTMLResponse)
async def queue_view(request: Request, queue_id: str, db: AsyncSession = Depends(get_db)):
    queue = await db.get(Queue, queue_id)
    if not queue:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    share_url = _share_url(request, queue.id)
    return templates.TemplateResponse("queue.html", {
        "request": request, "queue": queue, "share_url": share_url,
    })


@router.get("/admin/{queue_id}", response_class=HTMLResponse)
async def admin_view(request: Request, queue_id: str, token: str, db: AsyncSession = Depends(get_db)):
    queue = await db.get(Queue, queue_id)
    if not queue or queue.organizer_token != token:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    share_url = _share_url(request, queue.id)
    return templates.TemplateResponse("admin.html", {
        "request": request, "queue": queue, "token": token,
        "share_url": share_url,
    })


@router.get("/api/queue/{queue_id}/qr")
async def queue_qr(request: Request, queue_id: str):
    share_url = _share_url(request, queue_id)
    img = qrcode.make(share_url)
    buf = BytesIO()
    img.save(buf, format='PNG')
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png", headers={"Cache-Control": "public, max-age=3600"})
