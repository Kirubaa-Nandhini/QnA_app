## Context

The system already has a `Question` model and basic CRUD functionality. This design adds the secondary entities—`Answer` and `Comment`—and the interaction logic between them. It specifically addresses different "answering" paradigms for various question types (Choice-based vs. Text-based).

## Goals / Non-Goals

**Goals:**
- Implement an **Interactive Reveal System** for MCQ and True/False questions.
- Support **Short Answer Reference Answers** with a controlled reveal button.
- Implement discrete **Upvote and Downvote counting** for community answers.
- Automate **True/False option creation** to ensure consistent UX.
- Allow community submissions only for questions that require descriptive input.

**Non-Goals:**
- Per-user vote tracking (anonymous session-based logic is sufficient for MVP).
- Nested comment threads (one level of discussion per question).

## Decisions

### D1: Type-Aware "Answering" Logic
**Decision**: 
- **MCQ/TF**: Browsers handle the answer via an interactive "click-to-reveal" JavaScript system. No database entry is created for these "self-test" answers.
- **Short Answer**: A dedicated `correct_answer` field on the `Question` model stores the canonical solution, which is hidden behind a reveal button.
- **Community Answers**: Users can only post new `Answer` model entries for **Short Answer** questions.

---

### D2: Separate Vote Counters
**Decision**: In the `Answer` model, track `upvotes` (PositiveIntegerField) and `downvotes` (PositiveIntegerField) separately.
**Rationale**: Provides more granular data for future features (e.g., sorting by most controversial or most upvoted) rather than just a net score.

---

### D3: Automated Choice Integrity
**Decision**: In the Question Form, if "True/False" is selected, the Choice sub-forms are automatically set to exactly two rows with fixed text values managed via JavaScript.
**Rationale**: Prevents users from accidentally creating a T/F question with only one option or with nonsensical labels like "Yes/No".

---

### D4: AJAX-Powered Assessment
**Decision**: All interactive reveals and voting use AJAX (Fetch API) to prevent page reloads.
**Rationale**: Assessment and voting are micro-interactions. A full-page refresh would disrupt the user's flow and mental state during a quiz.

## Risks / Trade-offs

| Risk | Mitigation |
|---|---|
| Multiple Attempts in MCQ | The Assessment JS disables all choice clicks once a selection is made. |
| Cheat reveals | Reference answers are rendered in the HTML but hidden via `display: none` and revealed via JS; sufficient for non-secure quiz environments. |
| UI Clutter | Conditional rendering hides the long-form answer editor for MCQ types. |

## Migration Plan

1. **State Expansion**: Add `upvotes`, `downvotes`, and `correct_answer` fields to relevant models.
2. **Interactive UI**: Develop the `handleChoiceClick` and `revealCorrectAnswer` JS logic in `question_detail.html`.
3. **Form Logic**: Update `QuestionForm` and `ChoiceFormSet` for automatic T/F population.
4. **Data Sync**: Implement AJAX handlers to update separate counters and return JSON feedback.
