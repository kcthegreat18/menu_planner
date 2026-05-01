# Django API ↔ Svelte Frontend Integration Guide (Menu Planner)

This document explains **exactly how this project connects the Django REST API to the Svelte frontend**, step-by-step, so you can confidently discuss it in interviews.

---

## 1) Overall Architecture

- **Backend:** Django + Django REST Framework, running on `http://127.0.0.1:8000`.
- **Frontend:** SvelteKit app, running on `http://localhost:5173` in development.
- **Communication:** Frontend uses `fetch(...)` to call Django endpoints over HTTP.
- **Cross-origin support:** Django allows the Svelte dev origin via CORS.

---

## 2) Backend Routing and API Surface

### 2.1 Root URL wiring

In Django project URLs, all root traffic is delegated to the `api` app:

- `backend/backend_app/backend_app/urls.py`
  - `path('', include('api.urls'))`

This means endpoints like `/dishes/`, `/menu-dishes/`, and `/requests/` are served directly from the API app.

### 2.2 API endpoints

In `backend/backend_app/api/urls.py`, DRF `DefaultRouter` registers 4 viewsets:

- `dishes` → `/dishes/` and `/dishes/<id>/`
- `menus` → `/menus/`
- `menu-dishes` → `/menu-dishes/`
- `requests` → `/requests/`

Custom function-based endpoints are also exposed:

- `/generate-menu/`
- `/dish/react-increment/` (POST)

There is also a lightweight root response at `/` via `home`.

### 2.3 View logic

In `backend/backend_app/api/views.py`:

- `DishViewSet` and `MenuViewSet` are full `ModelViewSet` CRUD endpoints.
- `MenuDishViewSet` is read-only and filters records to **today’s date** using `localdate()`.
- `RequestViewSet` handles dish request submissions (create/read/update/delete).
- `dish_react_increment` accepts a JSON POST body with:
  - `dish_id`
  - `reaction` (`"like"` or `"dislike"`)
  and increments counters with atomic `F(...)` expressions.

---

## 3) CORS and Middleware (Critical for Frontend Calls)

In `backend/backend_app/backend_app/settings.py`:

- `corsheaders` is installed in `INSTALLED_APPS`.
- `corsheaders.middleware.CorsMiddleware` is added near the top of `MIDDLEWARE`.
- `CORS_ALLOWED_ORIGINS` includes `http://localhost:5173`.

This setup is what allows your browser-hosted Svelte app to call Django APIs without CORS blocking in dev.

---

## 4) Frontend API Consumption (Step-by-Step)

## A) Meals list page (`/meals`)

File: `frontend/src/routes/meals/+page.js`

1. SvelteKit `load()` runs when the page loads.
2. It calls `fetch('http://127.0.0.1:8000/dishes/')`.
3. JSON response is parsed and returned as `dishes`.
4. The page receives hydrated data and renders dish cards/components.

## B) Meal detail page (`/meals/[meal_id]`)

File: `frontend/src/routes/meals/[meal_id]/+page.js`

1. Route parameter `meal_id` is read from `params`.
2. The page calls `fetch('http://127.0.0.1:8000/dishes/${params.meal_id}/')`.
3. JSON response is returned as `meal`.
4. UI renders one dish based on backend object payload.

## C) Dashboard page (`/dashboard`)

File: `frontend/src/routes/dashboard/+page.js`

1. Page calls `fetch('http://127.0.0.1:8000/menu-dishes/')`.
2. Backend returns menu-dish objects (each includes nested `dish`).
3. Frontend maps `entry.dish` to flatten the structure before rendering.

This is a good interview example of transforming API shape in the client.

## D) Request page (`/request`)

File: `frontend/src/routes/request/+page.svelte`

1. User fills a form.
2. Component builds a JSON payload (`name`, `student_number`, `up_mail`, `dish_name`, `dish_type`, `dish_description`).
3. Frontend sends `POST` to `http://127.0.0.1:8000/requests/` with `Content-Type: application/json`.
4. On `response.ok`, form is reset and success message is shown.
5. On failure, frontend parses and logs server error response.

## E) Like/Dislike reaction flow

File: `frontend/src/lib/FoodList.svelte`

1. Component stores API base as `http://127.0.0.1:8000`.
2. `reactIncrement(dishId, reaction)` sends `POST` to `/dish/react-increment/`.
3. Body shape: `{ dish_id, reaction }`.
4. Backend validates input and increments either `dish_likes` or `dish_dislikes`.
5. Frontend first updates local UI state, then persists to backend; on error it rolls back local state.

This demonstrates optimistic UI + server persistence.

---

## 5) End-to-End Request Lifecycle (Browser → API → DB → UI)

Use this sequence in interviews:

1. User opens a Svelte route.
2. SvelteKit `load()` (or component event handler) issues `fetch`.
3. Browser sends HTTP request to Django (`127.0.0.1:8000`).
4. Django URL resolver matches endpoint in `api/urls.py`.
5. DRF viewset/function runs business logic and ORM query/update.
6. Django serializes result to JSON.
7. Frontend receives JSON and updates reactive state/UI.

---

## 6) Practical Talking Points for Interviews

- You used **RESTful resources** for core entities (`dishes`, `menus`, `requests`).
- You used a **custom action endpoint** (`/dish/react-increment/`) for non-CRUD behavior.
- You handled **CORS explicitly** for local frontend-backend dev split.
- You used both **server-side route data loading** (`+page.js`) and **client-side interaction fetches** (`+page.svelte`, component methods).
- You implemented **basic optimistic UI** in reactions and rollbacks on network/API failure.
- You shaped nested API responses in the frontend when needed (`menu-dishes` → `entry.dish`).

---

## 7) Suggested Improvements (if interviewers ask “what next?”)

- Move hardcoded API origin to environment variables (`VITE_API_BASE_URL`).
- Add authentication + permission classes for protected write endpoints.
- Add request validation and better typed contracts (OpenAPI schema generation).
- Add centralized API client wrappers and reusable error handlers.
- Add pagination/filtering on list endpoints for scalability.
- Add automated integration tests for frontend-backend contracts.

---

## 8) Quick Endpoint Reference

- `GET /` → API welcome message
- `GET /dishes/` → list dishes
- `GET /dishes/<id>/` → dish detail
- `GET/POST /requests/` → list/create dish requests
- `GET /menu-dishes/` → today’s menu dishes (nested dish payload)
- `POST /dish/react-increment/` → increment likes/dislikes
- `GET /menus/` and CRUD routes via DRF viewset
- `GET /generate-menu/` → trigger menu generation

