# TaskHub

A full-stack application for planning team work: created tasks are dragged into a weekly calendar, assigned to team members, and can be stretched across multiple hours. The project was built as a portfolio showcase.


**Live demo:** [taskhub.tomas-dev.cz](https://taskhub.tomas-dev.cz). On the login page, click **Demo režim** (Demo mode) and the app will create a temporary account with its own team for you, no registration required.


## Screenshots

**Dashboard** – weekly calendar with team tasks

![Dashboard](media/dashboard.png)

**Login page**

![Login page](media/login.png)


## Tech stack

| Layer | Used |
|---|---|
| Frontend | Vue 3 (Composition API), Vue Router, Pinia, Tailwind CSS 4, Vite |
| Backend | Django 5, Django REST Framework, SimpleJWT |
| Database | PostgreSQL 15 |
| Infrastructure | Docker Compose, nginx (reverse proxy + TLS via Let's Encrypt), Gunicorn |
| CI/CD | GitHub Actions (tests against a Postgres service), Bash deploy script |


## Deployment

Production runs on a VPS via Docker Compose. The [deploys/deploy.sh](deploys/deploy.sh) script pulls the latest version, builds and restarts the containers, removes old images, and then checks up to 30 times that the site is responding. If it doesn't respond, it prints the backend logs.


## Architecture decisions

### Django + Django REST Framework
- **Why:** built-in admin, ORM and auth out of the box; DRF makes a REST API with little boilerplate.
- **Trade-off:** heavier than e.g. FastAPI; for this app size it's not a problem.
- **Alternative considered:** FastAPI

### Vue 3 SPA (separate from the backend)
- **Why:** fast to build with, I use it at work, Pinia keeps calendar state simple.
- **Trade-off:** two deployables instead of one; solved by nginx serving both.

### JWT authentication (SimpleJWT)
- **Why:** I wanted to learn token-based auth hands-on.

### Deployment
- **Now:** Bash script with health check on a VPS.
- **Next step:** automatic deploy from GitHub Actions after green tests.