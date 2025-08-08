#!/usr/bin/env python3
"""
Launch script for Movember Impact Dashboard
"""

import subprocess
import time
import signal
import sys
import os
from pathlib import Path

def check_api_running():
    """Check if the API is running."""
    try:
        import requests
        response = requests.get('http://localhost: 8000/health/', timeout=2)
        return response.status_code == 200
    except:
        return False

def start_api():
    """Start the API server."""
    print("🚀 Starting Movember AI Rules API...")
    api_process = subprocess.Popen(['python', 'simple_api.py'],
                                  stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)
    time.sleep(3)  # Wait for API to start
    return api_process

def start_frontend():
    """Start the frontend server."""
    print("🌐 Starting frontend server...")
    frontend_dir = Path('frontend')
    if not frontend_dir.exists():
        print("❌ Frontend directory not found!")
        return None

    os.chdir('frontend')
    frontend_process = subprocess.Popen(['python', '-m', 'http.server', '3000'],
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE)
    os.chdir('..')
    time.sleep(2)  # Wait for frontend to start
    return frontend_process

def main():
    """Main launch function."""
    print("🎯 Movember Impact Dashboard Launcher")
    print("=" * 50)

    # Check if API is already running
    if check_api_running():
        print("✅ API server already running")
        api_process = None
    else:
        api_process = start_api()
        if api_process:
            print("✅ API server started")
        else:
            print("❌ Failed to start API server")
            return

    # Start frontend
    frontend_process = start_frontend()
    if frontend_process:
        print("✅ Frontend server started")
    else:
        print("❌ Failed to start frontend server")
        if api_process:
            api_process.terminate()
        return

    print("\n🎉 Dashboard is ready!")
    print("📊 API: http://localhost: 8000")
    print("🌐 Dashboard: http://localhost: 3000")
    print("\n📋 Available endpoints:")
    print("   • /impact/global/ - Global impact data")
    print("   • /impact/executive-summary/ - Executive summary")
    print("   • /impact/dashboard/ - Dashboard data")
    print("   • /impact/category/{category}/ - Category-specific data")
    print("\n⏹️  Press Ctrl+C to stop all servers")

    try:
        # Keep the script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        if api_process:
            api_process.terminate()
        if frontend_process:
            frontend_process.terminate()
        print("✅ Servers stopped")

if __name__ == "__main__":
    main()
