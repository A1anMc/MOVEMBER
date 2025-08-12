#!/usr/bin/env python3
"""
Analytics package for Movember AI Rules System
Digital analytics, social media tracking, and Google Analytics integration
"""

__version__ = "1.0.0"
__author__ = "Movember AI Team"
__description__ = "Digital Analytics Integration for Movember"

# Import main analytics classes
try:
    from .digital_analytics import (
        UnifiedDigitalAnalytics,
        SocialMediaAnalytics,
        GoogleAnalyticsIntegration,
        AttributionModel
    )
except ImportError:
    # Fallback for when the main module isn't available
    pass

__all__ = [
    "UnifiedDigitalAnalytics",
    "SocialMediaAnalytics", 
    "GoogleAnalyticsIntegration",
    "AttributionModel"
]
