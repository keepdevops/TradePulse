"""
Configuration Loader Utility
Loads and validates configuration from config.json.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ConfigLoader:
    """Configuration loader for TradePulse."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the configuration loader."""
        if config_path is None:
            config_path = "config.json"
        
        self.config_path = Path(config_path)
        self._config: Optional[Dict[str, Any]] = None
    
    def load_config(self) -> Dict[str, Any]:
        """Load configuration from config.json."""
        if self._config is not None:
            return self._config
        
        try:
            if not self.config_path.exists():
                logger.warning(f"Config file not found: {self.config_path}")
                return self._get_default_config()
            
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            
            # Validate configuration
            validated_config = self._validate_config(config)
            self._config = validated_config
            
            logger.info("Configuration loaded successfully")
            return validated_config
            
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in config file: {e}")
            return self._get_default_config()
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            return self._get_default_config()
    
    def _validate_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Validate and set default values for configuration."""
        # Ensure required sections exist
        required_sections = [
            'database', 'redline', 'live_feed', 'broker', 
            'models', 'visualization', 'alerts', 'backtest',
            'sentiment', 'portfolio', 'ai_module', 'message_bus',
            'logging', 'performance'
        ]
        
        for section in required_sections:
            if section not in config:
                config[section] = {}
                logger.warning(f"Missing config section: {section}, using defaults")
        
        # Set default values for critical settings
        defaults = {
            'database': {
                'type': 'duckdb',
                'path': './data/redline_data.duckdb'
            },
            'message_bus': {
                'host': 'localhost',
                'port': 5555,
                'timeout': 5000
            },
            'logging': {
                'level': 'INFO',
                'file_path': './logs'
            }
        }
        
        for section, section_defaults in defaults.items():
            for key, value in section_defaults.items():
                if key not in config[section]:
                    config[section][key] = value
        
        return config
    
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration when config.json is not available."""
        logger.info("Using default configuration")
        
        return {
            'database': {
                'type': 'duckdb',
                'path': './data/redline_data.duckdb'
            },
            'redline': {
                'utility_path': './redline_utility',
                'output_format': 'duckdb',
                'data_path': './data/redline_data.duckdb'
            },
            'live_feed': {
                'enabled': True,
                'api_endpoint': 'https://api.schwab.com',
                'update_interval': 5,
                'max_tickers': 100
            },
            'broker': {
                'type': 'alpaca',
                'demo_mode': True
            },
            'models': {
                'enabled_models': ['lstm', 'xgboost', 'random_forest'],
                'training': {
                    'test_size': 0.2,
                    'random_state': 42
                }
            },
            'visualization': {
                'theme': 'plotly_white',
                'candlestick_charts': True,
                '3d_plots': True
            },
            'alerts': {
                'enabled': True,
                'desktop_notifications': True
            },
            'backtest': {
                'enabled': True,
                'initial_capital': 100000
            },
            'sentiment': {
                'enabled': True,
                'sources': ['twitter', 'news']
            },
            'portfolio': {
                'max_positions': 20,
                'position_sizing': 0.05
            },
            'ai_module': {
                'enabled': True,
                'strategies': ['trend_following', 'mean_reversion']
            },
            'message_bus': {
                'host': 'localhost',
                'port': 5555,
                'timeout': 5000
            },
            'logging': {
                'level': 'INFO',
                'file_path': './logs'
            },
            'performance': {
                'cache_size': 1000,
                'max_workers': 4
            }
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value by key (supports dot notation)."""
        config = self.load_config()
        
        if '.' in key:
            # Handle nested keys like 'database.type'
            keys = key.split('.')
            value = config
            for k in keys:
                if isinstance(value, dict) and k in value:
                    value = value[k]
                else:
                    return default
            return value
        else:
            return config.get(key, default)
    
    def reload(self) -> Dict[str, Any]:
        """Reload configuration from file."""
        self._config = None
        return self.load_config()
    
    def save_config(self, config: Dict[str, Any]) -> bool:
        """Save configuration to file."""
        try:
            # Ensure directory exists
            self.config_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
            
            self._config = config
            logger.info("Configuration saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Error saving configuration: {e}")
            return False
