# Tazama Fraud Detection System

A comprehensive fraud detection system built with Tazama, featuring a full-stack Docker deployment and an API client interface.

## Quick Start

### 1. Start the Full Stack Docker Environment

Navigate to the Full-Stack-Docker-Tazama directory and start all services:

```bash
cd Full-Stack-Docker-Tazama
docker-compose up
```

This will start all the required Tazama services including:
- Database services (PostgreSQL, Redis, ArangoDB)
- NATS messaging
- Transaction Processing services
- Rule processors

### 2. Run the Tazama API Client

Once the Docker services are running, start the API client:

```bash
cd tazama_api_client
./start.sh
```

The API client will be available at `http://localhost:5000`

## Project Structure

```
tazama/
├── Full-Stack-Docker-Tazama/    # Docker compose setup for all Tazama services
├── tazama_api_client/           # Flask-based API client and web interface
└── tazama-local-db/             # Local database setup for development
```

## Requirements

- Docker and Docker Compose
- Python 3.8+
- Bash shell (for running start.sh)

## Additional Information

For more detailed configuration and troubleshooting, please refer to the documentation in each subdirectory.
