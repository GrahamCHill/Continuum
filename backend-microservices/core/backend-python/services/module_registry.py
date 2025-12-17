import json
import os
from shared.schemas.module_manifest import (
    ModuleManifest,
    ModuleWidget,
    ModuleRoute,
)

MODULES_PATH = "/modules"


def load_module(module_name: str) -> ModuleManifest:
    base = os.path.join(MODULES_PATH, module_name, "backend-python", "ui-dist")

    with open(os.path.join(base, "module.json")) as f:
        meta = json.load(f)

    with open(os.path.join(base, "routes.json")) as f:
        routes_raw = json.load(f)["routes"]

    with open(os.path.join(base, "widgets.json")) as f:
        widgets_raw = json.load(f)["widgets"]

    with open(os.path.join(base, "permissions.json")) as f:
        perms = json.load(f)["permissions"]

    return ModuleManifest(
        id=meta["id"],
        name=meta["name"],
        version=meta["version"],
        description=meta["description"],
        scope="project",
        permissions=perms,
        routes=[ModuleRoute(**r) for r in routes_raw],
        widgets=[ModuleWidget(**w) for w in widgets_raw],
    )


def load_modules():
    modules = []
    for name in os.listdir(MODULES_PATH):
        try:
            modules.append(load_module(name))
        except Exception:
            continue
    return modules
