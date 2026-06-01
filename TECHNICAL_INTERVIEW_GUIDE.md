# Menu Planner Technical Interview Guide

This guide explains the Menu Planner project from both the frontend and backend perspectives. It is written as interview preparation material: use it to explain what the project does, how the Svelte frontend talks to the Django backend, what each major file is responsible for, and what tradeoffs or improvements you can discuss.

## 1. Project Summary

Menu Planner is a full-stack web application for browsing and planning UFS meals. Users can:

- View today's generated menu.
- Browse all available dishes.
- Filter dishes by food category.
- Search for dishes.
- View dish details.
- Like or dislike dishes.
- Select foods and track total calorie intake against a personal calorie goal.
- Submit dish requests through a form.

The project is split into two main applications:

- `frontend/`: SvelteKit application, built with Svelte, Vite, Tailwind CSS, Flowbite Svelte, and Lucide icons.
- `backend/backend_app/`: Django application, built with Django, Django REST Framework, SQLite, django-cors-headers, and APScheduler.

At a high level:

```text
Browser
  |
  | SvelteKit routes and components
  v
Frontend dev server: http://localhost:5173
  |
  | fetch() HTTP requests
  v
Django API server: http://127.0.0.1:8000
  |
  | Django ORM queries and updates
  v
SQLite database: backend/backend_app/db.sqlite3
```

## 2. Tech Stack

### Frontend

- Svelte 5: component framework used to build interactive UI.
- SvelteKit: routing, page structure, and route-level `load()` functions.
- Vite: development server and build tooling.
- TypeScript: supported by SvelteKit and used in some components/routes.
- Tailwind CSS v4: utility-first styling through the Vite plugin.
- Flowbite Svelte: UI component dependency available in the project.
- Lucide Svelte: icon library used in the request page.

Important files:

- `frontend/src/routes/+layout.svelte`: shared app layout and sidebar navigation.
- `frontend/src/routes/dashboard/+page.js`: fetches today's menu dishes.
- `frontend/src/routes/dashboard/+page.svelte`: renders today's menu dashboard.
- `frontend/src/routes/meals/+page.js`: fetches all dishes.
- `frontend/src/routes/meals/+page.svelte`: renders all meals with search/category filtering.
- `frontend/src/routes/meals/[meal_id]/+page.js`: fetches one dish by id.
- `frontend/src/routes/meals/[meal_id]/+page.svelte`: renders one dish detail page.
- `frontend/src/routes/request/+page.svelte`: dish request form and POST request logic.
- `frontend/src/lib/FoodList.svelte`: dashboard food list, calorie selection, likes/dislikes.
- `frontend/src/lib/AllFoodList.svelte`: all-meals list with navigation to detail pages.
- `frontend/src/lib/CategoryButtons.svelte`: reusable category filter buttons.
- `frontend/src/lib/Tracker.svelte`: calorie goal/intake tracker.
- `frontend/src/lib/AnimatedCircularProgressBar.svelte`: SVG progress indicator.
- `frontend/src/index.css`: Tailwind import and custom font theme tokens.
- `frontend/vite.config.ts`: SvelteKit and Tailwind Vite plugin setup.

### Backend

- Django 5.2.3: backend web framework.
- Django REST Framework: serializers, routers, viewsets, and API responses.
- SQLite: local relational database.
- django-cors-headers: allows the Svelte dev server to call the Django API from the browser.
- APScheduler: schedules weekly menu generation.

Important files:

- `backend/backend_app/backend_app/settings.py`: Django settings, installed apps, database, CORS, timezone.
- `backend/backend_app/backend_app/urls.py`: root URL configuration.
- `backend/backend_app/api/models.py`: database models.
- `backend/backend_app/api/serializers.py`: converts model instances to/from JSON.
- `backend/backend_app/api/views.py`: API viewsets and custom endpoints.
- `backend/backend_app/api/urls.py`: DRF router and endpoint registration.
- `backend/backend_app/api/services.py`: menu generation business logic.
- `backend/backend_app/api/scheduler.py`: weekly scheduler setup.
- `backend/backend_app/api/apps.py`: starts scheduler when the Django app is ready.
- `backend/backend_app/api/admin.py`: Django admin registration.

## 3. System Architecture

The frontend and backend are separate during development:

- SvelteKit runs on `http://localhost:5173`.
- Django runs on `http://127.0.0.1:8000`.
- Svelte uses `fetch()` to call Django endpoints.
- Django returns JSON responses.
- Svelte renders the JSON into interactive components.

This separation is useful to explain in interviews because it shows a clear API boundary:

- The frontend owns presentation, navigation, filtering, searching, and user interactions.
- The backend owns persistence, data validation through serializers/model fields, database relationships, menu generation, and API contracts.

## 4. Data Model

The backend defines four main models in `backend/backend_app/api/models.py`.

### Dish

Represents one food item.

Fields:

- `dish_name`: unique dish name.
- `dish_type`: category code, such as `CH`, `PO`, `SF`, `VE`, `BF`, `SN`, `FR`.
- `dish_method`: cooking method, such as `SAUTE`, `FRIED`, `BAKED`, `SAUCY`, `SOUPY`.
- `dish_color`: simple color classification, such as brown, orange, white, or yellow.
- `dish_description`: short text description.
- `dish_calories`: calories per serving.
- `dish_likes`: like counter.
- `dish_dislikes`: dislike counter.

Interview explanation:

> The `Dish` model is the core entity. It stores the metadata needed for display and also stores attributes used by the menu generation algorithm, such as type, method, and color.

### Menu

Represents a menu for one date.

Fields:

- `date`: unique date for the menu.
- `created_at`: timestamp when the menu was created.

Interview explanation:

> I made `Menu.date` unique so the system does not generate duplicate menus for the same day.

### MenuDish

Join table between `Menu` and `Dish`.

Fields:

- `menu`: foreign key to `Menu`.
- `dish`: foreign key to `Dish`.

Interview explanation:

> `MenuDish` models a many-to-many relationship explicitly. A menu can have many dishes, and a dish can appear in menus on different dates. Using an explicit join model gives room to add extra fields later, such as serving time, quantity, price, or availability.

### Request

Represents a user-submitted dish request.

Fields:

- `name`
- `student_number`
- `up_mail`
- `dish_name`
- `dish_type`
- `dish_description`

Interview explanation:

> The `Request` model stores user feedback separately from approved dishes. This keeps user-submitted data out of the official dish catalog until an admin reviews it.

## 5. Backend API Design

The API is built with Django REST Framework.

### Serializers 

Defined in `backend/backend_app/api/serializers.py`.

- `DishSerializer`: exposes all `Dish` fields.
- `MenuSerializer`: exposes all `Menu` fields.
- `MenuDishSerializer`: nests both `DishSerializer` and `MenuSerializer`.
- `RequestSerializer`: exposes all `Request` fields.

Why serializers matter:

- They define the JSON shape sent to the frontend.
- They translate Django model instances into API responses.
- They validate incoming JSON for endpoints such as `POST /requests/`.

Interview explanation:

> Serializers are the contract between Django models and frontend JSON. For `MenuDish`, I used nested serializers because the dashboard needs the actual dish data, not just foreign key IDs.

### Viewsets

Defined in `backend/backend_app/api/views.py`.

`DishViewSet`

- Uses `ModelViewSet`.
- Provides list, retrieve, create, update, partial update, and delete actions for dishes.

`MenuViewSet`

- Uses `ModelViewSet`.
- Provides CRUD operations for menus.

`MenuDishViewSet`

- Uses `ReadOnlyModelViewSet`.
- Only supports read operations.
- Filters to today's menu using `localdate()`.
- Uses `select_related('dish')` to avoid extra database queries when fetching nested dish data.

`RequestViewSet`

- Uses `ModelViewSet`.
- Allows request submission and admin-style CRUD access.

Interview explanation:

> I used DRF viewsets because most entities follow standard REST patterns. For menu dishes, I intentionally made the viewset read-only because the dashboard only needs to consume generated menus rather than directly mutate them.

### URL Routing

Defined in `backend/backend_app/api/urls.py`.

DRF `DefaultRouter` registers:

- `/dishes/`
- `/menus/`
- `/menu-dishes/`
- `/requests/`

Custom endpoints:

- `/`: welcome JSON response.
- `/generate-menu/`: triggers weekly menu generation.
- `/dish/react-increment/`: increments like or dislike counters.

Interview explanation:

> The router removes repetitive URL wiring for CRUD resources, while custom endpoints handle behavior that is not a simple CRUD operation.

## 6. Backend Endpoints

| Endpoint | Method | Purpose | Frontend Usage |
| --- | --- | --- | --- |
| `/` | GET | API welcome message | Health/manual check |
| `/dishes/` | GET | List all dishes | Meals page |
| `/dishes/<id>/` | GET | Get one dish | Meal detail page |
| `/menus/` | GET/POST/etc. | CRUD for menus | Admin/API use |
| `/menu-dishes/` | GET | Get today's menu dishes | Dashboard page |
| `/requests/` | GET/POST/etc. | CRUD for dish requests | Request page POST |
| `/generate-menu/` | GET | Generate next weekly menus | Manual/scheduler support |
| `/dish/react-increment/` | POST | Increment like/dislike count | FoodList reaction buttons |

## 7. Menu Generation Logic

The algorithm lives in `backend/backend_app/api/services.py` inside `MenuGeneratorService`.

Responsibilities:

- Determine the current week range.
- Avoid reusing dishes already used in the same week.
- Choose dishes based on category rules.
- Create one `Menu` row for the target date.
- Create multiple `MenuDish` rows linking the menu to selected dishes.

Important methods:

- `get_week_used_dishes()`: finds dishes already used in the current week.
- `get_candidates()`: excludes already-used dishes.
- `pick_dishes(dishes, count, filters=None)`: randomly samples dishes when enough candidates exist.
- `pick_color_combo(color_groups, count)`: chooses dishes from different color groups.
- `generate_menu()`: applies all menu rules and saves the result.

Selection rules in `generate_menu()`:

- Chicken:
  - 2 saucy chicken dishes with different colors.
  - 1 fried or soupy chicken dish.
  - 1 baked or roasted chicken dish.
- Pork:
  - 2 saucy pork dishes with different colors.
  - 1 fried pork dish.
- Seafood:
  - 1 seafood dish.
- Vegetables:
  - 2 vegetable dishes.
- Breakfast:
  - 1 to 2 breakfast items.
- Snacks:
  - 1 to 2 snack items.
- Fruits:
  - 1 to 2 fruit items.

Interview explanation:

> I separated the menu generation rules into a service class instead of putting all of the logic inside the view. That makes the business rules easier to test, reuse, and change independently from the HTTP layer.

## 8. Scheduler

Scheduling is handled in `backend/backend_app/api/scheduler.py`.

The function `generate_weekly_menus()`:

1. Gets today's date in the configured timezone.
2. Calculates the next Monday.
3. Loops from Monday to Saturday.
4. Calls `MenuGeneratorService(date=day).generate_menu()` for each day.
5. Tracks generated and skipped days.

The function `start_scheduler()`:

- Creates a `BackgroundScheduler`.
- Adds a cron job for weekly menu generation.
- Starts the scheduler.

In `backend/backend_app/api/apps.py`, the scheduler starts from `ApiConfig.ready()`.

Interview explanation:

> APScheduler lets the app generate menus automatically on a schedule. The generation function also skips existing menus, so running it more than once should not create duplicate menus for the same date.

Production caveat:

> Starting a scheduler inside `AppConfig.ready()` is convenient for development, but in production it can run multiple times if the app has multiple worker processes. A more production-ready setup would move scheduled jobs into a separate worker, cron task, Celery beat process, or management command.

## 9. CORS and Frontend-Backend Communication

In `backend/backend_app/backend_app/settings.py`:

- `corsheaders` is installed in `INSTALLED_APPS`.
- `corsheaders.middleware.CorsMiddleware` is added at the top of `MIDDLEWARE`.
- `CORS_ALLOWED_ORIGINS` includes `http://localhost:5173`.

Why this matters:

The browser enforces same-origin policy. Since SvelteKit and Django run on different ports during development, the Django backend must explicitly allow requests from the SvelteKit origin.

Interview explanation:

> Because the frontend and backend run on different origins in development, I configured CORS so the browser would allow Svelte's `fetch()` calls to reach the Django API.

## 10. Frontend Architecture

The frontend is a SvelteKit app. SvelteKit uses file-based routing:

- `src/routes/dashboard/+page.svelte` becomes `/dashboard`.
- `src/routes/meals/+page.svelte` becomes `/meals`.
- `src/routes/meals/[meal_id]/+page.svelte` becomes `/meals/:meal_id`.
- `src/routes/request/+page.svelte` becomes `/request`.

The shared layout is defined in `src/routes/+layout.svelte`, which wraps every page with:

- A responsive sidebar.
- UFS logo.
- Navigation links.
- Main content slot.

Interview explanation:

> SvelteKit's file-based routing made it easy to organize the app by page. Shared UI, such as the sidebar, lives in the layout, while each route owns its own data loading and page-specific interactions.

## 11. SvelteKit Data Loading

Several pages use SvelteKit `load()` functions to fetch backend data before rendering.

### Dashboard

File: `frontend/src/routes/dashboard/+page.js`

Flow:

1. Calls `GET http://127.0.0.1:8000/menu-dishes/`.
2. Receives `MenuDish` objects with nested `dish` objects.
3. Maps each `entry.dish` into a flat `dishes` array.
4. Returns `{ dishes }` to `+page.svelte`.

Interview explanation:

> The backend returns menu-dish records because it needs to preserve the menu relationship, but the dashboard mostly renders dishes. The `load()` function adapts the API shape into the UI shape.

### All Meals

File: `frontend/src/routes/meals/+page.js`

Flow:

1. Calls `GET http://127.0.0.1:8000/dishes/`.
2. Parses the JSON response.
3. Returns `{ dishes: data }`.

### Meal Detail

File: `frontend/src/routes/meals/[meal_id]/+page.js`

Flow:

1. Reads `params.meal_id` from the URL.
2. Calls `GET http://127.0.0.1:8000/dishes/${params.meal_id}/`.
3. Returns `{ meal: data }`.

Interview explanation:

> Dynamic routes let each dish have its own URL. The route parameter is passed into `load()`, then used to fetch the matching backend resource.

## 12. Svelte Components

### CategoryButtons

File: `frontend/src/lib/CategoryButtons.svelte`

Responsibilities:

- Displays food category buttons.
- Receives the current active category.
- Calls `setActive(category.label)` when a user clicks a category.

Svelte detail:

- Uses Svelte 5 `$props()` syntax.

Interview explanation:

> This component is stateless from the user's perspective. It receives state from the parent and notifies the parent when the selected category changes.

### AllFoodList

File: `frontend/src/lib/AllFoodList.svelte`

Responsibilities:

- Receives all dishes.
- Filters by selected category.
- Filters by search text.
- Displays cards for each dish.
- Uses SvelteKit `goto()` to navigate to `/meals/{id}`.

Important reactive statement:

```js
$: filteredFoods = foods.filter(food => {
  const correctCategory = selectedCategory === "All Foods" || food.dish_type === CATEGORY_MAP[selectedCategory];
  const correctSearch = search === "" || food.dish_name.toLowerCase().includes(search.toLowerCase());
  return correctCategory && correctSearch;
});
```

Interview explanation:

> Svelte's reactive statements make derived UI state concise. When `foods`, `selectedCategory`, or `search` changes, `filteredFoods` recalculates automatically.

### FoodList

File: `frontend/src/lib/FoodList.svelte`

Responsibilities:

- Renders today's menu dishes.
- Allows selecting dishes into a calorie tracker.
- Calculates total calories.
- Handles like/dislike UI state.
- Sends reaction updates to the backend.
- Shows a temporary popup message after a reaction.

Important frontend concepts:

- Local component state: `chosen_foods`, `liked_foods`, `disliked_foods`.
- Derived state: `totalCalories`.
- Event modifiers: `on:click|stopPropagation` prevents button clicks from triggering the card click.
- Optimistic UI: local like/dislike state updates before the API call finishes.
- Rollback: if the API call fails, the local state is toggled back.

Interview explanation:

> The reaction flow uses optimistic UI: I immediately update the interface so the app feels responsive, then persist the reaction to Django. If the API call fails, I roll back the local UI state.

### Tracker

File: `frontend/src/lib/Tracker.svelte`

Responsibilities:

- Lets the user input a calorie goal.
- Receives calorie intake from selected foods.
- Computes calories remaining.
- Renders the circular progress bar.

Svelte detail:

- Uses Svelte 5 `$props()` and `$derived()`.

Interview explanation:

> The calorie tracker demonstrates component composition. The parent list owns selected foods and passes total calories into `Tracker`, while `Tracker` owns goal input and display logic.

### AnimatedCircularProgressBar

File: `frontend/src/lib/AnimatedCircularProgressBar.svelte`

Responsibilities:

- Draws an SVG circle.
- Computes progress percentage from `value`, `min`, and `max`.
- Uses SVG `stroke-dasharray` to visualize progress.

Interview explanation:

> The progress bar is a reusable visual component. It receives numeric props and converts them into SVG stroke values, so it is decoupled from the food-specific logic.

## 13. Request Page Flow

File: `frontend/src/routes/request/+page.svelte`

Flow:

1. User enters personal information.
2. User enters dish request details.
3. `submitRequest()` builds a payload.
4. Frontend sends `POST http://127.0.0.1:8000/requests/`.
5. Django REST Framework validates and saves the request using `RequestSerializer`.
6. Frontend shows success or error feedback.

Payload shape:

```json
{
  "name": "Student Name",
  "student_number": "2023-00000",
  "up_mail": "student@up.edu.ph",
  "dish_name": "Requested Dish",
  "dish_type": "CH",
  "dish_description": "Description"
}
```

Interview explanation:

> The request form is a simple example of client-side state becoming a JSON payload, then being persisted through a DRF endpoint.

## 14. Like/Dislike Flow

Frontend file: `frontend/src/lib/FoodList.svelte`

Backend function: `dish_react_increment()` in `backend/backend_app/api/views.py`

Frontend sends:

```json
{
  "dish_id": 1,
  "reaction": "like"
}
```

Backend logic:

1. Reads `dish_id` and `reaction`.
2. Validates that reaction is either `like` or `dislike`.
3. Looks up the dish.
4. Uses Django `F()` expressions to increment the count atomically.
5. Returns updated like/dislike totals.

Why `F()` matters:

`F("dish_likes") + 1` performs the increment in the database. This is safer than reading the old value into Python, incrementing it, and saving it back, because concurrent requests are less likely to overwrite each other.

Interview explanation:

> I used Django `F()` expressions for the reaction counter so increments happen atomically at the database level.

## 15. End-to-End Request Lifecycle

Use this explanation when asked "what happens when the page loads?"

Example: dashboard page

1. The user visits `/dashboard`.
2. SvelteKit runs `frontend/src/routes/dashboard/+page.js`.
3. `load()` calls `GET http://127.0.0.1:8000/menu-dishes/`.
4. Django routes the request through `api/urls.py`.
5. `MenuDishViewSet.get_queryset()` filters records to today's date.
6. `MenuDishSerializer` serializes each menu dish with nested menu and dish data.
7. Django returns JSON.
8. SvelteKit passes the data into `dashboard/+page.svelte`.
9. The page renders `CategoryButtons` and `FoodList`.
10. The user filters, selects food, or reacts to dishes through Svelte component state.

## 16. Styling and UI

The project uses Tailwind CSS through `@tailwindcss/vite`.

Configured in:

- `frontend/vite.config.ts`
- `frontend/src/index.css`

The CSS imports Google fonts and defines Tailwind theme font tokens:

- `--font-game`
- `--font-bitter`
- `--font-raleway`
- `--font-sharetech`

UI patterns:

- Responsive sidebar layout in `+layout.svelte`.
- Responsive grid for food cards.
- Category filter buttons.
- Card-based dish display.
- Form sections on request page.
- SVG circular progress indicator for calories.

Interview explanation:

> Tailwind let me build responsive layouts quickly using utility classes directly in Svelte components. The shared layout keeps navigation consistent across pages.

## 17. Running the Project Locally

### Backend

From the repo root:

```powershell
cd backend
.\env\Scripts\Activate.ps1
cd backend_app
python manage.py runserver
```

Backend URL:

```text
http://127.0.0.1:8000
```

### Frontend

From the repo root:

```powershell
cd frontend
npm install
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## 18. Strong Interview Talking Points

### Full-stack architecture

> This is a decoupled frontend/backend app. SvelteKit handles the browser UI and Django REST Framework exposes JSON endpoints. The two communicate through HTTP using `fetch()`.

### Why Django REST Framework

> DRF gave me model serializers, viewsets, and routers, which made it fast to expose RESTful endpoints for dishes, menus, menu dishes, and requests.

### Why Svelte/SvelteKit

> Svelte is lightweight and reactive. SvelteKit adds routing and `load()` functions, which made it straightforward to fetch backend data per page.

### State management

> Most state is local to components because the app is not large enough to need a global store. For example, category selection and search are page-level state, while selected foods and reaction state live in `FoodList`.

### API contract

> The frontend relies on predictable JSON shapes from DRF serializers. For example, `/menu-dishes/` returns nested dish data, while `/dishes/` returns a flat dish list.

### Database design

> `Dish`, `Menu`, and `MenuDish` separate the dish catalog from daily menu assignments. This prevents duplicating dish details each time a menu is generated.

### Business logic separation

> Menu generation lives in `MenuGeneratorService`, separate from views. That keeps HTTP request handling separate from domain rules.

### Concurrency

> Reaction counters use Django `F()` expressions, which are safer for concurrent increments.

### CORS

> Because the frontend and backend run on different ports locally, Django must allow the SvelteKit origin with CORS settings.

## 19. Known Issues and Improvement Opportunities

These are useful to mention if asked "what would you improve?"

### Move API base URL to environment variables

Current frontend code hardcodes:

```js
http://127.0.0.1:8000
```

Improvement:

Use `VITE_API_BASE_URL` so development, staging, and production can use different API origins.

### Add tests

Current `api/tests.py` is empty.

Useful tests:

- Serializer validation tests.
- API endpoint tests for `/dishes/`, `/requests/`, `/menu-dishes/`.
- Menu generation tests.
- Reaction increment tests.
- Frontend component tests for filtering/search behavior.

### Fix unresolved merge conflict in `FoodList.svelte`

`frontend/src/lib/FoodList.svelte` currently contains conflict markers:

```text
<<<<<<< HEAD
=======
>>>>>>> ...
```

This should be resolved before production or demo use.

### Align dish type codes

Backend uses pork code `PO`, but some frontend helper logic uses `PR` or `PK` in places.

Examples:

- `Request` page has a pork option value of `PK`.
- Price helpers check `PR`.
- Backend choices use `PO`.

Improvement:

Create one shared mapping or carefully align frontend constants with backend choices.

### Improve validation and error handling

Current frontend error handling mostly uses `alert()` and console logs.

Improvement:

- Show inline validation errors.
- Disable submit while loading.
- Add success/error UI states.
- Validate required fields before sending the request.

### Add authentication and permissions

Current API exposes write-capable viewsets.

Improvement:

- Allow students to submit requests.
- Restrict dish/menu CRUD to admins.
- Add permissions to protect mutation endpoints.

### Improve production scheduler setup

Current scheduler starts in `AppConfig.ready()`.

Improvement:

- Move scheduling to Celery Beat, cron, a management command, or a separate worker.
- Avoid duplicate scheduled jobs under multiple server workers.

### Add pagination and filtering to API

The dish list could grow.

Improvement:

- Add DRF pagination.
- Add query parameters for category/search.
- Decide whether filtering belongs on the server, client, or both.

### Add OpenAPI documentation

Improvement:

Use a tool such as drf-spectacular to generate API docs and keep frontend/backend contracts clearer.

## 20. Possible Interview Questions and Answers

### "Can you walk me through your project?"

Answer:

> Menu Planner is a full-stack app for browsing UFS dishes, viewing today's generated menu, tracking selected meal calories, reacting to dishes, and submitting dish requests. The frontend is built with SvelteKit and Tailwind CSS. It uses route-level `load()` functions and component state to render API data. The backend is Django with Django REST Framework. It exposes REST endpoints for dishes, menus, menu-dish relationships, and requests. The backend also has a service class that generates weekly menus based on dish type, cooking method, and color constraints.

### "How does the frontend communicate with the backend?"

Answer:

> The Svelte frontend uses `fetch()` to call the Django REST API. For example, the meals page calls `/dishes/`, the dashboard calls `/menu-dishes/`, the detail page calls `/dishes/:id/`, and the request form posts to `/requests/`. Since SvelteKit and Django run on different ports locally, Django uses CORS settings to allow requests from `http://localhost:5173`.

### "Why did you use nested serializers for menu dishes?"

Answer:

> The dashboard needs to render dish details, not only menu-dish IDs. By nesting `DishSerializer` inside `MenuDishSerializer`, the backend returns the dish object directly, which simplifies frontend rendering.

### "How does menu generation work?"

Answer:

> The menu generation logic is in `MenuGeneratorService`. It first excludes dishes already used in the same week, then selects dishes according to category rules: chicken, pork, seafood, vegetables, breakfast, snacks, and fruits. It also considers method and color for variety, such as choosing saucy dishes with different colors. Once selected, it creates a `Menu` for the date and creates `MenuDish` rows for each selected dish.

### "How do likes and dislikes work?"

Answer:

> The frontend stores local liked/disliked state for immediate UI feedback. When a user turns on a reaction, it sends a POST request to `/dish/react-increment/` with the dish ID and reaction type. The backend validates the payload, finds the dish, and uses Django `F()` expressions to atomically increment the correct counter.

### "What are the main Svelte features you used?"

Answer:

> I used SvelteKit file-based routing, route `load()` functions, component props, event handlers, reactive statements, conditional rendering, list rendering with `{#each}`, and component composition. Some components also use Svelte 5 runes like `$props()` and `$derived()`.

### "What are the main Django features you used?"

Answer:

> I used Django models and migrations for persistence, the Django ORM for queries, Django REST Framework serializers and viewsets for API endpoints, routers for URL generation, admin registration for data management, CORS middleware for frontend integration, and APScheduler for periodic menu generation.

### "What would you change if you had more time?"

Answer:

> I would resolve the current merge conflict in `FoodList.svelte`, move the hardcoded API base URL into environment variables, add tests for API endpoints and menu generation, add authentication and permissions for admin-only actions, improve form validation, and move the scheduler into a more production-safe background worker.

## 21. One-Minute Project Pitch

> Menu Planner is a SvelteKit and Django REST Framework application for managing and browsing UFS meals. The frontend uses Svelte components, route-level data loading, Tailwind styling, category filters, search, calorie tracking, and optimistic reaction UI. The backend models dishes, menus, menu-dish relationships, and user requests with Django ORM. DRF serializers and viewsets expose JSON endpoints consumed by the frontend. I also implemented a menu generation service that creates weekly menus based on dish categories, methods, and color variety while avoiding repeated dishes in the same week. The project taught me how to design a full-stack API boundary, connect Svelte to Django through REST, and separate UI concerns from backend business logic.

## 22. File Map for Review

```text
menu_planner/
  README.md
  API_FRONTEND_BACKEND_FLOW.md
  TECHNICAL_INTERVIEW_GUIDE.md

  backend/
    README.md
    backend_app/
      manage.py
      db.sqlite3
      backend_app/
        settings.py
        urls.py
        asgi.py
        wsgi.py
      api/
        models.py
        serializers.py
        views.py
        urls.py
        services.py
        scheduler.py
        apps.py
        admin.py
        tests.py
        migrations/

  frontend/
    package.json
    vite.config.ts
    svelte.config.js
    src/
      routes/
        +layout.svelte
        +page.svelte
        dashboard/
          +page.js
          +page.svelte
        meals/
          +page.js
          +page.svelte
          [meal_id]/
            +page.js
            +page.svelte
        request/
          +page.svelte
      lib/
        FoodList.svelte
        AllFoodList.svelte
        CategoryButtons.svelte
        Tracker.svelte
        AnimatedCircularProgressBar.svelte
      index.css
      app.css
    static/
      images/
      UFS-Logo-Maroon.png
```

