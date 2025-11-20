from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional


@dataclass
class FrameData:
    """Represents a single frame in the editor."""
    source_path: Optional[str]
    display_name: str
    duration_ms: int
    is_custom_duration: bool
    is_checked: bool = False


@dataclass
class AppConfig:
    """Persisted application configuration."""
    theme: str = "system"
    thumb_size: int = 64
    remember_add_dir: bool = True
    remember_open_dir: bool = True
    remember_save_dir: bool = True
    remember_export_dir: bool = True
    remember_geometry: bool = True
    last_add_dir: str = ""
    last_open_dir: str = ""
    last_save_dir: str = ""
    last_export_dir: str = ""


def config_path(base_dir: Path) -> Path:
    """Return the path to the JSON config file."""
    # Keep filename for compatibility with earlier version
    return base_dir / "geeks_gif_editor_settings.json"


def load_config(base_dir: Path) -> AppConfig:
    """Load configuration from disk, or return defaults on failure."""
    path = config_path(base_dir)
    if path.exists():
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            return AppConfig(**data)
        except Exception:
            # Fall back to defaults if anything goes wrong
            pass
    return AppConfig()


def save_config(base_dir: Path, config: AppConfig) -> None:
    """Save configuration to disk, ignoring errors."""
    path = config_path(base_dir)
    try:
        path.write_text(json.dumps(asdict(config), indent=2), encoding="utf-8")
    except Exception:
        # Config failure shouldn't crash the app
        pass
