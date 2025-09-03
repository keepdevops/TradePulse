#!/usr/bin/env python3
"""
TradePulse UI Panels - Data Displays Formatters
Data formatting utilities for the data displays
"""

import logging

logger = logging.getLogger(__name__)

class DataDisplaysFormatters:
    """Data formatting utilities for data displays"""
    
    def format_volume(self, volume: int) -> str:
        """Format volume with appropriate units"""
        try:
            if volume >= 1_000_000_000:
                return f"{volume / 1_000_000_000:.2f}B"
            elif volume >= 1_000_000:
                return f"{volume / 1_000_000:.2f}M"
            elif volume >= 1_000:
                return f"{volume / 1_000:.2f}K"
            else:
                return str(volume)
        except Exception as e:
            logger.error(f"Failed to format volume: {e}")
            return "0"
    
    def format_market_cap(self, market_cap: float) -> str:
        """Format market cap with appropriate units"""
        try:
            if market_cap >= 1_000_000_000_000:
                return f"${market_cap / 1_000_000_000_000:.2f}T"
            elif market_cap >= 1_000_000_000:
                return f"${market_cap / 1_000_000_000:.2f}B"
            elif market_cap >= 1_000_000:
                return f"${market_cap / 1_000_000:.2f}M"
            else:
                return f"${market_cap:.2f}"
        except Exception as e:
            logger.error(f"Failed to format market cap: {e}")
            return "$0.00"
    
    def format_price(self, price: float, decimals: int = 2) -> str:
        """Format price with specified decimal places"""
        try:
            return f"${price:.{decimals}f}"
        except Exception as e:
            logger.error(f"Failed to format price: {e}")
            return "$0.00"
    
    def format_change(self, change: float, change_percent: float) -> str:
        """Format price change with color coding"""
        try:
            change_symbol = "+" if change >= 0 else ""
            return f"{change_symbol}${change:.2f} ({change_symbol}{change_percent:.2f}%)"
        except Exception as e:
            logger.error(f"Failed to format change: {e}")
            return "$0.00 (0.00%)"
    
    def format_percentage(self, percentage: float, decimals: int = 2) -> str:
        """Format percentage with specified decimal places"""
        try:
            return f"{percentage:.{decimals}f}%"
        except Exception as e:
            logger.error(f"Failed to format percentage: {e}")
            return "0.00%"
    
    def format_ratio(self, ratio: float, decimals: int = 2) -> str:
        """Format ratio with specified decimal places"""
        try:
            return f"{ratio:.{decimals}f}"
        except Exception as e:
            logger.error(f"Failed to format ratio: {e}")
            return "0.00"
    
    def format_currency(self, amount: float, currency: str = "USD", decimals: int = 2) -> str:
        """Format currency amount"""
        try:
            if currency == "USD":
                return f"${amount:.{decimals}f}"
            elif currency == "EUR":
                return f"€{amount:.{decimals}f}"
            elif currency == "GBP":
                return f"£{amount:.{decimals}f}"
            else:
                return f"{currency} {amount:.{decimals}f}"
        except Exception as e:
            logger.error(f"Failed to format currency: {e}")
            return "$0.00"
    
    def format_number_with_commas(self, number: float) -> str:
        """Format number with comma separators"""
        try:
            return f"{number:,.0f}"
        except Exception as e:
            logger.error(f"Failed to format number with commas: {e}")
            return "0"
    
    def format_scientific_notation(self, number: float, precision: int = 2) -> str:
        """Format number in scientific notation"""
        try:
            return f"{number:.{precision}e}"
        except Exception as e:
            logger.error(f"Failed to format scientific notation: {e}")
            return "0.00e+00"
    
    def format_duration(self, seconds: float) -> str:
        """Format duration in human readable format"""
        try:
            if seconds < 60:
                return f"{seconds:.1f}s"
            elif seconds < 3600:
                minutes = seconds / 60
                return f"{minutes:.1f}m"
            elif seconds < 86400:
                hours = seconds / 3600
                return f"{hours:.1f}h"
            else:
                days = seconds / 86400
                return f"{days:.1f}d"
        except Exception as e:
            logger.error(f"Failed to format duration: {e}")
            return "0s"
    
    def format_file_size(self, bytes_size: int) -> str:
        """Format file size in human readable format"""
        try:
            if bytes_size < 1024:
                return f"{bytes_size}B"
            elif bytes_size < 1024**2:
                return f"{bytes_size / 1024:.1f}KB"
            elif bytes_size < 1024**3:
                return f"{bytes_size / (1024**2):.1f}MB"
            else:
                return f"{bytes_size / (1024**3):.1f}GB"
        except Exception as e:
            logger.error(f"Failed to format file size: {e}")
            return "0B"
    
    def format_timestamp(self, timestamp, format_str: str = "%Y-%m-%d %H:%M:%S") -> str:
        """Format timestamp"""
        try:
            if hasattr(timestamp, 'strftime'):
                return timestamp.strftime(format_str)
            else:
                return str(timestamp)
        except Exception as e:
            logger.error(f"Failed to format timestamp: {e}")
            return "Unknown"
    
    def format_range(self, low: float, high: float, separator: str = " - ") -> str:
        """Format range between two values"""
        try:
            return f"{low:.2f}{separator}{high:.2f}"
        except Exception as e:
            logger.error(f"Failed to format range: {e}")
            return "0.00 - 0.00"



