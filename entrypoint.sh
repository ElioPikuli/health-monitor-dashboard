#!/bin/bash
# Start the monitor in the background
python monitor.py &

# Start the dashboard in the foreground
# --server.port 8501 tells Streamlit to listen on port 8501
# --server.address 0.0.0.0 tells it to accept connections from outside the container
streamlit run dashboard.py --server.port 8501 --server.address 0.0.0.0
