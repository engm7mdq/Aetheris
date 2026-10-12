"""Central configuration for Aetheris (University Exam Scheduling Agent)."""
from __future__ import annotations

import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DATA_DIR = PROJECT_ROOT / "data"
DATASET_DIR = PROJECT_ROOT / "dataset"
SAMPLE_DIR = DATASET_DIR / "sample"
TEMPLATE_DIR = DATASET_DIR / "templates"
RESULTS_DIR = PROJECT_ROOT / "docs" / "results"

DEFAULT_DB_PATH = DATA_DIR / "exam_scheduler.db"
# Override with EXAM_DB_URL (e.g. "sqlite:///C:/temp/exams.db") if the project
# folder is synchronised by OneDrive and SQLite locking becomes a problem.
DATABASE_URL = os.environ.get("EXAM_DB_URL", f"sqlite:///{DEFAULT_DB_PATH.as_posix()}")

APP_NAME = "Aetheris"
APP_TAGLINE = "Intelligent Exam Scheduling"
APP_FULL_TITLE = "Aetheris — Intelligent Exam Scheduling"
APP_VERSION = "1.1.0"          # product/UI version (Aetheris branding, login, i18n, themes)
ALGORITHM_VERSION = "1.0.1"    # scheduling algorithm version: unchanged by the Aetheris UI upgrade

ASSETS_DIR = PROJECT_ROOT / "assets"
LOGO_MARK = ASSETS_DIR / "aetheris_mark.svg"
LOGO_LIGHT = ASSETS_DIR / "aetheris_logo_light.svg"
LOGO_DARK = ASSETS_DIR / "aetheris_logo_dark.svg"
FAVICON = ASSETS_DIR / "aetheris_icon_64.png"

# Upload safety limits
MAX_UPLOAD_BYTES = 5 * 1024 * 1024
MAX_UPLOAD_ROWS = 50_000

# A hard-constraint unit always outweighs any realistic soft penalty in the
# scalar fitness. Candidate comparison itself is lexicographic (hard, soft).
HARD_WEIGHT = 1_000_000.0

LOG_LEVEL = os.environ.get("EXAM_LOG_LEVEL", "INFO")
