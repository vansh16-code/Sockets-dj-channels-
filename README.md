# 🧵 Django WebSocket Chat App

A real-time chat application built using **Django**, **Django Channels**, **WebSockets**, **Redis**, and **Docker**.

---

## 🚀 Features

- Real-time chat using WebSockets
- User-based chat messages
- Asynchronous Django Channels
- Redis as a channel layer (message broker)
- Dockerized Redis setup
- Scalable and modular project structure

---

## 📦 Tech Stack

- Django
- Django Channels
- Redis (via Docker)
- WebSockets (ASGI)
- HTML + JavaScript (vanilla for frontend)

---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/django-websocket-chat.git
cd django-websocket-chat

2. Create a Virtual Environment

python -m venv venv
source venv/bin/activate    # On Windows: venv\Scripts\activate

3. Install Dependencies

pip install -r requirements.txt

4. Run Redis Server via Docker

Make sure Docker is installed and running.

docker run -d -p 6379:6379 --name redis-server redis

5. Apply Migrations

python manage.py migrate

6. Run the Django Development Server

python manage.py runserver


---

🌐 Access the App

Open your browser and go to:
http://127.0.0.1:8000/chat/room_name/

Replace room_name with any room you'd like to join or create.


---

🧠 Understanding the Architecture

Django Channels replaces WSGI with ASGI for handling WebSockets.

Redis acts as a channel layer (message broker) to send/receive WebSocket messages between consumers.

Consumers act like Django views for WebSocket connections (e.g., connect, disconnect, receive).

Messages are broadcast to groups (chat rooms).



---

📁 Project Structure (Core Files Only)

chat_project/
├── chat/
│   ├── consumers.py        # WebSocket consumer logic
│   ├── routing.py          # App-level routing
│   └── templates/chat/
│       └── room.html       # Chatroom UI
├── chat_project/
│   ├── asgi.py             # ASGI entry point
│   └── settings.py         # Includes channel layers config
├── requirements.txt
└── Dockerfile (optional)


---

⚙️ Example Channel Layer Configuration (in settings.py)

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}


---

📄 Requirements (requirements.txt)

Django==4.2
channels==4.0.0
channels_redis==4.1.0
daphne==4.0.0


---

🐳 Optional: Add Redis to Docker Compose

Create a docker-compose.yml if you want to automate Redis setup:

version: "3"
services:
  redis:
    image: redis
    ports:
      - "6379:6379"

Run with:

docker-compose up -d


---

📬 Contact

Made with ❤️ by [Your Name].
Feel free to contribute or raise issues!
