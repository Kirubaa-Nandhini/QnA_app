## ADDED Requirements

### Requirement: Auto-increment view count on detail page load
The system SHALL increment a question's `views` counter by exactly 1 each time its detail page is loaded via a GET request, using a race-condition-safe database update.

#### Scenario: User visits a question's detail page
- **WHEN** a GET request is made to `/questions/<id>/`
- **THEN** the system SHALL increment `Question.views` by 1 before rendering the page

#### Scenario: Concurrent visits do not lose counts
- **WHEN** multiple simultaneous GET requests are made to the same detail page
- **THEN** each request SHALL increment `views` by exactly 1 with no lost updates (using `F()` expression)

---

### Requirement: Display views and likes beneath question text
The system SHALL display both the `views` count and `likes` count visually beneath the question text on the detail page and in each question card on the list page.

#### Scenario: Detail page shows engagement metrics
- **WHEN** a user views a question's detail page
- **THEN** the page SHALL display the current `views` count and `likes` count below the question text, styled as distinct badges using Tailwind CSS

#### Scenario: List page shows engagement metrics per card
- **WHEN** a user views the question list
- **THEN** each question card SHALL display the `views` and `likes` counts below the question text

---

### Requirement: User can like a question
The system SHALL allow a user to increment a question's `likes` counter by submitting a POST request to `/questions/<id>/like/`.

#### Scenario: User clicks the Like button
- **WHEN** a user submits the like form on the detail page
- **THEN** the system SHALL increment `Question.likes` by 1 and redirect back to the detail page

#### Scenario: Like action is CSRF-protected
- **WHEN** the like form is rendered
- **THEN** the form SHALL include Django's `{% csrf_token %}` and only accept POST requests

#### Scenario: Like increments are cumulative and anonymous
- **WHEN** the same user clicks Like multiple times
- **THEN** each click SHALL increment `likes` by 1 with no uniqueness enforcement (anonymous counting)

---

### Requirement: Admin can view and edit engagement counts
The system SHALL expose `views` and `likes` as read-only fields in the Django admin question detail panel.

#### Scenario: Admin views a question in the admin panel
- **WHEN** a superuser opens a question in Django admin
- **THEN** the admin SHALL display `views` and `likes` as read-only fields alongside other question data
