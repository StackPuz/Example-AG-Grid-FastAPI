from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from sqlalchemy.sql import select, asc, desc, func
from app.db import get_db
from app.models.product import Product

router = APIRouter()

@router.get("/products")
def index(page: int = 1, size: int = 10, order = "id", direction = "asc", search = "", db: Session = Depends(get_db)):
    offset = (page - 1) * size
    sort_direction = asc if direction == "asc" else desc
    query = db.query(Product)
    if search:
        query = query.filter(Product.name.like(f"%{search}%"))
    count = query.count()
    products = (
        query
        .order_by(sort_direction(getattr(Product, order)))
        .offset(offset)
        .limit(size)
        .all()
    )
    return {
        "data": products,
        "count": count
    }