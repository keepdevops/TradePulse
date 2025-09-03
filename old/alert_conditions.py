#!/usr/bin/env python3
"""
TradePulse Alerts - Alert Condition Checker
Evaluates alert conditions against dataset data
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple, List
import logging

logger = logging.getLogger(__name__)

class AlertConditionChecker:
    """Evaluates alert conditions against dataset data"""
    
    def __init__(self):
        self.supported_conditions = {
            'Price Alert': self._check_price_condition,
            'Volume Alert': self._check_volume_condition,
            'Technical Indicator': self._check_technical_condition,
            'Custom Condition': self._check_custom_condition,
            'Pattern Recognition': self._check_pattern_condition
        }
    
    def check_alert_condition(self, alert: Dict, data: pd.DataFrame) -> Tuple[bool, Dict]:
        """
        Check if an alert condition is met
        
        Returns:
            Tuple[bool, Dict]: (condition_met, additional_info)
        """
        try:
            alert_type = alert['type']
            
            if alert_type in self.supported_conditions:
                return self.supported_conditions[alert_type](alert, data)
            else:
                logger.warning(f"Unsupported alert type: {alert_type}")
                return False, {'error': f'Unsupported alert type: {alert_type}'}
                
        except Exception as e:
            logger.error(f"Failed to check alert condition: {e}")
            return False, {'error': str(e)}
    
    def _check_price_condition(self, alert: Dict, data: pd.DataFrame) -> Tuple[bool, Dict]:
        """Check price-based alert conditions"""
        try:
            condition = alert['condition']
            threshold = alert['threshold']
            percentage = alert['percentage']
            
            if 'Close' not in data.columns:
                return False, {'error': 'No Close price data available'}
            
            latest_price = data['Close'].iloc[-1]
            info = {
                'current_price': latest_price,
                'threshold': threshold,
                'condition': condition
            }
            
            if condition == 'Above':
                triggered = latest_price > threshold
                info['comparison'] = f"{latest_price} > {threshold}"
                
            elif condition == 'Below':
                triggered = latest_price < threshold
                info['comparison'] = f"{latest_price} < {threshold}"
                
            elif condition == 'Crosses Above':
                if len(data) < 2:
                    return False, {'error': 'Insufficient data for crossing condition'}
                prev_price = data['Close'].iloc[-2]
                triggered = prev_price <= threshold and latest_price > threshold
                info['comparison'] = f"{prev_price} <= {threshold} and {latest_price} > {threshold}"
                
            elif condition == 'Crosses Below':
                if len(data) < 2:
                    return False, {'error': 'Insufficient data for crossing condition'}
                prev_price = data['Close'].iloc[-2]
                triggered = prev_price >= threshold and latest_price < threshold
                info['comparison'] = f"{prev_price} >= {threshold} and {latest_price} < {threshold}"
                
            elif condition == 'Changes By':
                if len(data) < 2:
                    return False, {'error': 'Insufficient data for change calculation'}
                prev_price = data['Close'].iloc[-2]
                price_change = abs((latest_price - prev_price) / prev_price) * 100
                triggered = price_change > percentage
                info['comparison'] = f"Change: {price_change:.2f}% > {percentage}%"
                info['price_change'] = price_change
                
            else:
                return False, {'error': f'Unsupported price condition: {condition}'}
            
            return triggered, info
            
        except Exception as e:
            logger.error(f"Failed to check price condition: {e}")
            return False, {'error': str(e)}
    
    def _check_volume_condition(self, alert: Dict, data: pd.DataFrame) -> Tuple[bool, Dict]:
        """Check volume-based alert conditions"""
        try:
            condition = alert['condition']
            threshold = alert['threshold']
            percentage = alert['percentage']
            
            if 'Volume' not in data.columns:
                return False, {'error': 'No Volume data available'}
            
            latest_volume = data['Volume'].iloc[-1]
            avg_volume = data['Volume'].mean()
            info = {
                'current_volume': latest_volume,
                'average_volume': avg_volume,
                'threshold': threshold,
                'condition': condition
            }
            
            if condition == 'Above':
                triggered = latest_volume > threshold
                info['comparison'] = f"{latest_volume} > {threshold}"
                
            elif condition == 'Below':
                triggered = latest_volume < threshold
                info['comparison'] = f"{latest_volume} < {threshold}"
                
            elif condition == 'Changes By':
                volume_change = abs((latest_volume - avg_volume) / avg_volume) * 100
                triggered = volume_change > percentage
                info['comparison'] = f"Change: {volume_change:.2f}% > {percentage}%"
                info['volume_change'] = volume_change
                
            else:
                return False, {'error': f'Unsupported volume condition: {condition}'}
            
            return triggered, info
            
        except Exception as e:
            logger.error(f"Failed to check volume condition: {e}")
            return False, {'error': str(e)}
    
    def _check_technical_condition(self, alert: Dict, data: pd.DataFrame) -> Tuple[bool, Dict]:
        """Check technical indicator-based alert conditions"""
        try:
            # This would implement technical indicator calculations
            # For now, return a placeholder implementation
            logger.info("Technical indicator conditions not yet implemented")
            return False, {'info': 'Technical indicator conditions coming soon'}
            
        except Exception as e:
            logger.error(f"Failed to check technical condition: {e}")
            return False, {'error': str(e)}
    
    def _check_custom_condition(self, alert: Dict, data: pd.DataFrame) -> Tuple[bool, Dict]:
        """Check custom condition-based alert conditions"""
        try:
            # This would implement custom condition evaluation
            # For now, return a placeholder implementation
            logger.info("Custom conditions not yet implemented")
            return False, {'info': 'Custom conditions coming soon'}
            
        except Exception as e:
            logger.error(f"Failed to check custom condition: {e}")
            return False, {'error': str(e)}
    
    def _check_pattern_condition(self, alert: Dict, data: pd.DataFrame) -> Tuple[bool, Dict]:
        """Check pattern recognition-based alert conditions"""
        try:
            # This would implement pattern recognition
            # For now, return a placeholder implementation
            logger.info("Pattern recognition not yet implemented")
            return False, {'info': 'Pattern recognition coming soon'}
            
        except Exception as e:
            logger.error(f"Failed to check pattern condition: {e}")
            return False, {'error': str(e)}
    
    def get_supported_conditions(self) -> List[str]:
        """Get list of supported alert conditions"""
        return list(self.supported_conditions.keys())
    
    def validate_alert_config(self, alert_config: Dict) -> Tuple[bool, List[str]]:
        """Validate alert configuration and return errors if any"""
        errors = []
        
        required_fields = ['type', 'condition', 'threshold']
        for field in required_fields:
            if field not in alert_config:
                errors.append(f"Missing required field: {field}")
        
        if 'type' in alert_config and alert_config['type'] not in self.supported_conditions:
            errors.append(f"Unsupported alert type: {alert_config['type']}")
        
        if 'threshold' in alert_config:
            try:
                float(alert_config['threshold'])
            except (ValueError, TypeError):
                errors.append("Threshold must be a valid number")
        
        if 'percentage' in alert_config:
            try:
                float(alert_config['percentage'])
            except (ValueError, TypeError):
                errors.append("Percentage must be a valid number")
        
        return len(errors) == 0, errors
