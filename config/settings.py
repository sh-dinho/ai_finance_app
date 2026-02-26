import os
from dataclasses import dataclass
from typing import Any
from .env_loader import load_dotenv
from .config_loader import config


@dataclass
class Settings:
    weights: Any
    thresholds: Any
    features: Any
    paths: Any
    email: Any
    project: Any

    @classmethod
    def load(cls):
        # Load .env from the same directory as this file (config/)
        env_path = os.path.join(os.path.dirname(__file__), ".env")
        load_dotenv(env_path)

        return cls(
            weights=config.load("weights.yaml"),
            thresholds=config.load("thresholds.yaml"),
            features=config.load("features.yaml"),
            paths=config.load("paths.yaml"),
            email=config.load("email.yaml"),
            project=config.load("project.yaml"),
        )