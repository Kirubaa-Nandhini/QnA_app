## Requirements

### Requirement: User Registration (Signup)
The system SHALL allow new visitors to create a unique account using a username, email, and password.

#### Scenario: Successful Signup
- **GIVEN** a guest is on the signup page
- **WHEN** they submit the form with a unique username, valid email, and matching passwords
- **THEN** the system SHALL create a new User record, log them in automatically, and redirect to the question list page.

#### Scenario: Signup fails with existing username
- **GIVEN** a guest is on the signup page
- **WHEN** they submit the form with a username that is already taken
- **THEN** the system SHALL redisplay the form with a specific error message "A user with that username already exists."

---

### Requirement: Account Validation
The system SHALL ensure that passwords meet basic safety requirements (length, similarity to username) and that the email address is in a valid format.

#### Scenario: Password too short
- **GIVEN** a guest is on the signup page
- **WHEN** they submit a password with fewer than 8 characters
- **THEN** the system SHALL reject the submission and show a validation error.
