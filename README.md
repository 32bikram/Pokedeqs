# Pokedeqs[🔗](https://pokedeqs-two.vercel.app/)

Pokedeqs is a Pokémon card collection tracker. Upload a photo of a physical card, and the backend identifies it using a vision LLM (Google Gemini), then adds or removes it from your personal collection on buy and sell. A minimal red/white frontend is included to demo the API end to end.

## Why this project

Most collection-tracking apps require manual data entry. PokeDeqs removes that step: snap a photo, and the card's name, set, and number are extracted automatically and matched against (or added to) a shared card catalog, then linked to the personal inventory count.

## Features

- **Auth** — JWT-based signup/login, passwords hashed with bcrypt (via `passlib`)
- **Card identification** — uploaded card images are sent to Gemini with a structured-output prompt; the response is validated against a Pydantic schema before touching the database
- **Buy / sell flow** — uploading a card with `action=buy` increments your count for that card (creating the card/collection entry on first purchase); `action=sell` decrements it
- **Fuzzy search** — search your collection by Pokémon name or set name using PostgreSQL trigram similarity (`pg_trgm`), so partial or slightly misspelled queries still match, ranked by similarity.
- **Frontend demo UI** — single-page HTML/CSS/JS client covering login, register, search, and card upload, so the API is easy to exercise without Postman/Swagger

## Tech stack

**Backend:** FastAPI, SQLAlchemy (ORM), PostgreSQL, Pydantic / `pydantic-settings`, `python-jose` (JWT), `passlib` + bcrypt (password hashing), Google Gemini (`google-genai`) for card identification

**Frontend:** HTML, CSS, vanilla JavaScript (`fetch` against the REST API — no framework)

## Architecture

```
Client (upload photo)
      │
      ▼
POST /upload/  ──► Gemini vision model ──► structured card JSON
      │                                          │
      ▼                                          ▼
  validate against            match/create row in `cards`,
  schemas.Card                update count in `collections`
      │                                          │
      └──────────────► CardDetails response ◄────┘
```

**Data model** (`application/models.py`):
- `users` — account credentials
- `cards` — the shared card catalog (`card_id` = `<set_name>-<card_number>`, deduplicated across all users)
- `collections` — join table between `users` and `cards`, tracking `card_count` per user per card

Separating `cards` from `collections` means the catalog is only ever identified by the LLM once per unique card — after that, every user's copy is just a count against the same row.

## API endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/createuser` | No | Register a new account |
| GET | `/getuser/{email}` | No | Look up a user by email |
| POST | `/login` | No | OAuth2 password login, returns a JWT |
| POST | `/upload/` | Yes | Upload a card image + `action` (`buy`/`sell`) |
| GET | `/search/?pokemon_name=` or `?set_name=` | Yes | Fuzzy search the collection |

Interactive API docs are available at `/docs` once the server is running.

## Setup

### Backend

1. Install dependencies:
   ```bash
   pip install -r requirments.txt
   ```
2. Create a `.env` file in the project root:
   ```env
   DATABASE_HOSTNAME=localhost
   DATABASE_PORT=5432
   DATABASE_USERNAME=your_pg_user
   DATABASE_PASSWORD=your_pg_password
   DATABASE_NAME=pokedeqs
   SECRET_KEY=your_jwt_secret
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   LLM_API=your_gemini_api_key
   ```
3. Make sure PostgreSQL has the `pg_trgm` extension enabled (required for fuzzy search):
   ```sql
   CREATE EXTENSION IF NOT EXISTS pg_trgm;
   ```
4. Run the server:
   ```bash
   uvicorn application.main:app --reload
   ```
   The API will be live at `http://localhost:8000`, with docs at `http://localhost:8000/docs`.

> **CORS:** if you're serving the frontend from a different origin than the API, add `CORSMiddleware` to `main.py` so the browser doesn't block requests.

### Frontend

The `frontend/` folder is static — no build step. Open `index.html` in a browser, or serve the folder with any static file server. Set the API URL field in the top bar to wherever your backend is running (defaults to `http://localhost:8000`). It is generated with the help of LLM.

## Known limitations / roadmap

- No automated tests yet (planned)
- Schema is currently created via `Base.metadata.create_all` on startup — migrating to **Alembic** for proper, reversible schema migrations
- No rate limiting on the upload endpoint

## Project structure

```
application/
├── main.py            # FastAPI app entrypoint
├── config.py           # env-based settings
├── database.py          # SQLAlchemy engine/session
├── models.py            # ORM models (Users, Cards, Collections)
├── schemas.py            # Pydantic request/response schemas
├── oauth2.py              # JWT creation/verification
├── utils.py                # password hashing
├── identifier.py            # Gemini card-identification call
├── purchase.py               # buy/sell business logic
├── availability.py            # card/collection existence checks
└── routers/
    ├── auth.py                # /login
    ├── user.py                 # /createuser, /getuser
    ├── upload.py                # /upload
    └── carddata.py               # /search
```
### Docker

The backend image is published on Docker Hub as [`kiertolainen/pokedeqs:latest`](https://hub.docker.com/r/kiertolainen/pokedeqs).

Two Compose files are provided in the repo:

- `docker-compose-dev.yml` — development setup
- `docker-compose-prod.yml` — production setup

Make sure your `.env` file (see the Backend section above) is present in the project root before running either one, then start the stack:

```bash
# Development
docker compose -f docker-compose-dev.yml up -d

# Production
docker compose -f docker-compose-prod.yml up -d
```

To pull the image directly instead of building from source:

```bash
docker pull kiertolainen/pokedeqs:latest
```
## Connect with Me
[![LeetCode](https://img.shields.io/badge/LeetCode-FFA116?style=for-the-badge&logo=leetcode&logoColor=white)](https://leetcode.com/u/kiertolainen/)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/bikram-sarkar-b90521257/)
[![Instagram](https://img.shields.io/badge/Instagram-E4405F?style=for-the-badge&logo=instagram&logoColor=white)](https://www.instagram.com/bikramdsarkar/)
