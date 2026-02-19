# Refnode

invitation and referral system built with FastAPI, featuring unique referral codes, tracking, reward distribution, and expiration handling.

## Features

- **Unique Referral Code Generation** - Each user gets a unique, cryptographically secure referral code
- **Track Sign-ups** - Monitor all referrals and their status in real-time
- **Reward Distribution** - Automated reward distribution for successful referrals
- **Expiration Handling** - Configurable expiration periods for referral codes
- **Viral Features** - Track viral coefficient and referral metrics
- **Scalable Architecture** - Built with async FastAPI and PostgreSQL

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Migration**: Alembic
- **Task Queue**: Celery with Redis
- **Authentication**: JWT tokens
- **Testing**: Pytest with async support

## Quick Start

### Prerequisites

- Python 3.9+
- PostgreSQL
- Redis

### Installation

1. Clone the repository:
```bash
git clone https://github.com/afriwondimu/Refnode.git
cd refnode
```
2. Create your venv and install the requirement.txt:
```bash
pip install -r requirements.txt
```
3. Migrate:
```bash
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```
4. Run
```bash
uvicorn app.main:app --reload
```
5. Test by swagger
```bash
http://localhost:8000/docs#/
```