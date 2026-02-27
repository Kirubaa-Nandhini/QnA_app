## Why

The QnA application currently allows users to manage questions but lacks the ability for community members to contribute their own answers or discuss existing questions. To foster a collaborative learning environment, we need a robust Answer Management system that supports peer evaluation and general discussions. Integrating voting (upvotes/downvotes) and commenting capabilities allows the most helpful content to rise to the top while keeping the community engaged.

## What Changes

- **Introduced Django Models**:
  - `Answer`: Links to a `Question` and tracks content, **independent upvote/downvote counters**, net score, and timestamps.
  - `Comment`: Links to a `Question` to allow for general meta-discussion and clarifications.
- **Interactive Question Detail Workspace**:
  - **Dynamic MCQ/TF Interaction**: Choices are now interactive—clicking an option provides instant feedback with success/error icons and highlights the correct choice. Interaction is disabled once a choice is made to prevent multiple attempts.
  - **Automated T/F Handling**: Form logic ensures True/False questions always have exactly two read-only options ("True" and "False") to maintain data integrity.
  - **Short Answer Reference Reveal**: Implemented a "Show Answer" button that reveals a hidden reference answer for Short Answer questions.
  - **Conditional Answer Submission**: The "Your Answer" input appears only for **Short Answer** questions, whereas MCQ/TF questions rely on the interactive choice system.
  - **Dynamic Content Visibility**: Empty-state placeholders for "Answers" and "Comments" hide automatically to keep the UI clean if no content exists.
- **Seamless Interaction (AJAX + JS)**:
  - **Individual Vote Tracking**: Upvote and downvote actions are tracked separately and updated in real-time via AJAX Fetch API.
  - **Full CRUD Lifecycle**: Added support for **Editing** and **Deleting** answers.
- **Aesthetic Integration**:
  - All interactive elements use the premium Dark Mode design system with glassmorphic cards and vibrant status indicators.

## Capabilities

### New Capabilities

- `interactive-test`: Click-to-reveal feedback for all choice-based questions (MCQ and T/F).
- `answer-management`: Users can submit long-form answers to Short Answer questions and manage their lifecycle (Edit/Delete).
- `separate-voting`: Independent tracking of upvotes and downvotes for more transparent community feedback.
- `short-answer-reference`: Dedicated field in the creation form and reveal UI for authoritative reference answers.
- `discussion-system`: High-level clarification space for questions separate from the solution space.

### Modified Capabilities

- `question-detail`: Transitioned from a static viewing experience to a fully interactive assessment and discussion workspace.

## Impact

- **Database**: Introduced `questions_answer` and `questions_comment` tables. Added `upvotes` and `downvotes` as separate positive integer fields.
- **Views**: Implemented specialized AJAX handlers for individual up/down increments and context-aware detail views.
- **Templates**: `question_detail.html` expanded with complex JavaScript for interactive state management and conditional form rendering.
- **User Flow**: Users can now test their knowledge on choice questions or contribute deep-dive solutions for short-answer prompts.
