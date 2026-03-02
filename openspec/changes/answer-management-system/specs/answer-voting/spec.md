## ADDED Requirements

### Requirement: Upvote an answer
The system SHALL increment the `votes` counter of an answer by 1 when the upvote action is triggered.

#### Scenario: User upvotes an answer
- **WHEN** a user clicks the "Upvote" button for a specific answer
- **THEN** the system SHALL increment that answer's `votes` score and redirect to the question detail page

---

### Requirement: Downvote an answer
The system SHALL decrement the `votes` counter of an answer by 1 when the downvote action is triggered.

#### Scenario: User downvotes an answer
- **WHEN** a user clicks the "Downvote" button for a specific answer
- **THEN** the system SHALL decrement that answer's `votes` score and redirect to the question detail page

---

### Requirement: Anonymous voting
The system SHALL allow voting on answers anonymously, treating each upvote/downvote as a simple counter increment/decrement.

#### Scenario: Multiple users vote on an answer
- **WHEN** several users click the upvote/downvote buttons for a specific answer
- **THEN** the `votes` count SHALL reflect the net sum of those actions (e.g., 5 upvotes and 2 downvotes = 3 votes)
