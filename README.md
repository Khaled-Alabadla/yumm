# Yumm 🍽️🇵🇸

Yumm is a centralized restaurant exploration and review platform based in Palestine, built using **Python** and **Django**. This repository contains the robust backend architecture, relational database management, and AI integration engines that power the platform.

As a dedicated backend service, this system exposes structured data and business logic optimized for high availability, fast querying (under 2 seconds for AI integrations), and seamless AJAX communications.

---

## 🚀 Key Features (Backend Logic)

- **Role-Based Access Control (RBAC):** Tailored registration and secure workflows for Admins, Restaurant Owners, and Regular Users.
- **Menu & Profile CRUD:** Dynamic data-entry architecture for managing restaurant locations, hours, and categorized menus.
- **Real-time AJAX Support:** Stateless endpoints handling incoming reviews and instantly updating global rating aggregates without page refreshes.
- **AI Smart Recommender:** Integration with LLMs (Gemini/ChatGPT) using contextual prompts to recommend top-3 dining options based on user budget and preferences.
- **AI Review Summarizer:** Automated pipeline that aggregates community feedback to extract structural Pros and Cons for any restaurant.
- **Geospatial Endpoints:** JSON engines feeding exact coordinates to interactive mapping interfaces.

---

## 📂 Project Architecture

The project is structured into modular Django applications to ensure scalability:

```text
├── yumm_core/           # Project configuration settings and URL routing
├── accounts/            # Custom user models, authentication, and permissions
├── restaurants/         # Restaurant registration, approval logic, and menu CRUD
├── reviews/             # Ratings, comments, AJAX endpoints, and notifications
├── ai_bot/              # Prompt engineering, LLM API integration, and chat logic
├── manage.py            # Django management CLI
└── requirements.txt     # Production dependencies
```
