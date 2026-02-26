import os
import yaml
from typing import Any, Dict


class ConfigNamespace:
    """
    Allows dot-notation access to nested dictionaries.
    Example:
        cfg.health.weights.cashflow
    """
    def __init__(self, data: Dict[str, Any]):
        for key, value in data.items():
            if isinstance(value, dict):
                value = ConfigNamespace(value)
            setattr(self, key, value)

    def __getitem__(self, item):
        return getattr(self, item)

    def to_dict(self):
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, ConfigNamespace):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result


class ConfigLoader:
    """
    Loads YAML config files from the config/ directory.
    Caches results so each file is loaded only once.
    Expands environment variables automatically.
    """

    def __init__(self, base_path: str = None):
        self.base_path = base_path or os.path.join(os.getcwd(), "financial_intelligence_system", "config")
        self._cache: Dict[str, ConfigNamespace] = {}

    def _expand_env_vars(self, data: Any) -> Any:
        if isinstance(data, dict):
            return {k: self._expand_env_vars(v) for k, v in data.items()}
        if isinstance(data, list):
            return [self._expand_env_vars(v) for v in data]
        if isinstance(data, str) and data.startswith("$"):
            env_var = data[1:]
            return os.getenv(env_var, "")
        return data

    def load(self, filename: str) -> ConfigNamespace:
        """
        Loads a YAML config file and returns a ConfigNamespace.
        Uses caching to avoid repeated disk reads.
        """
        if filename in self._cache:
            return self._cache[filename]

        path = os.path.join(self.base_path, filename)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Config file not found: {path}")

        with open(path, "r") as f:
            raw = yaml.safe_load(f) or {}

        expanded = self._expand_env_vars(raw)
        namespace = ConfigNamespace(expanded)
        self._cache[filename] = namespace
        return namespace

    def reload(self, filename: str) -> ConfigNamespace:
        """Forces reload of a config file."""
        if filename in self._cache:
            del self._cache[filename]
        return self.load(filename)


# Singleton instance for convenience
config = ConfigLoader()
