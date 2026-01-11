# Riot Integration Service

Riot Integration Service is a backend service built with **FastAPI** that integrates **Riot Games APIs** to retrieve and persist player and match data.

The project is designed as a **data ingestion backend** and can be used as a reference implementation for:
- API integration
- backend service design
- database persistence with migrations
- microservice-oriented architecture

---

## Features

- Lookup players by Riot ID (`gameName` + `tagLine`)
- Retrieve match history by **PUUID**
- Persist matches and participants into **PostgreSQL**
- Idempotent data import to avoid duplicates
- Schema evolution managed through **Alembic migrations**

---

## Tech Stack

- **Python**, **FastAPI**
- **PostgreSQL**
- **SQLAlchemy ORM**
- **Alembic** (database migrations)
- **httpx** (HTTP client for Riot APIs)

---

## Architecture Overview

The service exposes REST endpoints that:
1. Fetch data from Riot Games APIs  
2. Map external API responses to internal domain models  
3. Persist normalized data into a relational database  

The project follows a modular structure to keep API, database models, and service logic clearly separated.

---

## Why this project

This project was developed as a **personal backend project** to:
- practice real-world API integration
- work with relational data modeling
- manage schema changes safely over time
- design a maintainable backend service using modern Python tools

---

## Local Setup

> Requirements: Python 3.10+, PostgreSQL

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies
4. Configure environment variables
5. Run database migrations with Alembic
6. Start the FastAPI application

---

## Notes

This project is intended as a **learning and portfolio project** and not as a production-ready service.
