<div align="center">
   <img src="public/warj_banner2.png" width="850" alt="Banner API5">

   # API5BD2026 - Backend
   
   [![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
   [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
   [![Checked with mypy](https://www.mypy-lang.org/static/mypy_badge.svg)](https://mypy-lang.org/)
   [![Husky](https://img.shields.io/badge/Husky-64b5f6?style=flat&logo=dog&logoColor=white)](https://typicode.github.io/husky/)
   [![SonarCloud Quality Gate](https://img.shields.io/sonar/quality_gate/Warj-Group_API5BD2026Backend?server=https%3A%2F%2Fsonarcloud.io&logo=sonarcloud&style=flat)](https://sonarcloud.io/summary/new_code?id=Warj-Group_API5BD2026Backend)
</div>

<br>

## Initial Configuration

It is required to use:

**Python 3.11**, download: [official Python website](https://www.python.org/downloads/release/python-3110/).

**Node.js 22.22.0**, download: [official Node.js Website](https://nodejs.org/en/blog/release/v22.22.0).

**Docker**, download: [official Docker website](https://www.docker.com/get-started/).

<br>

## Environment Setup

Clone the repository to your local environment and use your preferred IDE:

```bash
git clone https://github.com/Warj-Group/API5BD2026Backend.git
cd API5BD2026Backend
```

### Virtual Environment (venv)
Create and activate the virtual environment before installing any dependencies.

* **Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

* **Linux/Mac/Git Bash:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Setup Script
With the virtual environment activated, run the automation script to install the dependencies from `requirements.txt` and configure Husky hooks (pre-commit and branch validation):

* **Windows:** `setup_backend.bat`
* **Linux/Mac/Git Bash:** `bash setup_backend.sh`

### Execution
To run the backend, you need to start the database container and then run the application using Uvicorn.

* **Windows:**
```bash
# Start Docker Compose
> docker compose up -d

# Wait for database to be ready
echo Waiting for database to be ready...
timeout /t 10 /nobreak > nul

# Run the backend
> python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Or you can run the `run.bat` script in the project root directory.


* **Linux/Mac/Git Bash:**
```bash
# Start Docker Compose
docker compose up -d

# Wait for database to be ready
echo "Waiting for database to be ready..."
sleep 10

# Run the backend
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```
Or you can run the `run.sh` script in the project root directory.

Accessing backend tools:

- Endpoints: localhost:8000/docs
- Backend JSON: localhost:8000

<br> 

## Development and Quality

During development, to maintain code quality and best practices, we use specific tools for linting, formatting, and type checking.

### 1. Ruff: Linter and Imports (Find logical errors)
It looks for unused variables, duplicate imports, syntax errors, etc.
* **Check only:** `ruff check .`
* **Fix automatically (Recommended):** `ruff check --fix .`

### 2. Ruff: Formatter (Beautify the code)
It fixes spaces, line breaks, and quotes to match the official standard.
* **Check only (used in CI):** `ruff format --check .`
* **Format automatically (Recommended):** `ruff format .`

### 3. Mypy: Type Checking
It reads your code looking for typing errors (e.g., you specified a function receives an `int`, but you are passing a `string`). Mypy does not fix it automatically; it only warns you where to fix it.
* **Check:** `mypy .`

<br>

## Contribution Guidelines

To ensure traceability between YouTrack tasks and GitHub commits, strictly follow the standards below:

### 1. Commit Messages
Messages must use the task ID for automatic integration with YouTrack:
* **Format:** `{type}/{yt_id}: Description`
* **Example:** `feat/WARJ-1: implement user authentication`

### 2. Branch Naming Convention
Create working branches linked to the sprint cards:
* **Format:** `{type}/{yt_id}-brief-description`
* **Example:** `feature/WARJ-1-user-authentication`

### 3. Automatic Validation
The project uses Husky and Commitlint. If the commit standard or linting rules are not followed, the submission (push/commit) will be blocked by the terminal with the appropriate correction instructions.

<br>

## Additional Documentation
For details on the group's architecture, CI/CD, and design patterns, access our Wiki: [WARJ-GROUP - Wiki Documentation](https://github.com/Warj-Group/API5BD2026Main/wiki)
