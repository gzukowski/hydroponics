# HydroAPI

HydroAPI is a Django-based API for managing hydroponic systems and their measurements. This project is developed as part of a recruitment task.


## Table of Contents

- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [Generate Django Secret Key](#generate-django-secret-key)
  - [Create and Fill .env File](#create-and-fill-env-file)
  - [Build and Run with Docker](#build-and-run-with-docker)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)

## Prerequisites

Ensure you have the following installed on your machine:

- [Docker](https://www.docker.com/get-started)

## Setup

### Generate Django Secret Key

Run the following Python code to generate a new secret key:

```python
import secrets

print(secrets.token_urlsafe(50))
```

Copy the generated secret key for later use.

### Create and Fill .env File

Create a file named `.env` in the root directory of your project and add the following contents:

```env
SECRET=
DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=
DB_PORT=
```

Replace fields with your credentials.

### Build and Run with Docker

1. **Build the Docker image:**

   ```bash
   docker-compose build
   ```

2. **Start the Docker containers:**

   ```bash
   docker-compose up
   ```
3. **Create superuser to access /admin panel:**
    Access the backend container console and run
   ```bash
   python manage.py createsuperuser
   ```
Your Django project should now be running on `http://localhost:8000`.

## Usage

To interact with the API, you can use tools like [Postman](https://www.postman.com/), `curl` or some designed frontend.

### API Endpoints

- **Register:** `POST /api/auth/register/`
- **Login:** `POST /api/auth/login/`
- **Create Hydroponic System:** `POST /api/hydro/`
- **Get Hydroponic Systems:** `GET /api/hydro/`
- **Update Hydroponic System:** `PUT /api/hydro/{id}/`
- **Delete Hydroponic System:** `DELETE /api/hydro/{id}/`
- **Create Measurement:** `POST /api/hydro/{id}/measurements/`
- **Get Measurements:** `GET /api/hydro/{id}/measurements/`

Refer to the [API Documentation](#api-endpoints) for detailed information on request and response formats.

### Additional Notes:

- Ensure that your `Dockerfile` and `docker-compose.yml` are correctly configured to use the `.env` variables.
- You might want to add more environment variables depending on your project's requirements (e.g., database settings).
- Make sure the `.env` file is listed in your `.gitignore` to avoid exposing sensitive information.