## Why

The QnA application currently allows users to manage questions but lacks the ability for users to provide answers. A community-driven platform requires a way to answer questions and a peer-review mechanism to highlight high-quality content. An Answer Management system with voting (upvotes and downvotes) is essential for building a functional knowledge-sharing ecosystem.

## What Changes

- Introduce an `Answer` Django model in the `questions` app with fields:
  - `question` — ForeignKey linking the answer to a specific `Question`
  - `text` — the content of the answer
  - `votes` — integer counter tracking the net score (upvotes minus downvotes)
  - `created_at` and `updated_at` — auto-managed timestamps
- Update the Question Detail page to:
  - List all answers associated with the question
  - Display the net `votes` count for each answer
  - Provide a form to submit a new answer to that question
- Implement voting actions for answers:
  - "Upvote" button to increment the vote count
  - "Downvote" button to decrement the vote count
- Register the `Answer` model with the Django admin interface
- Add URL routing for answer creation and voting endpoints
- Ensure answers are styled consistently with the existing Tailwind CSS theme

## Capabilities

### New Capabilities

- `answer-management`: Ability to create answers for any existing question and view them on the question's detail page.
- `answer-voting`: Support for upvoting and downvoting answers to reflect community consensus on answer quality.
- `answer-admin`: Integration with the Django admin panel for managing user-submitted answers.

### Modified Capabilities

- `question-detail`: Enhanced the question detail view to include the list of answers and an answer submission form.

## Impact

- **Database**: A new migration will add the `questions_answer` table with a foreign key to the `questions_question` table.
- **Views**: Question detail view will be updated to include answer context; new views for answer submission and voting will be added.
- **Templates**: `question_detail.html` will be significantly expanded to render the answer section; new components for answer display and voting buttons.
- **URLs**: New routes under `questions/` for `answer/<int:pk>/upvote/`, `answer/<int:pk>/downvote/`, and `question/<int:pk>/answer/`.
