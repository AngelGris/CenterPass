# 🏐 CenterPass – Netball Video Analytics Engine

CenterPass is a computer vision system designed to analyze netball match videos and automatically extract structured game statistics such as:

- Shot attempts & accuracy
- Intercepts
- Player tracking
- Ball possession sequences
- Event detection

The goal of CenterPass is to build an automated netball analytics engine that enables data-driven coaching insights using AI.

---

## 🏗 Architecture

The system is structured into clear layers:

centerpass/
│
├── app/ # FastAPI web layer
├── core/ # Computer vision & event detection logic
├── database/ # SQLAlchemy models & persistence layer
├── alembic/ # Database migrations
├── dashboard/ # (Future) Frontend analytics UI


### Key Technologies

- **FastAPI** – REST API layer
- **PostgreSQL** – Persistent storage
- **SQLAlchemy + Alembic** – ORM & migrations
- **OpenCV** – Frame extraction & vision processing
- **uv** – Dependency management
- **Docker** – Local database environment
