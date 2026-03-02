## Why

The QnA application currently has no way to manage questions — there is no model, API, or UI for creating, viewing, editing, or deleting questions. Beyond basic CRUD, questions need social engagement signals (likes and view counts) displayed beneath each question, so users can identify popular and frequently-visited content. A Question Management System with these engagement metrics forms the core domain layer before answer or quiz functionality can be built on top.

## What Changes

- Introduce a `Question` Django model with fields:
  - `text` — the question body
  - `question_type` — multiple-choice, true/false, or short-answer
  - `difficulty` — easy / medium / hard
  - `tags` — comma-separated keyword tags
  - `views` — integer counter, auto-incremented each time a question's detail page is loaded
  - `likes` — integer counter, incremented when a user clicks the Like button
  - `created_at` and `updated_at` — auto-managed timestamps
- Implement full CRUD views (list, create, detail, update, delete) for questions
- Display `views` and `likes` counts visually beneath the question text on both the list and detail pages
- Provide a "Like" action endpoint that increments the like counter without a full page reload (via a simple POST)
- Register the `Question` model with the Django admin interface
- Add URL routing for all question and like endpoints
- Style all templates using **Tailwind CSS** (via CDN for development, with a `tailwind.config.js` for production builds if needed)
- Create HTML templates with a consistent base layout styled with Tailwind utility classes

## Capabilities

### New Capabilities

- `question-crud`: Create, read, update, and delete questions with support for multiple question types, difficulty levels, and tag filtering
- `question-engagement`: Track and display `views` (auto-incremented on detail page load) and `likes` (user-triggered) beneath each question on list and detail views
- `question-admin`: Django admin panel integration for managing questions as a super-user

### Modified Capabilities

_(None — this is a greenfield feature; no existing specs are impacted)_

## Impact

- **New app**: A new Django app (e.g., `questions`) will be created inside the project
- **Database**: A new migration will add the `questions_question` table with `views` and `likes` integer columns
- **URLs**: Root `urls.py` will include the new `questions/` URL namespace; a dedicated `like/` sub-route will handle like increments
- **Templates**: New templates directory under the `questions` app; list and detail templates will render likes/views badges below the question text
- **Dependencies**: **Tailwind CSS** added as the UI framework — loaded via CDN for development; optionally compiled via `tailwindcss` CLI or `django-tailwind` package for production; no other new third-party Python packages required
