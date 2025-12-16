from fastapi import APIRouter
from infra.go_client import call_go_service

router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "Python backend up"}

@router.get("/go-data")
def call_go():
    return call_go_service()
