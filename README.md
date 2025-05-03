# Internal AI Assistant

This system is designed to help product and engineering teams quickly extract insights from internal documents and team reports—particularly those containing product bugs and user feedback.

## Installation

### Prerequisites
* Docker and Docker Compose (for containerized deployment)
* Python >= 3.12

```bash
# Create environment variables file from template
cp .env.example .env
# Edit the .env file with your configuration
```

### Docker compose deployment
For a complete containerized deployment of all components:

```bash
# Build and start all services
docker compose up -d
```

The development server will be available at http://localhost:8000

## How to use

```bash
# Listing application
curl -X 'GET' \
  'http://localhost:8000/list-apps' \
  -H 'accept: application/json'

# response [
#   "assistants",
#   "data"
# ]
```

```bash
# Create session 
curl -X 'POST' \
  'http://localhost:8000/apps/assistants/users/YOUR_USER_HERE/sessions' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "additionalProp1": {}
}'
# response {
#   "id": "86f9c3ab-3ef0-4392-ad3f-e218278736d9",
#   "app_name": "assistants",
#   "user_id": "YOUR_USER_HERE",
#   "state": {
#     "additionalProp1": {}
#   },
#   "events": [],
#   "last_update_time": 1746286390.0858347
# }
```

```bash
# chat
curl -X 'POST' \
  'http://localhost:8000/run_sse' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "app_name": "assistants",
  "user_id": "YOUR_USER_HERE",
  "session_id": "86f9c3ab-3ef0-4392-ad3f-e218278736d9",
  "new_message": {
    "parts": [
      {
        "text": "hello there."
      }
    ],
    "role": "user"
  },
  "streaming": false
}'

```

view http://localhost:8000/docs for more information 