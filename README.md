# Distributed System Health Dashboard 🛡️

![Dashboard Screenshot](<img width="1814" height="804" alt="image" src="https://github.com/user-attachments/assets/9caa27fa-177a-4124-8ba1-c61e97cc41ad" />
)

## Project Overview

The **Distributed System Health Dashboard** is a robust, Python-based monitoring solution designed to track the uptime and performance of distributed web services. It consists of a data collector that periodically pings target URLs and a real-time web dashboard that visualizes latency trends and service availability.

This project demonstrates a microservices-like architecture where data collection and data visualization are decoupled processes, communicating via a shared persistent storage layer.

## Architecture

The system is containerized using **Docker Compose** and consists of two main services:

1.  **Monitor Service (`monitor.py`)**: A background worker that pings a configurable list of websites every 60 seconds. It logs timestamp, status code, and latency (ms) into a SQLite database.
2.  **Dashboard Service (`dashboard.py`)**: A Streamlit web application that queries the database to display real-time Key Performance Indicators (KPIs) and historical latency charts.

**Data Persistence**: A shared Docker Volume (`db_data`) is used to persist the SQLite database (`health_monitor.db`), ensuring that data remains intact even if containers are restarted, and allowing both services to access the same data source simultaneously.

## Tech Stack

*   **Language**: Python 3.11+
*   **Visualization**: Streamlit
*   **Data Analysis**: Pandas
*   **Database**: SQLite
*   **Containerization**: Docker & Docker Compose
*   **Scheduling**: `schedule` library

## How to Run Locally

### Prerequisites
*   Docker and Docker Compose installed on your machine.

### Steps

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/your-username/distributed-health-dashboard.git
    cd distributed-health-dashboard
    ```

2.  **Start the Services**
    Run the following command to build and start the containers in the background:
    ```bash
    docker-compose up --build -d
    ```

3.  **Access the Dashboard**
    Open your browser and navigate to:
    [http://localhost:8501](http://localhost:8501)

4.  **Stop the Services**
    To shut down the application:
    ```bash
    docker-compose down
    ```

## Development (Non-Docker)

If you prefer to run the scripts directly without Docker:

1.  Create a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Run the application using the helper script:
    ```bash
    ./run_app.sh
    ```
