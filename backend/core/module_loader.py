from __future__ import annotations

import importlib
import inspect
from typing import List, Any, Dict

from core.vulnerability import VulnerabilityModule


def _try_import(module_path: str):
    try:
        return importlib.import_module(module_path)
    except Exception:
        return None


def load_module_by_name(name: str, config: Dict[str, Any], logger: Any) -> VulnerabilityModule:
    """Dynamically load a module by name and return an instantiated VulnerabilityModule.

    Tries several import paths: backend.modules.<name>.detector, modules.<name>.detector
    The detector module should expose one class that subclasses core.vulnerability.VulnerabilityModule.
    """
    candidates = [f"backend.modules.{name}.detector", f"modules.{name}.detector", f"backend.modules.{name}"]
    mod = None
    for path in candidates:
        mod = _try_import(path)
        if mod:
            break
    if mod is None:
        raise ImportError(f"Module {name} not found in paths: {candidates}")

    # Find a class in the module that subclasses VulnerabilityModule
    for _, obj in inspect.getmembers(mod, inspect.isclass):
        try:
            if issubclass(obj, VulnerabilityModule) and obj is not VulnerabilityModule:
                # instantiate with config and logger
                return obj(config, logger)
        except Exception:
            continue

    # If not found, raise
    raise ImportError(f"No VulnerabilityModule subclass found in module {mod.__name__}")


def load_modules(names: List[str], config: Dict[str, Any], logger: Any) -> List[VulnerabilityModule]:
    instances: List[VulnerabilityModule] = []
    for n in names:
        n = n.strip()
        if not n:
            continue
        inst = load_module_by_name(n, config, logger)
        instances.append(inst)
    return instances
