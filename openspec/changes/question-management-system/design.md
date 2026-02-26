## Context

The QnA application is a Django project starting from a blank slate (only the default project scaffold exists). There is no existing `questions` app, no models, and no templates. This design establishes the architecture for the entire Question Management System including engagement tracking (`views`, `likes`) and Tailwind CSS-based UI.

## Goals / Non-Goals

**Goals:**
- Define the Django app structure, model schema, URL layout, and view strategy for questions
- Establish how `views` (auto-tracked) and `likes` (user-triggered) are stored and incremented
- Specify how Tailwind CSS is integrated — via CDN for now
- Ensure all pages render properly with a shared base template

**Non-Goals:**
- User authentication or per-user like tracking (likes are anonymous counts for now)
- Answer/comment functionality (out of scope for this change)
- Production Tailwind build pipeline (`django-tailwind`) — CDN is sufficient at this stage
- Pagination, search, or filtering beyond basic tag display
- REST API or JSON endpoints (HTML-rendered views only)

## Decisions

### D1: Separate `questions` Django app
**Decision:** Create a dedicated `questions` app via `python manage.py startapp questions`.

**Rationale:** Keeps the domain isolated and follows Django conventions. The main project package (`QnA_app`) stays a configuration-only layer.

**Alternative considered:** Putting models directly in the project package — rejected because it violates Django's app-based separation of concerns.

---

### D2: `views` auto-incremented in the detail view
**Decision:** Increment `Question.views` by 1 on every `GET` request to the detail page using a simple `F()` expression update before rendering.

```python
Question.objects.filter(pk=pk).update(views=F('views') + 1)
```

**Rationale:** Using `F()` avoids race conditions from concurrent requests. No caching layer is needed at this scale.

**Alternative considered:** Session/cookie-based de-duplication — deferred; adds complexity without clear benefit at MVP stage.

---

### D3: `likes` via a lightweight POST endpoint (no JS framework)
**Decision:** A dedicated `POST /questions/<id>/like/` view increments `Question.likes` by 1 and redirects back to the detail page. A small `<form method="POST">` handles the action.

**Rationale:** Keeps the implementation dependency-free (no AJAX/fetch required), works without JavaScript enabled, and is trivially testable.

**Alternative considered:** AJAX/fetch with JSON response for a seamless UX — deferred to a future enhancement once the base system is stable.

---

### D4: Tailwind CSS via CDN
**Decision:** Load Tailwind CSS from `https://cdn.tailwindcss.com` in the base template's `<head>`.

**Rationale:** Zero setup cost; ideal for the initial build phase. The CDN version includes the full Tailwind utility set at runtime.

**Alternative considered:** `django-tailwind` with PostCSS build — preferred for production, deferred until the project is ready for deployment.

---

### D5: Class-Based Views (CBVs) for CRUD, function-based view for Like
**Decision:** Use Django's built-in `ListView`, `DetailView`, `CreateView`, `UpdateView`, `DeleteView` for standard CRUD. Use a plain function-based view for the like action.

**Rationale:** CBVs reduce boilerplate for standard operations. The like endpoint is a single `POST` with a redirect — simpler as a function.

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| `views` count inflated by bots/crawlers | Acceptable at MVP; can add rate-limiting or user-session checks later |
| Likes can be submitted multiple times (no uniqueness constraint) | Intentional for now — anonymous counters only; add per-user tracking in a future change |
| Tailwind CDN is blocked in offline environments | Switch to `django-tailwind` for production deployment |
| No CSRF protection awareness for the like form | Django's `{% csrf_token %}` in the form template handles this automatically |

## Migration Plan

1. Create the `questions` app: `python manage.py startapp questions`
2. Define the `Question` model and register in `INSTALLED_APPS`
3. Generate and apply migration: `python manage.py makemigrations && python manage.py migrate`
4. Register URLs in the root `urls.py`
5. Create base template with Tailwind CDN `<script>` tag
6. Build list, detail, create, update, delete, and like templates
7. Register `Question` in `admin.py`
8. Smoke-test all CRUD routes and verify `views`/`likes` increment correctly

**Rollback:** Drop the `questions` app folder, remove from `INSTALLED_APPS` and `urls.py`, and run `python manage.py migrate questions zero`.
