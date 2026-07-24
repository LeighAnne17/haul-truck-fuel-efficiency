import os
import yaml
import logging

logger = logging.getLogger(__name__)

class PipelineConfig:
    """Loads and validates the central configurationfile for the analytics pipeline."""

    def __init__(self, config_path: str = "config/config.yaml"):
        self.config_path = config_path
        self.settings = self._load_yaml()

    def _load_yaml(self) -> dict:
        """Reads the raw configuration file safely."""
        if not os.path.exists(self.config_path):
            logger.error(f"Configuration file missing at: {self.config_path}")
            raise FileNotFoundError(f"Missing setup configuration file: {self.config_path}")

        try:
            with open(self.config_path, "r") as file:
                config_dict = yaml.safe_load(file)
                logger.info(f"Configuration file successfully initialised from {self.config_path}")
                return config_dict
        except Exception as e:
            logger.error(f"Failed to parse YAML configuration: {str(e)}")
            raise e
    
    @property
    def paths(self) -> dict:
        return self.settings.get("paths", {})
    
    @property
    def financials(self) -> dict:
        return self.settings.get(f"financials", {})
    
    @property
    def anomaly_settings(self) -> dict:
        return self.settings.get("anomaly_detection", {})
        
    
