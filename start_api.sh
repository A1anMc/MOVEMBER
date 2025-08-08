#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python -m uvicorn api.movember_api:app --host 0.0.0.0 --port 8000 --reload 