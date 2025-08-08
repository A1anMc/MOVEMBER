#!/usr/bin/env python3
"""
API Stability Fix
Identifies and fixes common API stability issues.
"""

import os
import sys
import subprocess
import time
import psutil
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class APIStabilityFixer:


    """Fixes common API stability issues."""

    def __init__(self):


        self.port = 8001
        self.process_name = "uvicorn"
        self.api_module = "api.movember_api:app"

    def check_port_availability(self) -> bool:


        """Check if port 8001 is available."""
        try:
            import socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            result = sock.connect_ex(('localhost', self.port))
            sock.close()
            return result != 0
        except Exception as e:
            logger.error(f"Error checking port availability: {e}")
            return False

    def kill_existing_processes(self) -> bool:


        """Kill any existing uvicorn processes on port 8001."""
        try:
            # Find processes using port 8001
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    if proc.info['cmdline'] and any('8001' in arg for arg in proc.info['cmdline']):
                        logger.info(f"Killing process {proc.info['pid']} using port 8001")
                        proc.terminate()
                        proc.wait(timeout=5)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                    pass

            # Also kill any uvicorn processes
            for proc in psutil.process_iter(['pid', 'name']):
                try:
                    if proc.info['name'] and 'uvicorn' in proc.info['name'].lower():
                        logger.info(f"Killing uvicorn process {proc.info['pid']}")
                        proc.terminate()
                        proc.wait(timeout=5)
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                    pass

            return True
        except Exception as e:
            logger.error(f"Error killing processes: {e}")
            return False

    def start_api_server(self) -> subprocess.Popen:


        """Start the API server with stability optimizations."""
        try:
            # Set environment variables for stability
            env = os.environ.copy()
            env.update({
                'PYTHONPATH': os.getcwd(),
                'PYTHONUNBUFFERED': '1',
                'UVICORN_LOG_LEVEL': 'info'
            })

            # Start the server with optimizations
            cmd = [
                sys.executable, '-m', 'uvicorn',
                self.api_module,
                '--host', '0.0.0.0',
                '--port', str(self.port),
                '--reload',
                '--log-level', 'info',
                '--access-log'
            ]

            logger.info(f"Starting API server: {' '.join(cmd)}")
            process = subprocess.Popen(
                cmd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )

            return process
        except Exception as e:
            logger.error(f"Error starting API server: {e}")
            return None

    def wait_for_server_startup(self, timeout: int = 30) -> bool:


        """Wait for the server to start up."""
        logger.info(f"Waiting for server to start (timeout: {timeout}s)...")

        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                import httpx
                response = httpx.get(f"http://localhost:{self.port}/health/", timeout=5.0)
                if response.status_code == 200:
                    logger.info("✅ Server started successfully!")
                    return True
            except Exception:
                pass

            time.sleep(1)

        logger.error("❌ Server failed to start within timeout")
        return False

    def test_api_stability(self) -> Dict[str, Any]:


        """Test API stability with multiple endpoints."""
        import httpx

        endpoints = [
            "/health/",
            "/data-upload/health/",
            "/real-data/health/",
            "/grant-acquisition/health/",
            "/impact-intelligence/health/",
            "/logo/",
            "/favicon.ico"
        ]

        results = {
            "total_endpoints": len(endpoints),
            "successful": 0,
            "failed": 0,
            "endpoint_results": []
        }

        for endpoint in endpoints:
            try:
                response = httpx.get(f"http://localhost:{self.port}{endpoint}", timeout=10.0)
                success = response.status_code == 200
                results["endpoint_results"].append({
                    "endpoint": endpoint,
                    "status_code": response.status_code,
                    "success": success
                })

                if success:
                    results["successful"] += 1
                else:
                    results["failed"] += 1

            except Exception as e:
                results["endpoint_results"].append({
                    "endpoint": endpoint,
                    "status_code": None,
                    "success": False,
                    "error": str(e)
                })
                results["failed"] += 1

        return results

    def fix_common_issues(self) -> bool:


        """Fix common API stability issues."""
        logger.info("🔧 Fixing common API stability issues...")

        # 1. Kill existing processes
        logger.info("1. Killing existing processes...")
        self.kill_existing_processes()
        time.sleep(2)

        # 2. Check port availability
        logger.info("2. Checking port availability...")
        if not self.check_port_availability():
            logger.warning("Port 8001 is still in use, attempting to free it...")
            self.kill_existing_processes()
            time.sleep(3)

        # 3. Start server with optimizations
        logger.info("3. Starting API server with optimizations...")
        process = self.start_api_server()
        if not process:
            logger.error("Failed to start API server")
            return False

        # 4. Wait for startup
        logger.info("4. Waiting for server startup...")
        if not self.wait_for_server_startup():
            logger.error("Server startup failed")
            process.terminate()
            return False

        # 5. Test stability
        logger.info("5. Testing API stability...")
        results = self.test_api_stability()

        success_rate = (results["successful"] / results["total_endpoints"]) * 100
        logger.info(f"API Stability Test Results:")
        logger.info(f"  - Total endpoints: {results['total_endpoints']}")
        logger.info(f"  - Successful: {results['successful']}")
        logger.info(f"  - Failed: {results['failed']}")
        logger.info(f"  - Success rate: {success_rate:.1f}%")

        if success_rate >= 95:
            logger.info("✅ API stability is good!")
            return True
        else:
            logger.warning("⚠️ API stability needs improvement")
            return False

def main():


    """Main function to fix API stability."""
    print("🔧 Movember API Stability Fixer")
    print("=" * 40)

    fixer = APIStabilityFixer()

    # Check current status
    print("\n📊 Current API Status:")
    try:
        import httpx
        response = httpx.get("http://localhost:8001/health/", timeout=5.0)
        if response.status_code == 200:
            print("✅ API is currently running")
        else:
            print("⚠️ API is running but may have issues")
    except Exception as e:
        print(f"❌ API is not responding: {e}")

    # Run stability fix
    print("\n🔧 Running stability fix...")
    success = fixer.fix_common_issues()

    if success:
        print("\n✅ API stability fix completed successfully!")
        print("🎯 The API should now be stable and responsive.")
    else:
        print("\n❌ API stability fix encountered issues.")
        print("🔍 Please check the logs for more details.")

    print("\n📋 Next Steps:")
    print("1. Test the API endpoints manually")
    print("2. Monitor for any recurring issues")
    print("3. Check system resources if problems persist")

if __name__ == "__main__":
    main()
