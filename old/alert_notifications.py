#!/usr/bin/env python3
"""
TradePulse Alerts - Alert Notification System
Handles alert notifications and delivery
"""

import pandas as pd
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

class AlertNotificationSystem:
    """Handles alert notifications and delivery"""
    
    def __init__(self):
        self.notification_history = []
        self.supported_channels = ['Email', 'SMS', 'Push', 'Sound', 'Desktop']
    
    def send_notification(self, alert: Dict, trigger_info: Dict, 
                         channels: Optional[List[str]] = None) -> bool:
        """
        Send notification for a triggered alert
        
        Args:
            alert: The alert that was triggered
            trigger_info: Information about what triggered the alert
            channels: List of notification channels to use (defaults to alert's channels)
        
        Returns:
            bool: True if notification was sent successfully
        """
        try:
            if channels is None:
                channels = alert.get('notifications', ['Email'])
            
            # Validate channels
            valid_channels = [ch for ch in channels if ch in self.supported_channels]
            if not valid_channels:
                logger.warning(f"No valid notification channels found: {channels}")
                return False
            
            # Create notification record
            notification = {
                'alert_id': alert['id'],
                'alert_type': alert['type'],
                'channels': valid_channels,
                'trigger_time': pd.Timestamp.now(),
                'trigger_info': trigger_info,
                'status': 'pending'
            }
            
            # Send to each channel
            success_count = 0
            for channel in valid_channels:
                if self._send_to_channel(channel, alert, trigger_info):
                    success_count += 1
                    logger.info(f"✅ Notification sent via {channel} for alert {alert['id']}")
                else:
                    logger.error(f"❌ Failed to send notification via {channel} for alert {alert['id']}")
            
            # Update notification record
            notification['status'] = 'sent' if success_count > 0 else 'failed'
            notification['success_count'] = success_count
            self.notification_history.append(notification)
            
            return success_count > 0
            
        except Exception as e:
            logger.error(f"Failed to send notification: {e}")
            return False
    
    def _send_to_channel(self, channel: str, alert: Dict, trigger_info: Dict) -> bool:
        """Send notification to a specific channel"""
        try:
            if channel == 'Email':
                return self._send_email_notification(alert, trigger_info)
            elif channel == 'SMS':
                return self._send_sms_notification(alert, trigger_info)
            elif channel == 'Push':
                return self._send_push_notification(alert, trigger_info)
            elif channel == 'Sound':
                return self._send_sound_notification(alert, trigger_info)
            elif channel == 'Desktop':
                return self._send_desktop_notification(alert, trigger_info)
            else:
                logger.warning(f"Unsupported notification channel: {channel}")
                return False
                
        except Exception as e:
            logger.error(f"Failed to send {channel} notification: {e}")
            return False
    
    def _send_email_notification(self, alert: Dict, trigger_info: Dict) -> bool:
        """Send email notification"""
        try:
            # Here you would implement actual email sending
            # For now, just log the action
            subject = f"🚨 Alert Triggered: {alert['type']}"
            body = self._format_notification_message(alert, trigger_info)
            
            logger.info(f"📧 Email notification prepared:")
            logger.info(f"  Subject: {subject}")
            logger.info(f"  Body: {body[:100]}...")
            
            # Simulate email sending
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email notification: {e}")
            return False
    
    def _send_sms_notification(self, alert: Dict, trigger_info: Dict) -> bool:
        """Send SMS notification"""
        try:
            # Here you would implement actual SMS sending
            # For now, just log the action
            message = self._format_notification_message(alert, trigger_info, max_length=160)
            
            logger.info(f"📱 SMS notification prepared:")
            logger.info(f"  Message: {message}")
            
            # Simulate SMS sending
            return True
            
        except Exception as e:
            logger.error(f"Failed to send SMS notification: {e}")
            return False
    
    def _send_push_notification(self, alert: Dict, trigger_info: Dict) -> bool:
        """Send push notification"""
        try:
            # Here you would implement actual push notification
            # For now, just log the action
            title = f"🚨 {alert['type']}"
            body = self._format_notification_message(alert, trigger_info, max_length=100)
            
            logger.info(f"📲 Push notification prepared:")
            logger.info(f"  Title: {title}")
            logger.info(f"  Body: {body}")
            
            # Simulate push notification
            return True
            
        except Exception as e:
            logger.error(f"Failed to send push notification: {e}")
            return False
    
    def _send_sound_notification(self, alert: Dict, trigger_info: Dict) -> bool:
        """Send sound notification"""
        try:
            # Here you would implement actual sound notification
            # For now, just log the action
            logger.info(f"🔊 Sound notification prepared for alert {alert['id']}")
            
            # Simulate sound notification
            return True
            
        except Exception as e:
            logger.error(f"Failed to send sound notification: {e}")
            return False
    
    def _send_desktop_notification(self, alert: Dict, trigger_info: Dict) -> bool:
        """Send desktop notification"""
        try:
            # Here you would implement actual desktop notification
            # For now, just log the action
            title = f"🚨 {alert['type']}"
            body = self._format_notification_message(alert, trigger_info, max_length=200)
            
            logger.info(f"🖥️ Desktop notification prepared:")
            logger.info(f"  Title: {title}")
            logger.info(f"  Body: {body}")
            
            # Simulate desktop notification
            return True
            
        except Exception as e:
            logger.error(f"Failed to send desktop notification: {e}")
            return False
    
    def _format_notification_message(self, alert: Dict, trigger_info: Dict, 
                                   max_length: Optional[int] = None) -> str:
        """Format notification message based on alert and trigger info"""
        try:
            # Base message
            message = f"Alert '{alert['id']}' ({alert['type']}) has been triggered.\n"
            
            # Add trigger information
            if 'comparison' in trigger_info:
                message += f"Condition: {trigger_info['comparison']}\n"
            
            if 'current_price' in trigger_info:
                message += f"Current Price: ${trigger_info['current_price']:.2f}\n"
            
            if 'current_volume' in trigger_info:
                message += f"Current Volume: {trigger_info['current_volume']:,}\n"
            
            if 'price_change' in trigger_info:
                message += f"Price Change: {trigger_info['price_change']:.2f}%\n"
            
            if 'volume_change' in trigger_info:
                message += f"Volume Change: {trigger_info['volume_change']:.2f}%\n"
            
            # Add timestamp
            message += f"Triggered at: {pd.Timestamp.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            # Truncate if max_length specified
            if max_length and len(message) > max_length:
                message = message[:max_length-3] + "..."
            
            return message
            
        except Exception as e:
            logger.error(f"Failed to format notification message: {e}")
            return f"Alert {alert['id']} triggered at {pd.Timestamp.now()}"
    
    def get_notification_history(self, alert_id: Optional[str] = None) -> List[Dict]:
        """Get notification history, optionally filtered by alert ID"""
        if alert_id:
            return [n for n in self.notification_history if n['alert_id'] == alert_id]
        return self.notification_history.copy()
    
    def get_notification_statistics(self) -> Dict:
        """Get notification delivery statistics"""
        try:
            total_notifications = len(self.notification_history)
            successful_notifications = sum(1 for n in self.notification_history 
                                        if n['status'] == 'sent')
            failed_notifications = total_notifications - successful_notifications
            
            # Channel statistics
            channel_stats = {}
            for notification in self.notification_history:
                for channel in notification['channels']:
                    if channel not in channel_stats:
                        channel_stats[channel] = {'total': 0, 'successful': 0}
                    channel_stats[channel]['total'] += 1
                    if notification['status'] == 'sent':
                        channel_stats[channel]['successful'] += 1
            
            return {
                'total_notifications': total_notifications,
                'successful_notifications': successful_notifications,
                'failed_notifications': failed_notifications,
                'success_rate': (successful_notifications / total_notifications * 100) if total_notifications > 0 else 0,
                'channel_statistics': channel_stats
            }
            
        except Exception as e:
            logger.error(f"Failed to get notification statistics: {e}")
            return {}
    
    def clear_notification_history(self) -> int:
        """Clear notification history and return count of cleared notifications"""
        try:
            count = len(self.notification_history)
            self.notification_history.clear()
            logger.info(f"🗑️ Cleared {count} notification records")
            return count
        except Exception as e:
            logger.error(f"Failed to clear notification history: {e}")
            return 0
