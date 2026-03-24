import yaml
from pathlib import Path

def load_config() -> dict:
    """Load configuration with validation."""
    candidates = [Path("configs/config.yaml"), Path("configs/configs.yml")]
    config_path = next((path for path in candidates if path.exists()), None)
    if config_path is None:
        raise FileNotFoundError("No config file found. Expected configs/config.yaml or configs/configs.yml")
    with open(config_path, "r") as f:
        return yaml.safe_load(f)