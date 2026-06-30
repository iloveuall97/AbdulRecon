import yaml
from pathlib import Path
from typing import Dict, Any

class ConfigLoader:
    """Load and manage configuration files"""
    
    def __init__(self, config_path="config/local.yaml", default_config="config/default.yaml"):
        self.config_path = config_path
        self.default_config = default_config
        self.config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration with fallback to defaults"""
        # Load default config
        default = self._read_yaml(self.default_config)
        
        # Load local config if exists
        if Path(self.config_path).exists():
            local = self._read_yaml(self.config_path)
            # Merge configs (local overrides default)
            return self._merge_dicts(default, local)
        
        return default
    
    @staticmethod
    def _read_yaml(path: str) -> Dict[str, Any]:
        """Read YAML file"""
        try:
            with open(path, 'r') as f:
                return yaml.safe_load(f) or {}
        except FileNotFoundError:
            return {}
        except yaml.YAMLError as e:
            raise ValueError(f"Invalid YAML in {path}: {e}")
    
    @staticmethod
    def _merge_dicts(base: Dict, override: Dict) -> Dict:
        """Recursively merge dictionaries"""
        result = base.copy()
        for key, value in override.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = ConfigLoader._merge_dicts(result[key], value)
            else:
                result[key] = value
        return result
    
    def get(self, key: str, default=None) -> Any:
        """Get configuration value by dot notation (e.g., 'app.debug')"""
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
        
        return value if value is not None else default
    
    def get_all(self) -> Dict[str, Any]:
        """Get entire configuration"""
        return self.config