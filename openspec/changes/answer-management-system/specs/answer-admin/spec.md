## ADDED Requirements

### Requirement: Answer admin integration
The system SHALL register the `Answer` model in the Django admin interface.

#### Scenario: Admin user manages answers
- **WHEN** an administrator visits the Django admin panel and selects "Answers"
- **THEN** they SHALL be able to view, create, edit, or delete any answer across any question

---

### Requirement: Answer filtering by question in admin
The system SHALL allow admin users to filter answers by the associated question.

#### Scenario: Admin user views answers for a specific question
- **WHEN** an administrator filters the "Answers" list by a particular "Question" ID
- **THEN** only answers belonging to that question ID SHALL be displayed in the admin panel
