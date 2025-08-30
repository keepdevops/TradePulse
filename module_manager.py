"""
Module Manager
Handles launching, monitoring, and managing TradePulse modules.
"""

import subprocess
import sys
import time
from pathlib import Path
from typing import Dict
from utils.logger import setup_logger

logger = setup_logger(__name__)


class ModuleManager:
    """Manages TradePulse modules including launching, monitoring, and restarting."""
    
    def __init__(self, message_bus):
        """Initialize the module manager."""
        self.message_bus = message_bus
        self.processes: Dict[str, subprocess.Popen] = {}
    
    def launch_module(self, module_name: str) -> bool:
        """Launch a module as a subprocess."""
        try:
            module_path = Path(f"{module_name}/__main__.py")
            if not module_path.exists():
                logger.warning(f"Module {module_name} not found at {module_path}")
                return False
            
            # Launch the module
            process = subprocess.Popen(
                [sys.executable, str(module_path)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes[module_name] = process
            logger.info(f"Launched {module_name} with PID {process.pid}")
            
            # Subscribe to module messages
            self.message_bus.subscribe(f"{module_name}_heartbeat")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to launch {module_name}: {e}")
            return False
    
    def launch_all_modules(self) -> None:
        """Launch all available modules."""
        modules = [
            "data_grid",
            "analysis_grid", 
            "models_grid",
            "trading_grid",
            "portfolio_grid",
            "ai_module"
        ]
        
        logger.info("Launching all modules...")
        for module in modules:
            if self.launch_module(module):
                time.sleep(1)  # Small delay between launches
    
    def check_module_health(self) -> Dict[str, bool]:
        """Check the health of all running modules."""
        health_status = {}
        
        for module_name, process in self.processes.items():
            if process.poll() is None:
                # Process is still running
                health_status[module_name] = True
            else:
                # Process has terminated
                health_status[module_name] = False
                logger.warning(f"Module {module_name} has terminated")
        
        return health_status
    
    def restart_module(self, module_name: str) -> bool:
        """Restart a failed module."""
        if module_name in self.processes:
            self.processes[module_name].terminate()
            self.processes[module_name].wait()
            del self.processes[module_name]
        
        return self.launch_module(module_name)
    
    def monitor_modules(self, running: bool) -> None:
        """Monitor and maintain module health."""
        while running:
            health_status = self.check_module_health()
            
            # Restart failed modules
            for module_name, is_healthy in health_status.items():
                if not is_healthy:
                    logger.info(f"Restarting failed module: {module_name}")
                    self.restart_module(module_name)
            
            # Check for new messages
            try:
                message = self.message_bus.receive(timeout=1000)
                if message:
                    logger.info(f"Received message: {message}")
            except Exception as e:
                # Timeout or no messages
                pass
            
            time.sleep(5)  # Check every 5 seconds
    
    def shutdown(self) -> None:
        """Shutdown all modules gracefully."""
        # Terminate all processes
        for module_name, process in self.processes.items():
            try:
                logger.info(f"Terminating {module_name}...")
                process.terminate()
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                logger.warning(f"Force killing {module_name}")
                process.kill()
            except Exception as e:
                logger.error(f"Error terminating {module_name}: {e}")
