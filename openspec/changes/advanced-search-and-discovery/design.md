# Design: Advanced Search and Discovery

## Architectural Approach

### 1. Enhanced Keyword Search (SQLite Compatible)
We will use Django's `Q` objects and `icontains` for a broad cross-field search.
- **Dynamic Q filters**: Filter across `text`, `tags`, and `author__username`.
- **Keyword Splitting**: Split user queries into individual words to find more inclusive matches.

### 2. Filtering Architecture
A new `QuestionFilter` service or utility class will be created to handle complex `Q` objects:
- **Date Filtering**: Use `created_at__gte` with calculated date offsets (e.g., `timezone.now() - timedelta(days=7)`).
- **Status Filtering**: Use `annotate(answer_count=Count('answers'))` and filter for `answer_count__gt=0`.

### 3. Related Questions Sidebar
Instead of complex AI, we will use a **Frequency-based Similarity** approach:
- Find questions that share at least 2 tags with the current question.
- Exclude the current question.
- Limit to top 5 results sorted by net votes.

## UI/UX Design

### Sidebar Layout
- **Left Sidebar** on `question_list.html`:
  - Search input with glassmorphism style.
  - Radio buttons for "Time Range".
  - Toggle for "Only Unanswered".
- **Right Sidebar** on `question_detail.html`:
  - "Related Questions" card with a subtle border and brand icons.

### Indicators
- Highlight search terms in results using the `<mark>` tag styled with a brand-glow effect.

## Risks & Trade-offs
- **PostgreSQL Dependency**: This feature will ONLY work on PostgreSQL. Local development on SQLite will require `django.contrib.postgres` to be disabled or switched to a mock search.
- **Performance**: Many-to-Many tag filtering can be slow. We will optimize with database indexes on `created_at` and search vectors.
