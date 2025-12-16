from fastapi import APIRouter
from typing import List

from services.module_registry import load_modules
from shared.schemas.module_manifest import ModuleManifest

router = APIRouter()


@router.get("/modules", response_model=List[ModuleManifest])
def list_modules():
    """
    Return all available modules and their frontend-facing metadata.
    """
    return load_modules()
