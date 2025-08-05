# app/routes.py
from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from app import crud, schemas, database

router = APIRouter()
templates = Jinja2Templates(directory="templates")

PRODUCT_TYPES = ["Electronics", "Clothing", "Books", "Toys", "Furniture", "Food", "Appliances", "Sports", "Beauty", "Tools"]
PRODUCTS = ["Item A", "Item B", "Item C", "Item D", "Item E", "Item F", "Item G", "Item H", "Item I", "Item J"]

@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@router.get("/register", response_class=HTMLResponse)
def register_get(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register", response_class=HTMLResponse)
def register_post(request: Request, username: str = Form(...), db: Session = Depends(database.get_db)):
    user = crud.create_user(db, username)
    if not user:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Already registered."})
    return templates.TemplateResponse("login.html", {"request": request, "uuid": user.uuid, "username": username})

@router.get("/login", response_class=HTMLResponse)
def login_get(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login", response_class=HTMLResponse)
def login_post(request: Request, username: str = Form(...), uuid: str = Form(...), db: Session = Depends(database.get_db)):
    user = crud.authenticate_user(db, username, uuid)
    if user:
        return templates.TemplateResponse("input_form.html", {
            "request": request,
            "username": username,
            "uuid": uuid,
            "types": PRODUCT_TYPES,
            "products": PRODUCTS
        })
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials."})

@router.post("/calculate", response_class=HTMLResponse)
def calculate_tax(
    request: Request,
    username: str = Form(...),
    uuid: str = Form(...),
    type: str = Form(...),
    product: str = Form(...),
    quantity: int = Form(...),
    weight: int = Form(...),
    db: Session = Depends(database.get_db)
):
    data = schemas.ProductInput(username=username, uuid=uuid, type=type, product=product, quantity=quantity, weight=weight)
    result = crud.save_product_entry(db, data)
    return templates.TemplateResponse("result.html", {
        "request": request,
        **result
    })
