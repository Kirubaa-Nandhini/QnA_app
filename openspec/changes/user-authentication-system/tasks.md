# Implementation Tasks

## [users-setup] 1. Application Initialization [x]

- [x] Run `python manage.py startapp users`
- [x] Add `'users'` to `INSTALLED_APPS` in `QnA_app/settings.py`
- [x] Set up empty `users/urls.py` and include it in `QnA_app/urls.py` with the `users/` prefix
- [x] Configure `LOGIN_URL = 'users:login'`, `LOGIN_REDIRECT_URL = 'questions:list'`, and `LOGOUT_REDIRECT_URL = 'questions:list'` in `settings.py`

---

## [users-signup] 2. User Registration [x]

- [x] Create `users/forms.py` with `CustomUserCreationForm` inheriting from `UserCreationForm`
- [x] Implement `signup` view in `users/views.py` to process the form and log in the user upon success
- [x] Create `users/signup.html` template with Tailwind styling
- [x] Add `signup/` path to `users/urls.py`

---

## [users-auth] 3. Login and Logout [x]

- [x] Map `auth_views.LoginView.as_view(template_name='users/login.html')` in `users/urls.py`
- [x] Map `auth_views.LogoutView.as_view()` in `users/urls.py`
- [x] Create `users/login.html` template with Tailwind styling
- [x] Ensure `base.html` navigation handles authenticated vs. anonymous states correctly

---

## [users-password] 4. Password Management [x]

- [x] Set up URL patterns for `password_reset`, `password_reset_done`, `password_reset_confirm`, and `password_reset_complete`
- [x] Implement the 4 required templates in `users/` using the global Dark Mode design
- [x] **Configure SMTP Settings** in `settings.py`:
  - [x] Set `EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'`
  - [x] Define `EMAIL_HOST`, `EMAIL_PORT`, `EMAIL_USE_TLS`, `EMAIL_HOST_USER`, and `EMAIL_HOST_PASSWORD`
- [x] Add `PasswordChangeView` and its corresponding template

---

## [users-protection] 5. Security Integration [x]

- [x] Apply `LoginRequiredMixin` to `QuestionCreateView`, `QuestionUpdateView`, and `QuestionDeleteView` in `questions/views.py`
- [x] Add `@login_required` decorators to the voting views (`like_question`, `upvote_answer`, etc.)
- [x] Update `Question` and `Answer` models to include an `author` field (Migration pending: USER needs to run `makemigrations`)

---

## [users-verification] 6. End-to-End Testing [ ]

- [ ] Verify new user can register and is redirected to the questions list
- [ ] Verify existing user can login and logout accurately
- [ ] Verify that attempting to "Ask a Question" while logged out redirects to the login page
- [ ] Test the password reset flow via terminal console email output
