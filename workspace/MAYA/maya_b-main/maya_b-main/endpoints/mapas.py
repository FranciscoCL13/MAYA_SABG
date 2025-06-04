from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core import get_db
from db import crud


router = APIRouter()


@router.get("/metadata")
async def get_metadata(db: Session = Depends(get_db)):
    return [{"label": x[1], "value": x[0]} for x in crud.metadata.get_metadata_list(db)]


@router.get("/layer/{id}")
async def get_layer(id: int, db: Session = Depends(get_db)):
    return crud.layer.load_layer(db, id)

@router.get("/areas/{id}")
async def get_layer(id: int, db: Session = Depends(get_db)):
    return crud.layer.load_areas(db, id)