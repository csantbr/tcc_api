# Gemini Code Assistant Context

## Project Overview

This project is a Python-based backend API for a programming contest judging system. It allows users to submit solutions to programming problems, which are then evaluated by a dedicated "judge" service.

**Key Technologies:**

*   **Backend:** Python with the FastAPI framework.
*   **Database:** MongoDB for storing data related to users, problems, and submissions.
*   **Task Queue:** Celery with a Redis broker to manage the asynchronous judging of submissions.
*   **Containerization:** Docker and Docker Compose are used to orchestrate the different services (API, worker, judge, and database).
*   **Dependency Management:** Poetry is used for managing Python dependencies.

**Architecture:**

The system is composed of four main services:

*   `api`: The main FastAPI application that exposes the RESTful API endpoints.
*   `worker`: A Celery worker that consumes submission tasks from the Redis queue.
*   `judge`: A dedicated service that executes the submitted code in a sandboxed environment and evaluates the output. This service is built from `Dockerfile.judge` and includes runtimes for various programming languages.
*   `mongo`: A MongoDB instance for data persistence.

## Building and Running

### Initial Setup

1.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2.  **Install dependencies using Poetry:**
    ```bash
    pip install poetry
    poetry install
    ```

### Running the Application

*   **Start all services with Docker Compose:**
    ```bash
    docker-compose up -d --build
    ```
    The API will be available at `http://127.0.0.1:8000/docs#/`.

### Testing and Linting

*   **Run the linter:**
    ```bash
    make lint
    ```
    This project uses `ruff` for linting.

*   **Stress Testing:**
    The `k6_testing` directory contains a basic stress test setup using k6.

## Development Conventions

*   **Code Style:** The project uses `ruff` for linting and formatting. The `Makefile` provides a `lint` command to enforce the style.
*   **Configuration:** Application configuration is managed using `pydantic-settings` and is loaded from a `local.env` file. The main configuration is in `src/config.py`.
*   **Modularity:** The application is well-structured, with clear separation of concerns. Routers are defined in `src/routers.py` and are dynamically loaded by the main application in `src/app.py`. Each feature (e.g., `users`, `problems`, `submissions`) has its own dedicated module with controllers, models, and repositories.
*   **Typing:** The codebase uses Python type hints extensively.
*   **Authentication:** The API uses a JWT token for authentication. The `README.md` file provides instructions on how to generate a token for testing purposes. The master API key is defined in the `.env` file.
