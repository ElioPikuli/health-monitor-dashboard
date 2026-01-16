#!/bin/bash
source .venv/bin/activate
python monitor.py &
streamlit run dashboard.py
