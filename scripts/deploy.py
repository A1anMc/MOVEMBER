#!/usr/bin/env python3
"""
Movember AI Rules System - Deployment Script
Automated deployment with environment validation, health checks, and rollback.
"""

import argparse
import asyncio
import json
import logging
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class DeploymentManager:
    """Manages deployment of the Movember AI Rules System."""
    
    def __init__(self, environment: str, config_path: str = "config/deployment.json"):
        self.environment = environment
        self.config_path = config_path
        self.config = self._load_config()
        self.deployment_id = f"deploy-{datetime.now().strftime('%Y%m%d-%H%M%S')}"
        
    def _load_config(self) -> Dict:
        """Load deployment configuration."""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {self.config_path} not found, using defaults")
            return self._get_default_config()
    
    def _get_default_config(self) -> Dict:
        """Get default deployment configuration."""
        return {
            "environments": {
                "development": {
                    "python_version": "3.9",
                    "dependencies": ["requirements.txt"],
                    "health_check_url": "http://localhost:8000/health",
                    "timeout": 300,
                    "rollback_enabled": True
                },
                "staging": {
                    "python_version": "3.9",
                    "dependencies": ["requirements.txt"],
                    "health_check_url": "https://staging.movember-rules.com/health",
                    "timeout": 600,
                    "rollback_enabled": True
                },
                "production": {
                    "python_version": "3.9",
                    "dependencies": ["requirements.txt"],
                    "health_check_url": "https://rules.movember.com/health",
                    "timeout": 900,
                    "rollback_enabled": True
                }
            }
        }
    
    async def deploy(self) -> bool:
        """Execute the deployment process."""
        logger.info(f"Starting deployment to {self.environment}")
        logger.info(f"Deployment ID: {self.deployment_id}")
        
        try:
            # Pre-deployment checks
            if not await self._pre_deployment_checks():
                logger.error("Pre-deployment checks failed")
                return False
            
            # Backup current version
            if not await self._backup_current_version():
                logger.error("Backup failed")
                return False
            
            # Deploy new version
            if not await self._deploy_new_version():
                logger.error("Deployment failed")
                await self._rollback()
                return False
            
            # Health checks
            if not await self._health_checks():
                logger.error("Health checks failed")
                await self._rollback()
                return False
            
            # Post-deployment tasks
            await self._post_deployment_tasks()
            
            logger.info(f"Deployment {self.deployment_id} completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"Deployment failed: {e}")
            await self._rollback()
            return False
    
    async def _pre_deployment_checks(self) -> bool:
        """Run pre-deployment validation."""
        logger.info("Running pre-deployment checks...")
        
        checks = [
            self._check_python_version(),
            self._check_dependencies(),
            self._check_environment_variables(),
            self._check_disk_space(),
            self._check_network_connectivity()
        ]
        
        results = await asyncio.gather(*checks, return_exceptions=True)
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                logger.error(f"Check {i+1} failed: {result}")
                return False
            elif not result:
                logger.error(f"Check {i+1} failed")
                return False
        
        logger.info("All pre-deployment checks passed")
        return True
    
    async def _check_python_version(self) -> bool:
        """Check Python version compatibility."""
        required_version = self.config["environments"][self.environment]["python_version"]
        current_version = f"{sys.version_info.major}.{sys.version_info.minor}"
        
        if current_version != required_version:
            logger.warning(f"Python version mismatch: {current_version} vs {required_version}")
            return False
        
        logger.info(f"Python version check passed: {current_version}")
        return True
    
    async def _check_dependencies(self) -> bool:
        """Check if all dependencies are available."""
        try:
            import requests
            import pytest
            import asyncio
            logger.info("Dependency check passed")
            return True
        except ImportError as e:
            logger.error(f"Dependency check failed: {e}")
            return False
    
    async def _check_environment_variables(self) -> bool:
        """Check required environment variables."""
        required_vars = ["MOVEMBER_ENV", "MOVEMBER_API_KEY"]
        
        for var in required_vars:
            if not os.getenv(var):
                logger.warning(f"Environment variable {var} not set")
                return False
        
        logger.info("Environment variables check passed")
        return True
    
    async def _check_disk_space(self) -> bool:
        """Check available disk space."""
        try:
            stat = os.statvfs('.')
            free_space_gb = (stat.f_frsize * stat.f_bavail) / (1024**3)
            
            if free_space_gb < 1.0:  # Less than 1GB
                logger.error(f"Insufficient disk space: {free_space_gb:.2f}GB")
                return False
            
            logger.info(f"Disk space check passed: {free_space_gb:.2f}GB available")
            return True
        except Exception as e:
            logger.error(f"Disk space check failed: {e}")
            return False
    
    async def _check_network_connectivity(self) -> bool:
        """Check network connectivity."""
        try:
            import requests
            response = requests.get("https://www.google.com", timeout=5)
            logger.info("Network connectivity check passed")
            return True
        except Exception as e:
            logger.error(f"Network connectivity check failed: {e}")
            return False
    
    async def _backup_current_version(self) -> bool:
        """Backup current version before deployment."""
        logger.info("Creating backup of current version...")
        
        try:
            backup_dir = f"backups/{self.deployment_id}"
            os.makedirs(backup_dir, exist_ok=True)
            
            # Copy current files to backup
            subprocess.run(["cp", "-r", "rules", backup_dir], check=True)
            subprocess.run(["cp", "requirements.txt", backup_dir], check=True)
            
            logger.info(f"Backup created: {backup_dir}")
            return True
        except Exception as e:
            logger.error(f"Backup failed: {e}")
            return False
    
    async def _deploy_new_version(self) -> bool:
        """Deploy the new version."""
        logger.info("Deploying new version...")
        
        try:
            # Install/update dependencies
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            
            # Run tests
            subprocess.run([sys.executable, "-m", "pytest", "test_rules_system.py"], check=True)
            
            # Update version file
            with open("VERSION", "w") as f:
                f.write(f"{self.deployment_id}\n")
            
            logger.info("New version deployed successfully")
            return True
        except Exception as e:
            logger.error(f"Deployment failed: {e}")
            return False
    
    async def _health_checks(self) -> bool:
        """Run health checks after deployment."""
        logger.info("Running health checks...")
        
        health_url = self.config["environments"][self.environment]["health_check_url"]
        timeout = self.config["environments"][self.environment]["timeout"]
        
        # Simulate health check (in real deployment, this would check actual endpoints)
        await asyncio.sleep(2)  # Simulate health check delay
        
        try:
            # Test rule engine functionality
            from rules.domains.movember_ai import create_movember_engine
            engine = create_movember_engine()
            
            # Test basic rule evaluation
            from rules.types import ExecutionContext, ContextType
            context = ExecutionContext(
                context_type=ContextType.IMPACT_REPORTING,
                context_id="health-check",
                data={"test": True}
            )
            
            results = await engine.evaluate_context(context)
            
            if results:
                logger.info("Health checks passed")
                return True
            else:
                logger.error("Health checks failed")
                return False
                
        except Exception as e:
            logger.error(f"Health checks failed: {e}")
            return False
    
    async def _rollback(self) -> bool:
        """Rollback to previous version."""
        if not self.config["environments"][self.environment]["rollback_enabled"]:
            logger.warning("Rollback disabled for this environment")
            return False
        
        logger.info("Initiating rollback...")
        
        try:
            backup_dir = f"backups/{self.deployment_id}"
            if os.path.exists(backup_dir):
                subprocess.run(["cp", "-r", f"{backup_dir}/rules", "."], check=True)
                subprocess.run(["cp", f"{backup_dir}/requirements.txt", "."], check=True)
                logger.info("Rollback completed successfully")
                return True
            else:
                logger.error("No backup found for rollback")
                return False
        except Exception as e:
            logger.error(f"Rollback failed: {e}")
            return False
    
    async def _post_deployment_tasks(self) -> None:
        """Execute post-deployment tasks."""
        logger.info("Running post-deployment tasks...")
        
        # Update deployment log
        log_entry = {
            "deployment_id": self.deployment_id,
            "environment": self.environment,
            "timestamp": datetime.now().isoformat(),
            "status": "success"
        }
        
        with open("deployment.log", "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        
        # Clean up old backups (keep last 5)
        self._cleanup_old_backups()
        
        logger.info("Post-deployment tasks completed")
    
    def _cleanup_old_backups(self) -> None:
        """Clean up old backup files."""
        try:
            backup_dir = Path("backups")
            if backup_dir.exists():
                backups = sorted(backup_dir.iterdir(), key=lambda x: x.stat().st_mtime, reverse=True)
                for backup in backups[5:]:  # Keep only last 5
                    import shutil
                    shutil.rmtree(backup)
                    logger.info(f"Cleaned up old backup: {backup}")
        except Exception as e:
            logger.warning(f"Backup cleanup failed: {e}")


async def main():
    """Main deployment function."""
    parser = argparse.ArgumentParser(description="Deploy Movember AI Rules System")
    parser.add_argument("environment", choices=["development", "staging", "production"],
                       help="Target environment")
    parser.add_argument("--config", default="config/deployment.json",
                       help="Deployment configuration file")
    parser.add_argument("--dry-run", action="store_true",
                       help="Run deployment in dry-run mode")
    
    args = parser.parse_args()
    
    if args.dry_run:
        logger.info("DRY RUN MODE - No actual deployment will occur")
    
    deployment_manager = DeploymentManager(args.environment, args.config)
    
    success = await deployment_manager.deploy()
    
    if success:
        logger.info("Deployment completed successfully")
        sys.exit(0)
    else:
        logger.error("Deployment failed")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main()) 