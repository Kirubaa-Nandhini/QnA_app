## Requirements

### Requirement: User Authentication (Login)
The system SHALL allow registered users to establish a secure session by providing their credentials.

#### Scenario: Successful Login
- **GIVEN** a registered user is on the login page
- **WHEN** they submit the correct username and password
- **THEN** the system SHALL establish a session and redirect them to the configured `LOGIN_REDIRECT_URL`.

#### Scenario: Login fails with invalid credentials
- **GIVEN** a user is on the login page
- **WHEN** they submit an incorrect password or non-existent username
- **THEN** the system SHALL show an error message "Please enter a correct username and password." and keep the user on the login page.

---

### Requirement: Session Termination (Logout)
The system SHALL allow authenticated users to securely terminate their session.

#### Scenario: Successful Logout
- **GIVEN** an authenticated user clicks the "Logout" button
- **WHEN** the logout request is processed
- **THEN** the system SHALL terminate the session and redirect them to the home page or login page.
