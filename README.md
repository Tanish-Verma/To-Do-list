# Telegram To-Do List Bot

A clean, async, and persistent **Telegram To-Do List Bot** built using **python-telegram-bot v20+** and **SQLite (aiosqlite)**.
Each user gets their own private task list with interactive buttons for a smooth UX.

---

## Features

### Core Functionality

* Add tasks using `/add`
* View pending tasks using `/list`
* Mark tasks as completed using **inline buttons** (`/done`)
* Clear all tasks with confirmation (`/clear`)
* Built-in `/help` command

### Safety & UX

* Tasks are **user-specific** (no data leakage)
* Confirmation before destructive actions
* Handles invalid callbacks gracefully

### Persistence

* Uses **SQLite** via `aiosqlite`
* Tasks persist across restarts
* Tracks creation time and completion state

### Deployment Ready

* Async-first architecture
* Supports **Polling** and **Webhook** modes
* Works with **Docker** and platforms like **Render**, **Railway**, **PythonAnywhere**

---

## Tech Stack

* **Python 3.10+**
* **python-telegram-bot (v20+)**
* **aiosqlite**
* **SQLite**
* **dotenv** (for local development)
* **Docker / Docker Compose**

---

## Project Structure

```
ToDoList/
│
├── main.py          # Bot entry point
├── methods.py       # Telegram command & callback handlers
├── db.py            # Database logic (SQLite)
├── tasks.db         # SQLite database (auto-created)
├── roadmap.md       # Planned future features
├── README.md
├── Dockerfile
├── docker-compose.yml
├── .dockerignore
└── .env             # Environment variables 
```

---

## Setup Instructions (Without Docker)

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd ToDoList
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\\Scripts\\activate     # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Variables

Create a `.env` file:

```env
BOT_TOKEN=your_telegram_bot_token
```

For webhook deployment:

```env
WEBHOOK_URL=https://your-app-domain
PORT=8000
```

---

## ▶ Running the Bot (Without Docker)

### Polling (Local Development)

```bash
python main.py
```

### Webhook (Production)

* Uses `Application.run_webhook()`
* Requires a public HTTPS URL

---

## 🐳 Running with Docker (Recommended)

Docker provides a clean, reproducible environment and is recommended for deployment.

### Prerequisites

* Docker
* Docker Compose (v2+)

---

### 1. Create `.env` File

```env
BOT_TOKEN=your_telegram_bot_token
WEBHOOK_URL=https://your-app-domain
PORT=8000
```

> ⚠️ `.env` is required at runtime and **must not be committed**.

---

### 2. Build and Run with Docker Compose

From the project root:

```bash
docker compose up --build
```

This will:

* Build the Docker image
* Start the bot container
* Inject environment variables securely

---

### 3. Stop the Bot

```bash
docker compose down
```

---

### 4. Database Persistence (Important)

The SQLite database is persisted using a bind mount:

```yaml
volumes:
  - ./tasks.db:/app/tasks.db
```

This ensures:

* Tasks persist across restarts
* Data is not lost when containers are recreated

---

## Commands

| Command       | Description              |
| ------------- | ------------------------ |
| `/start`      | Start the bot            |
| `/help`       | Show help message        |
| `/add <task>` | Add a new task           |
| `/list`       | List pending tasks       |
| `/done`       | Mark a task as completed |
| `/clear`      | Delete all tasks         |

---

## Design Decisions

* **Inline keyboards** instead of numeric IDs → better UX
* **SQLite** for simplicity and portability
* **Async DB access** to avoid blocking the event loop
* **Docker volumes** for database persistence
* **Runtime secrets injection** (no secrets in images)

---

## Future Enhancements

Planned features are documented in [`roadmap.md`](roadmap.md), including:

* Due dates & reminders
* Task priorities
* Categories / tags
* Bulk delete

---

## License

MIT License — free to use, modify, and distribute.

---

## Acknowledgements

* [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
* Telegram Bot API
