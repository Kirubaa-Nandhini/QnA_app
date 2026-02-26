## ADDED Requirements

### Requirement: Question model fields
The system SHALL store each question with the following fields: `text` (string, required), `question_type` (choices: multiple-choice, true/false, short-answer; required), `difficulty` (choices: easy, medium, hard; required), `tags` (string, optional, comma-separated), `views` (integer, default 0), `likes` (integer, default 0), `created_at` (auto timestamp), `updated_at` (auto timestamp).

#### Scenario: Question is saved with all required fields
- **WHEN** a user submits the create form with `text`, `question_type`, and `difficulty` filled in
- **THEN** the system SHALL save the question to the database and redirect to the question detail page

#### Scenario: Question creation fails when required fields are missing
- **WHEN** a user submits the create form with `text` empty
- **THEN** the system SHALL redisplay the form with a validation error and NOT save the record

---

### Requirement: List all questions
The system SHALL display a paginated list of all questions showing `text`, `question_type`, `difficulty`, `tags`, `views`, and `likes` for each entry.

#### Scenario: Questions exist in the database
- **WHEN** a user visits `/questions/`
- **THEN** the system SHALL render a list of all questions ordered by `created_at` descending

#### Scenario: No questions exist
- **WHEN** a user visits `/questions/` and the database is empty
- **THEN** the system SHALL display an empty-state message indicating no questions have been added yet

---

### Requirement: View question detail
The system SHALL display full question details on a dedicated page, including all model fields.

#### Scenario: Valid question ID
- **WHEN** a user visits `/questions/<id>/`
- **THEN** the system SHALL render the detail page for that question, incrementing `views` by 1

#### Scenario: Invalid question ID
- **WHEN** a user visits `/questions/<id>/` with a non-existent ID
- **THEN** the system SHALL return a 404 response

---

### Requirement: Create a question
The system SHALL provide a form at `/questions/create/` for adding a new question.

#### Scenario: User creates a valid question
- **WHEN** a user submits the create form with valid data
- **THEN** the system SHALL save the question and redirect to its detail page

---

### Requirement: Edit a question
The system SHALL provide a form at `/questions/<id>/edit/` for modifying an existing question's `text`, `question_type`, `difficulty`, and `tags`.

#### Scenario: User updates a question
- **WHEN** a user submits the edit form with valid data
- **THEN** the system SHALL update the record and redirect to the question detail page

#### Scenario: Edit preserves views and likes
- **WHEN** a question is updated via the edit form
- **THEN** the `views` and `likes` counts SHALL remain unchanged

---

### Requirement: Delete a question
The system SHALL provide a confirmation page at `/questions/<id>/delete/` and remove the question on POST confirmation.

#### Scenario: User confirms deletion
- **WHEN** a user confirms deletion on the delete page
- **THEN** the system SHALL delete the question and redirect to the question list

#### Scenario: User cancels deletion
- **WHEN** a user visits the delete page but navigates away without confirming
- **THEN** the question SHALL remain in the database

---

### Requirement: Tailwind CSS styling
The system SHALL use Tailwind CSS (loaded via CDN) to style all question templates including list, detail, create, edit, and delete pages.

#### Scenario: Base template loads Tailwind
- **WHEN** any question page is rendered
- **THEN** the HTML `<head>` SHALL include the Tailwind CDN `<script>` tag and Tailwind utility classes SHALL apply correctly to all elements
