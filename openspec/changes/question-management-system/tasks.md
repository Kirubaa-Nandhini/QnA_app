## 1. Project Setup

- [x] 1.1 Create the `questions` Django app: `python manage.py startapp questions`
- [x] 1.2 Add `'questions'` to `INSTALLED_APPS` in `settings.py`
- [x] 1.3 Create `questions/templates/questions/` directory for all HTML templates
- [x] 1.4 Create a `base.html` template that loads Tailwind CSS via CDN `<script>` tag and defines `{% block content %}` slot

## 2. Question Model

- [x] 2.1 Define the `Question` model in `questions/models.py` with fields: `text`, `question_type` (choices), `difficulty` (choices), `tags`, `views` (default=0), `likes` (default=0), `created_at`, `updated_at`
- [x] 2.2 Run `python manage.py makemigrations questions` to generate the migration
- [x] 2.3 Run `python manage.py migrate` to apply the migration and create the `questions_question` table

## 3. Admin Registration

- [x] 3.1 Register `Question` in `questions/admin.py` with a custom `ModelAdmin` class
- [x] 3.2 Set `list_display` to include `text`, `question_type`, `difficulty`, `views`, `likes`, `created_at`
- [x] 3.3 Add `search_fields = ['text']` and `list_filter = ['question_type', 'difficulty']`
- [x] 3.4 Add `readonly_fields = ['views', 'likes']` to prevent manual editing of engagement counts

## 4. Forms

- [x] 4.1 Create `questions/forms.py` with a `QuestionForm` `ModelForm` exposing `text`, `question_type`, `difficulty`, and `tags` fields
- [x] 4.2 Apply Tailwind utility classes to form widget `attrs` (e.g., `class="border rounded px-3 py-2 w-full"`) for consistent styling

## 5. CRUD Views

- [x] 5.1 Implement `QuestionListView` (CBV `ListView`) — orders by `-created_at`
- [x] 5.2 Implement `QuestionDetailView` (CBV `DetailView`) — increments `views` by 1 using `F()` expression on GET before rendering
- [x] 5.3 Implement `QuestionCreateView` (CBV `CreateView`) — uses `QuestionForm`, success redirects to detail page
- [x] 5.4 Implement `QuestionUpdateView` (CBV `UpdateView`) — uses `QuestionForm`, success redirects to detail page
- [x] 5.5 Implement `QuestionDeleteView` (CBV `DeleteView`) — shows confirmation page, success redirects to list
- [x] 5.6 Implement `like_question` function-based view — accepts POST only, increments `likes` by 1 using `F()`, redirects to detail page

## 6. URL Routing

- [x] 6.1 Create `questions/urls.py` with routes for: list `/`, create `create/`, detail `<int:pk>/`, edit `<int:pk>/edit/`, delete `<int:pk>/delete/`, like `<int:pk>/like/`
- [x] 6.2 Include `questions.urls` in the root `QnA_app/urls.py` under the `questions/` prefix

## 7. Templates

- [x] 7.1 Create `question_list.html` — extends `base.html`, renders a card grid of questions; each card shows `text`, `question_type`, `difficulty`, `tags`, and displays `views` 👁 and `likes` ❤️ badges below the question text using Tailwind
- [x] 7.2 Create `question_detail.html` — extends `base.html`, shows all question fields; renders `views` and `likes` as styled badges below the question text; includes the Like `<form method="POST">` with `{% csrf_token %}`
- [x] 7.3 Create `question_form.html` — extends `base.html`, renders the `QuestionForm` with labeled fields and a submit button; used for both create and update
- [x] 7.4 Create `question_confirm_delete.html` — extends `base.html`, shows the question text and confirmation/cancel buttons

## 8. Smoke Testing

- [x] 8.1 Verify question list page loads at `/questions/` and shows empty state when no questions exist
- [x] 8.2 Create a question via the form and confirm it appears on the list page
- [x] 8.3 Visit the detail page and confirm `views` increments by 1 on each load
- [x] 8.4 Click Like and confirm `likes` increments by 1 and redirects back to detail page
- [x] 8.5 Edit the question and confirm `views` and `likes` are unchanged after edit
- [x] 8.6 Delete the question and confirm redirect to list and removal from database
- [x] 8.7 Log into `/admin/` as superuser and verify `views` and `likes` are read-only in the admin change form
