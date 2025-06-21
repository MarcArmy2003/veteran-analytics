import os
from pathlib import Path
from typing import Any, Dict

try:
    import yaml
except Exception:
    yaml = None

_config_cache: Dict[str, Any] = {}

def _load_yaml_config() -> Dict[str, Any]:
    config_file = os.getenv("VISTA_CONFIG_FILE", "config.yml")
    if yaml is None:
        return {}
    if Path(config_file).is_file():
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
        except Exception:
            return {}
    return {}

def get_path(key: str, default: str) -> Path:
    if key in _config_cache:
        return Path(_config_cache[key])
    env_val = os.getenv(key)
    if env_val:
        _config_cache[key] = env_val
        return Path(env_val)
    cfg = _load_yaml_config().get("paths", {})
    if key in cfg:
        _config_cache[key] = cfg[key]
        return Path(cfg[key])
    _config_cache[key] = default
    return Path(default)
