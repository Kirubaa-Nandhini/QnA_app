## Context

The system already has a `Question` model and basic CRUD functionality. This design adds the second major entity, `Answer`, and the interaction logic between them. It leverages the existing Tailwind CSS setup and anonymous interaction patterns (votes are simple counters, not uniquely tracked per user yet).

## Goals / Non-Goals

**Goals:**
- Implement the `Answer` model with a relationship to `Question`
- Allow users to submit answers directly from the `Question` detail page
- Enable simple upvote/downvote mechanics for answers (anonymous)
- Ensure answers are displayed chronologically or by vote score

**Non-Goals:**
- Per-user vote tracking (preventing multiple votes from the same user)
- Markdown support for answer text (plain text for now)
- Nested comments or replies to answers
- Question-level voting (already handled by 'likes' in the previous change)

## Decisions

### D1: `Answer` model in the `questions` app
**Decision:** Add the `Answer` model to the existing `questions/models.py` rather than creating a new `answers` app.

**Rationale:** Answers are intrinsically linked to questions. Keeping them in the same app simplifies imports and migrations.

---

### D2: Inline Answer Form on Question Detail Page
**Decision:** The question detail view will include a `ModelForm` for the `Answer` model at the bottom of the page.

**Rationale:** This provides the best user experience, allowing users to read the question and its existing answers before submitting theirs without page transitions.

---

### D3: Voting via POST Redirect
**Decision:** Similar to question likes, upvotes and downvotes will be handled by POST forms that redirect back to the question detail page.

**Rationale:** Consistent with the current design architecture. Avoids JavaScript complexity while ensuring state changes are handled via CSRF-protected POST requests.

---

### D4: Vote Calculation logic
**Decision:** `votes` will be a single `IntegerField`. Upvote = +1, Downvote = -1.

**Rationale:** Simplicity. Total score is the only metric needed for the MVP.

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| Spam answers or vote manipulation | Anonymous for now; add Anti-Spam (reCAPTCHA) or authentication requirements in future iterations |
| Page bloat on questions with many answers | Add pagination to the answer list if a question exceeds 50 answers |
| Rapid voting hitting the database | Use `F()` expressions for atomic increments/decrements |

## Migration Plan

1. Define `Answer` model in `questions/models.py`
2. Create and run migrations: `python manage.py makemigrations` and `python manage.py migrate`
3. Implement `AnswerForm` in `questions/forms.py`
4. Update `QuestionDetailView` in `questions/views.py` to:
   - Include the answer list in context
   - Handle answer submission if the request is a POST (or use a separate view)
5. Add `upvote_answer` and `downvote_answer` view functions
6. Update `urls.py` with new answer patterns
7. Update `question_detail.html` template to render answers and the form
8. Register `Answer` in `admin.py`
