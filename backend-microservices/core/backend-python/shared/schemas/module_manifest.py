from pydantic import BaseModel
from typing import List, Optional, Literal, Dict


class ModuleRoute(BaseModel):
    path: str
    methods: List[str]


class ModuleWidget(BaseModel):
    id: str
    type: Literal["table", "board", "list", "iframe"]
    title: str
    data_endpoint: Optional[str] = None
    iframe_src: Optional[str] = None


class ModuleManifest(BaseModel):
    id: str
    name: str
    version: str
    description: str
    widgets: List[ModuleWidget]
    routes: List[ModuleRoute]
    permissions: List[str]
    scope: Literal["project", "global"]
