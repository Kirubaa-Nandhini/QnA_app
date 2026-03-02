# Tasks: Advanced Search and Discovery

## Phase 1: Search Infrastructure (SQLite)
- [x] Create a custom search filter utility using `Q` objects.
- [x] Implement search logic in `QuestionListView` using keyword splitting and `icontains`.

## Phase 2: Advanced Filtering
- [x] Create a sidebar filters section in `question_list.html`.
- [x] Add date range logic to `QuestionListView.get_queryset`.
- [x] Implement "Unanswered" filter logic.
- [x] Style the filter sidebar with Dark Mode/Tailwind CSS.

## Phase 3: Discovery (Related Content)
- [x] Implement related questions discovery logic in `QuestionDetailView`.
- [x] Create a related questions sidebar in `question_detail.html`.
- [x] Integrate the sidebar into `question_detail.html`.

## Phase 4: Polish & Performance
- [ ] Add database indexes for search and date fields.
- [ ] Implement "Did you mean?" suggestions (requires PostgreSQL for Trigram Similarity).
- [x] Verify responsive behavior on mobile (collapse sidebars into menus).
