#!/usr/bin/env python3
"""
TradePulse Main Application
Main entry point for launching modules and managing the Message Bus.
"""

import subprocess
import sys
import os
import signal
import time
from pathlib import Path
from typing import Dict, List, Optional
import json

# Add the project root to the Python path
sys.path.insert(0, str(Path(__file__).parent))

from utils.message_bus_client import MessageBusClient
from utils.config_loader import ConfigLoader
from utils.logger import setup_logger
from module_manager import ModuleManager

logger = setup_logger(__name__)


class TradePulseApp:
    """Main TradePulse application class."""
    
    def __init__(self):
        """Initialize the TradePulse application."""
        self.config = ConfigLoader().load_config()
        self.message_bus = MessageBusClient()
        self.module_manager = ModuleManager(self.message_bus)
        self.running = False
        
        # Ensure data and logs directories exist
        Path("data").mkdir(exist_ok=True)
        Path("logs").mkdir(exist_ok=True)
        
        # Setup signal handlers for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle shutdown signals."""
        logger.info(f"Received signal {signum}, shutting down gracefully...")
        self.shutdown()
        sys.exit(0)
    
    def launch_module(self, module_name: str) -> bool:
        """Launch a module as a subprocess."""
        return self.module_manager.launch_module(module_name)
    
    def launch_all_modules(self) -> None:
        """Launch all available modules."""
        self.module_manager.launch_all_modules()
    
    def check_module_health(self) -> Dict[str, bool]:
        """Check the health of all running modules."""
        return self.module_manager.check_module_health()
    
    def restart_module(self, module_name: str) -> bool:
        """Restart a failed module."""
        return self.module_manager.restart_module(module_name)
    
    def monitor_modules(self) -> None:
        """Monitor and maintain module health."""
        self.module_manager.monitor_modules(self.running)
    
    def shutdown(self) -> None:
        """Shutdown all modules gracefully."""
        logger.info("Shutting down TradePulse...")
        self.running = False
        
        # Shutdown module manager
        self.module_manager.shutdown()
        
        # Close message bus connection
        self.message_bus.close()
        logger.info("TradePulse shutdown complete")
    
    def run_interactive(self) -> None:
        """Run the application in interactive mode."""
        print("\n" + "="*50)
        print("TradePulse - Stock Market Analysis Platform")
        print("="*50)
        
        while True:
            print("\nAvailable options:")
            print("1. Launch Data Grid")
            print("2. Launch Analysis Grid")
            print("3. Launch Models Grid")
            print("4. Launch Trading Grid")
            print("5. Launch Portfolio Grid")
            print("6. Launch AI Module")
            print("7. Launch All Modules")
            print("8. Check Module Health")
            print("9. Exit")
            
            try:
                choice = input("\nSelect option (1-9): ").strip()
                
                if choice == "1":
                    self.launch_module("data_grid")
                elif choice == "2":
                    self.launch_module("analysis_grid")
                elif choice == "3":
                    self.launch_module("models_grid")
                elif choice == "4":
                    self.launch_module("trading_grid")
                elif choice == "5":
                    self.launch_module("portfolio_grid")
                elif choice == "6":
                    self.launch_module("ai_module")
                elif choice == "7":
                    self.launch_all_modules()
                elif choice == "8":
                    health = self.check_module_health()
                    print("\nModule Health Status:")
                    for module, status in health.items():
                        print(f"  {module}: {'Running' if status else 'Stopped'}")
                elif choice == "9":
                    break
                else:
                    print("Invalid option. Please select 1-9.")
                    
            except KeyboardInterrupt:
                break
            except Exception as e:
                logger.error(f"Error in interactive mode: {e}")
                print(f"Error: {e}")
    
    def run_daemon(self) -> None:
        """Run the application in daemon mode."""
        logger.info("Starting TradePulse in daemon mode...")
        self.running = True
        
        # Launch all modules
        self.launch_all_modules()
        
        # Start monitoring
        self.monitor_modules()
    
    def run(self, mode: str = "interactive") -> None:
        """Run the TradePulse application."""
        try:
            if mode == "daemon":
                self.run_daemon()
            else:
                self.run_interactive()
        except Exception as e:
            logger.error(f"Application error: {e}")
            raise
        finally:
            self.shutdown()


def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description="TradePulse Stock Market Analysis Platform")
    parser.add_argument(
        "--mode", 
        choices=["interactive", "daemon"], 
        default="interactive",
        help="Run mode (default: interactive)"
    )
    
    args = parser.parse_args()
    
    try:
        app = TradePulseApp()
        app.run(mode=args.mode)
    except KeyboardInterrupt:
        print("\nShutting down...")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
