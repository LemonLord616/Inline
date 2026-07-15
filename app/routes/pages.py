from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from models import Queue, Participant, SwapRequest
import qrcode
import qrcode.image.svg
from io import BytesIO
import os

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def gen_qr_svg(url: str) -> str:
    factory = qrcode.image.svg.SvgPathImage
    img = qrcode.make(url, image_factory=factory)
    buf = BytesIO()
    img.save(buf)
    return buf.getvalue().decode()


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
    base_url = os.getenv("BASE_URL", "http://localhost:9000")
    share_url = f"{base_url}/join/{queue.id}"
    qr_svg = gen_qr_svg(share_url)
    return templates.TemplateResponse("queue.html", {
        "request": request, "queue": queue, "share_url": share_url, "qr_svg": qr_svg,
    })


@router.get("/admin/{queue_id}", response_class=HTMLResponse)
async def admin_view(request: Request, queue_id: str, token: str, db: AsyncSession = Depends(get_db)):
    queue = await db.get(Queue, queue_id)
    if not queue or queue.organizer_token != token:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    base_url = os.getenv("BASE_URL", "http://localhost:9000")
    share_url = f"{base_url}/join/{queue.id}"
    qr_svg = gen_qr_svg(share_url)
    return templates.TemplateResponse("admin.html", {
        "request": request, "queue": queue, "token": token,
        "share_url": share_url, "qr_svg": qr_svg,
    })
