<div align="center">

# 🚀 SFM_BACKEND

*Empowering seamless connections for innovative solutions.*

![last-commit](https://img.shields.io/github/last-commit/qminh011002/SFM_BackEnd?style=flat&logo=git&logoColor=white&color=0080ff)
![repo-top-language](https://img.shields.io/github/languages/top/qminh011002/SFM_BackEnd?style=flat&color=0080ff)
![repo-language-count](https://img.shields.io/github/languages/count/qminh011002/SFM_BackEnd?style=flat&color=0080ff)

*Built with the tools and technologies:*

![Markdown](https://img.shields.io/badge/Markdown-000000.svg?style=flat&logo=Markdown&logoColor=white)
![GNU%20Bash](https://img.shields.io/badge/GNU%20Bash-4EAA25.svg?style=flat&logo=GNU-Bash&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688.svg?style=flat&logo=FastAPI&logoColor=white)
![Pytest](https://img.shields.io/badge/Pytest-0A9EDC.svg?style=flat&logo=Pytest&logoColor=white)
![ReadMe](https://img.shields.io/badge/ReadMe-018EF5.svg?style=flat&logo=ReadMe&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB.svg?style=flat&logo=Python&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-E92063.svg?style=flat&logo=Pydantic&logoColor=white)

</div>

---

## 📚 Table of Contents

- [🧩 Overview](#overview)
- [🛠️ Getting Started](#getting-started)
  - [📌 Prerequisites](#prerequisites)
  - [⚙️ Installation](#installation)
  - [🚦 Usage](#usage)
  - [✅ Testing](#testing)
- [🏛️ Clean Architecture](#clean-architecture)

---

## 🧩 Overview

**SFM_BackEnd** is a modern backend framework built with **FastAPI** and aligned with **Clean Architecture** principles. It emphasizes scalability, maintainability, and modularity in building backend systems.

### 🔍 Why SFM_BackEnd?

This project simplifies backend development with a strong focus on:

- 🛠️ **Dependency Management**: Stable environments through pinned package versions.
- 📡 **Modular API Structure**: Organized endpoints for handling user roles, production workflows, etc.
- 📊 **DTOs (Data Transfer Objects)**: Clean, validated request and response models using Pydantic.
- 🔄 **Database Migration**: Alembic integration for version-controlled schema updates.
- 🔒 **Security**: JWT authentication and role-based access control.
- 🧼 **Clean Architecture**: Clear separation of domain logic and infrastructure code.

---

## 🛠️ Getting Started

### 📌 Prerequisites

Ensure you have the following installed:

- **Python 3.9+**
- **Pip**

### ⚙️ Installation

```bash
# Clone the repository
git clone https://github.com/qminh011002/SFM_BackEnd

# Navigate into the project
cd SFM_BackEnd

# Install dependencies
pip install -r requirements.txt
```

### 🚦 Usage

To run the application:

```bash
python main.py
```

Replace `main.py` if your actual entrypoint differs.

### ✅ Testing

To run the test suite using Pytest:

```bash
pytest
```

---

## 🏛️ Clean Architecture

This project follows **Clean Architecture** to ensure a scalable and testable codebase.

### 🧱 Directory Structure

```
SFM_BACKEND/
├── app/
│   ├── alembic/          # Alembic migration scripts
│   ├── application/      # Use cases and business workflows
│   ├── core/             # Shared configs and utility constants
│   ├── domain/           # Entities and domain logic
│   ├── infrastructure/   # External services, DB implementations
│   └── presentation/     # API endpoints, controllers, schemas
├── .env                  # Environment variables
├── alembic.ini           # Alembic configuration
├── main.py               # Application entrypoint
├── commit-each.sh        # Dev script for streamlined commits
├── requirements.txt      # Dependency list
├── README.md             # Project documentation
└── .gitignore            # Git ignore rules
```

> 🧠 **Note**: This structure enforces separation of concerns, improving testability and adaptability over time.

---

[⬆ Return to Top](#top)

---
