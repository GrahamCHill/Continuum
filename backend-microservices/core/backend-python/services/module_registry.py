import os
import httpx
from typing import List

from shared.schemas.module_manifest import ModuleManifest


MODULE_ENV_PREFIX = "MODULE_"


def _module_urls() -> List[str]:
    urls = []
    for key, value in os.environ.items():
        if key.startswith(MODULE_ENV_PREFIX):
            urls.append(value)
    return urls


def load_modules() -> List[ModuleManifest]:
    modules: List[ModuleManifest] = []

    for base_url in _module_urls():
        try:
            resp = httpx.get(
                f"{base_url}/internal/module-manifest",
                timeout=2.0,
            )
            resp.raise_for_status()

            manifest = ModuleManifest(**resp.json())
            modules.append(manifest)

        except Exception as e:
            # IMPORTANT: failure of a module must not break the core
            print(f"[modules] failed to load {base_url}: {e}")

    return modules
