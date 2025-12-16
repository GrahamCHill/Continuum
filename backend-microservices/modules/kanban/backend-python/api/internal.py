from fastapi import APIRouter

router = APIRouter(prefix="/internal")

@router.get("/module-manifest")
def module_manifest():
    return {
        "id": "kanban",
        "name": "Kanban Boards",
        "version": "0.1.0",
        "base_path": "/modules/kanban",
        "capabilities": [
            "kanban:boards",
            "kanban:cards"
        ],
        "ui": {
            "type": "iframe",
            "entry": "/ui",
            "navigation": {
                "label": "Kanban",
                "icon": "columns"
            }
        }
    }
