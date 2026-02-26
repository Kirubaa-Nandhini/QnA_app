## ADDED Requirements

### Requirement: Question registered in Django admin
The system SHALL register the `Question` model with Django's admin site so that superusers can manage questions via `/admin/`.

#### Scenario: Superuser accesses question admin
- **WHEN** a superuser navigates to `/admin/questions/question/`
- **THEN** the system SHALL display the list of all questions with columns for `text`, `question_type`, `difficulty`, `views`, `likes`, and `created_at`

---

### Requirement: Admin list display and filtering
The system SHALL configure the admin list view with useful display columns, search, and filters.

#### Scenario: Admin searches by question text
- **WHEN** a superuser enters a search term in the admin search box
- **THEN** the system SHALL filter the question list to show only questions whose `text` contains the search term

#### Scenario: Admin filters by question_type or difficulty
- **WHEN** a superuser applies a sidebar filter for `question_type` or `difficulty`
- **THEN** the system SHALL display only questions matching the selected filter value

---

### Requirement: Engagement fields are read-only in admin
The system SHALL mark `views` and `likes` as read-only fields within the admin change form to prevent manual corruption of counts.

#### Scenario: Admin opens a question for editing
- **WHEN** a superuser opens a question in the admin change form
- **THEN** `views` and `likes` SHALL be displayed as read-only (non-editable) fields
