## ADDED Requirements

### Requirement: Answer model fields
The system SHALL store each answer with the following fields: `question` (ForeignKey to Question, required), `text` (string, required), `votes` (integer, default 0), `created_at` (auto timestamp), `updated_at` (auto timestamp).

#### Scenario: Answer is saved with all required fields
- **WHEN** a user submits the answer form with a valid `text`
- **THEN** the system SHALL save the answer linked to the current question and redirect back to the question detail page

#### Scenario: Answer creation fails when required fields are missing
- **WHEN** a user submits the answer form with `text` empty
- **THEN** the system SHALL redisplay the form with a validation error on the question detail page

---

### Requirement: List answers for a question
The system SHALL display all answers associated with a specific question on its detail page.

#### Scenario: Answers exist for a question
- **WHEN** a user visits `/questions/<id>/`
- **THEN** the system SHALL render a list of all answers associated with that question ID

#### Scenario: No answers exist for a question
- **WHEN** a user visits `/questions/<id>/` and no answers have been submitted yet
- **THEN** the system SHALL display a message indicating "No answers yet" below the question

---

### Requirement: Submit an answer from Question Detail
The system SHALL provide an inline form at the bottom of the Question Detail page to add a new answer.

#### Scenario: User submits a valid answer
- **WHEN** a user fills the answer form on the question detail page and clicks "Submit"
- **THEN** the system SHALL create the answer and append it to the answer list for that question
