#!/usr/bin/env python3
"""
Model Visualizer for Models Grid
Consolidates visualization functionality for all models.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from typing import Dict, Any, Optional, List
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from utils.logger import setup_logger
from utils.message_bus_client import MessageBusClient
from utils.config_loader import ConfigLoader

logger = setup_logger(__name__)


class ModelVisualizer:
    """Consolidated model visualizer for all model types."""
    
    def __init__(self, config: ConfigLoader, message_bus: MessageBusClient):
        """Initialize the model visualizer."""
        self.config = config
        self.message_bus = message_bus
        self.logger = setup_logger(__name__)
        
        # Set plotting style
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def plot_predictions_vs_actual(self, y_true: np.ndarray, y_pred: np.ndarray, 
                                  title: str = "Predictions vs Actual", 
                                  save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a scatter plot of predictions vs actual values.
        
        Args:
            y_true: True target values
            y_pred: Predicted values
            title: Plot title
            save_path: Optional path to save the plot
            
        Returns:
            Matplotlib figure object
        """
        try:
            fig, ax = plt.subplots(figsize=(10, 8))
            
            # Create scatter plot
            ax.scatter(y_true, y_pred, alpha=0.6, s=50)
            
            # Add perfect prediction line
            min_val = min(y_true.min(), y_pred.min())
            max_val = max(y_true.max(), y_pred.max())
            ax.plot([min_val, max_val], [min_val, max_val], 'r--', lw=2, label='Perfect Prediction')
            
            # Customize plot
            ax.set_xlabel('Actual Values')
            ax.set_ylabel('Predicted Values')
            ax.set_title(title)
            ax.legend()
            ax.grid(True, alpha=0.3)
            
            # Add R² value
            r2 = np.corrcoef(y_true, y_pred)[0, 1] ** 2
            ax.text(0.05, 0.95, f'R² = {r2:.3f}', transform=ax.transAxes, 
                   bbox=dict(boxstyle="round", facecolor='wheat', alpha=0.8))
            
            if save_path:
                fig.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"Saved prediction plot to {save_path}")
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating predictions vs actual plot: {e}")
            raise
    
    def plot_feature_importance(self, feature_names: List[str], 
                               importance_scores: np.ndarray,
                               title: str = "Feature Importance",
                               save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a bar plot of feature importance scores.
        
        Args:
            feature_names: List of feature names
            importance_scores: Array of importance scores
            title: Plot title
            save_path: Optional path to save the plot
            
        Returns:
            Matplotlib figure object
        """
        try:
            # Sort features by importance
            sorted_indices = np.argsort(importance_scores)[::-1]
            sorted_names = [feature_names[i] for i in sorted_indices]
            sorted_scores = importance_scores[sorted_indices]
            
            fig, ax = plt.subplots(figsize=(12, 8))
            
            # Create horizontal bar plot
            bars = ax.barh(range(len(sorted_names)), sorted_scores)
            
            # Customize plot
            ax.set_yticks(range(len(sorted_names)))
            ax.set_yticklabels(sorted_names)
            ax.set_xlabel('Importance Score')
            ax.set_title(title)
            ax.grid(True, alpha=0.3)
            
            # Add value labels on bars
            for i, (bar, score) in enumerate(zip(bars, sorted_scores)):
                ax.text(score + 0.01, i, f'{score:.3f}', 
                       va='center', fontweight='bold')
            
            if save_path:
                fig.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"Saved feature importance plot to {save_path}")
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating feature importance plot: {e}")
            raise
    
    def plot_model_comparison(self, model_results: Dict[str, Dict[str, float]],
                             metrics: List[str] = ['mse', 'mae', 'r2'],
                             title: str = "Model Performance Comparison",
                             save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a comparison plot of different models' performance.
        
        Args:
            model_results: Dictionary of model results with metrics
            metrics: List of metrics to compare
            title: Plot title
            save_path: Optional path to save the plot
            
        Returns:
            Matplotlib figure object
        """
        try:
            fig, axes = plt.subplots(1, len(metrics), figsize=(5*len(metrics), 6))
            if len(metrics) == 1:
                axes = [axes]
            
            model_names = list(model_results.keys())
            
            for i, metric in enumerate(metrics):
                values = [model_results[model].get(metric, 0) for model in model_names]
                
                bars = axes[i].bar(model_names, values, alpha=0.7)
                axes[i].set_title(f'{metric.upper()} Comparison')
                axes[i].set_ylabel(metric.upper())
                axes[i].grid(True, alpha=0.3)
                
                # Add value labels on bars
                for bar, value in zip(bars, values):
                    axes[i].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                               f'{value:.3f}', ha='center', va='bottom')
            
            plt.suptitle(title, fontsize=16)
            plt.tight_layout()
            
            if save_path:
                fig.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"Saved model comparison plot to {save_path}")
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating model comparison plot: {e}")
            raise
    
    def plot_training_history(self, history: Dict[str, List[float]],
                             title: str = "Training History",
                             save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a plot of training history (loss, accuracy, etc.).
        
        Args:
            history: Dictionary containing training metrics over epochs
            title: Plot title
            save_path: Optional path to save the plot
            
        Returns:
            Matplotlib figure object
        """
        try:
            fig, axes = plt.subplots(1, len(history), figsize=(5*len(history), 5))
            if len(history) == 1:
                axes = [axes]
            
            for i, (metric, values) in enumerate(history.items()):
                epochs = range(1, len(values) + 1)
                axes[i].plot(epochs, values, 'b-', marker='o')
                axes[i].set_title(f'{metric.title()}')
                axes[i].set_xlabel('Epoch')
                axes[i].set_ylabel(metric.title())
                axes[i].grid(True, alpha=0.3)
            
            plt.suptitle(title, fontsize=16)
            plt.tight_layout()
            
            if save_path:
                fig.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"Saved training history plot to {save_path}")
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating training history plot: {e}")
            raise
    
    def create_dashboard(self, model_results: Dict[str, Any],
                        save_path: Optional[str] = None) -> plt.Figure:
        """
        Create a comprehensive dashboard with multiple visualizations.
        
        Args:
            model_results: Dictionary containing model results and data
            save_path: Optional path to save the dashboard
            
        Returns:
            Matplotlib figure object
        """
        try:
            fig = plt.figure(figsize=(20, 12))
            
            # Create subplots for different visualizations
            gs = fig.add_gridspec(2, 3, hspace=0.3, wspace=0.3)
            
            # Example dashboard layout - adjust based on available data
            ax1 = fig.add_subplot(gs[0, :2])  # Predictions vs Actual
            ax2 = fig.add_subplot(gs[0, 2])   # Feature Importance
            ax3 = fig.add_subplot(gs[1, :])   # Model Comparison
            
            # Add placeholder text for now
            ax1.text(0.5, 0.5, 'Predictions vs Actual\n(Data required)', 
                    ha='center', va='center', transform=ax1.transAxes, fontsize=14)
            ax2.text(0.5, 0.5, 'Feature Importance\n(Data required)', 
                    ha='center', va='center', transform=ax2.transAxes, fontsize=14)
            ax3.text(0.5, 0.5, 'Model Comparison\n(Data required)', 
                    ha='center', va='center', transform=ax3.transAxes, fontsize=14)
            
            plt.suptitle('Model Analysis Dashboard', fontsize=18)
            
            if save_path:
                fig.savefig(save_path, dpi=300, bbox_inches='tight')
                self.logger.info(f"Saved dashboard to {save_path}")
            
            return fig
            
        except Exception as e:
            self.logger.error(f"Error creating dashboard: {e}")
            raise
