# Image-to-Speech Web App

Study project: upload an image with a handwritten digit (`0-9`) and get spoken audio of the detected number.

## Architecture

The system has 4 microservices:

1. **simple-frontend**  
   Static HTML UI served by Nginx (`http://localhost:8080`).
2. **facade-api**  
   Main API used by the frontend. Receives image + language and orchestrates downstream services.
3. **image-to-text**  
   TensorFlow-based digit classifier. Returns a detected number from the uploaded image.
4. **translate-api**  
   Converts the detected number to speech (MP3) using Google Text-to-Speech.

There is also a **tensor** folder used for model training artifacts.

## Request Flow (How it Works)

1. User uploads an image in the frontend.
2. Frontend sends the file to `facade-api` (`POST /image-to-audio/`).
3. `facade-api` sends the image to `image-to-text` (`POST /predict`) and receives a predicted digit.
4. `facade-api` calls `translate-api` (`GET /generate_audio`) with the predicted digit + selected language.
5. `facade-api` returns MP3 audio to the frontend.
6. Frontend plays the generated audio.

## Local Setup (Docker Compose) — Recommended

### Prerequisites

- Docker Desktop installed and running
- Docker Compose available (`docker compose version`)

### Start

Run from repository root:

```bash
docker compose up --build
```

### Service Endpoints

```text
Frontend:      http://localhost:8080
Facade API:    http://localhost:3004
Image-to-text: http://localhost:3001
Translate API: http://localhost:3002
```

### Stop

```bash
docker compose down
```

### Rebuild from scratch (optional)

If you changed dependencies or Dockerfiles:

```bash
docker compose down
docker compose build --no-cache
docker compose up
```

## Usage

1. Open `http://localhost:8080`
2. Select an image file (`.jpg`, `.jpeg`, `.png`) with a clear handwritten digit
3. Select language (`en`, `es`, `fr`)
4. Click **Convert**
5. Play the returned audio in the player

## Troubleshooting

- **Command typo issue**  
  Use a single command:
  ```bash
  docker compose up --build
  ```
  (not `docker compose up --builddocker compose up --build`)

- **Port already in use**  
  Stop the process using that port, or change port mapping in `docker-compose.yml`.

- **Containers started but app not responding**  
  Check logs:
  ```bash
  docker compose logs -f
  ```

- **Need clean restart**  
  ```bash
  docker compose down -v
  docker compose up --build
  ```

## Kubernetes/Minikube (Alternative)

This repository also includes Kubernetes manifests and a deployment script:

```bash
minikube config set driver docker
minikube start --cpus max
./deploy-projects.sh
```