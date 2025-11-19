from typing import Final
from pathlib import Path

PROJECT_ROOT: Final[Path] = Path(__file__).resolve().parent.parent.parent

DATA_DIR: Final[Path] = PROJECT_ROOT / "data"

LOGS_DIR: Final[Path] = PROJECT_ROOT / "logs"

SRC_DIR: Final[Path] = PROJECT_ROOT / "src"


