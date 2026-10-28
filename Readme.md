# TaskHub

Full-stack aplikace pro plánování týmové práce: úkoly z backlogu se přetahují do týdenního kalendáře, přiřazují se členům týmu a dají se roztáhnout na víc hodin. Projekt vznikl jako showcase do portfolia.

**Live demo:** [taskhub.tomas-dev.cz](https://taskhub.tomas-dev.cz). Na přihlašovací stránce klikněte na **Demo režim** a aplikace vám založí dočasný účet s vlastním týmem, bez registrace.


## Technologie

| Vrstva | Použito |
|---|---|
| Frontend | Vue 3 (Composition API), Vue Router, Pinia, Tailwind CSS 4, Vite |
| Backend | Django 5, Django REST Framework, SimpleJWT |
| Databáze | PostgreSQL 15 |
| Infrastruktura | Docker Compose, nginx (reverse proxy + TLS přes Let's Encrypt), Gunicorn |
| CI/CD | GitHub Actions (testy proti Postgres service), deploy skript v Bashi |


## Nasazení

Produkce běží na VPS přes Docker Compose. Skript [deploys/deploy.sh](deploys/deploy.sh) stáhne poslední verzi, sestaví a restartuje kontejnery, smaže staré images a pak až 30× ověří, že web odpovídá. Pokud neodpoví, vypíše logy backendu.
