## Context

The project currently operates with a single `questions` app. To scale effectively and maintain clean separation of concerns, the authentication logic will be moved to a standalone `users` app. This follows the Django "best practice" of isolating core secondary systems like identity.

## Goals / Non-Goals

**Goals:**
- Implement a complete authentication lifecycle (Signup -> Login -> Logout).
- Provide secure password recovery workflows (forgot password).
- Style all authentication pages to match the existing premium Dark Mode/Tailwind CSS theme.
- Ensure all views are protected by `LoginRequiredMixin` or `login_required` decorator.

**Non-Goals:**
- Social Auth (OAuth2/Google/GitHub) — out of scope for MVP.
- Profile management (avatars, bios) — will be handled in a separate "profiles" change.
- JWT or Token-based auth — the platform will use standard Django sessions.

## Decisions

### D1: Dedicated `users` App
**Decision**: Create a new app using `python manage.py startapp users`.
**Rationale**: Keeps the codebase modular and prevents the `questions` app from becoming bloated with unrelated logic.

---

### D2: Leverage `django.contrib.auth.views`
**Decision**: Use Django's built-in class-based views for Login, Logout, and Password Reset.
**Rationale**: These views are battle-tested and secure. We only need to provide the templates and URL routing.

---

### D3: Custom Signup Flow
**Decision**: Implement a custom `signup` view and `UserCreationForm` subclass.
**Rationale**: Django's default `UserCreationForm` is basic. A custom subclass allows us to add fields (like Email as required) and apply Tailwind styling directly to the widgets.

---

### D4: Consistent Global Navigation
**Decision**: Update `base.html` to show "Login/Signup" buttons for guests and "Logout/Profile" for authenticated users.
**Rationale**: Essential for user discovery of auth features.

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| Plaintext Passwords | Django uses PBKDF2 with a SHA256 hash by default, ensuring high security. |
| Email Failure | Implementation of a full SMTP configuration (`EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_HOST_USER`, etc.) to ensure reliable delivery of reset tokens. |
| CSRF Vulnerabilities | Ensure all templates use `{% csrf_token %}` (Django's built-in protection). |

## Migration Plan

1. **Initialize App**: Run `startapp users` and register in `INSTALLED_APPS`.
2. **Forms**: Define `CustomUserCreationForm` in `users/forms.py`.
3. **Views/URLs**: Set up the `users:signup` view and map `auth_views` in `users/urls.py`.
4. **Templates**: Create the `users` template structure with Tailwind styling.
5. **Integration**: Update `settings.py` auth redirects and the `base.html` navigation.
