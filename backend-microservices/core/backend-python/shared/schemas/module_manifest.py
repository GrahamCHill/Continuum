from pydantic import BaseModel
from typing import List, Optional, Literal


class ModuleNavigation(BaseModel):
    label: str
    icon: Optional[str] = None


class ModuleUI(BaseModel):
    type: Literal["iframe"]
    entry: str
    navigation: Optional[ModuleNavigation] = None


class ModuleManifest(BaseModel):
    id: str
    name: str
    version: str
    base_path: str
    capabilities: List[str]
    ui: Optional[ModuleUI] = None
