# Project Worldview: Collaborative Q&A Platform

## Tech Stack
- [cite_start]**Framework**: Django (Python) [cite: 1]
- **Database**: PostgreSQL (Required for Full-Text Search features)
- **Frontend**: Django Templates + Tailwind CSS
- [cite_start]**Authentication**: Django Contrib Auth (Session-based) [cite: 1]

## Coding Standards & Rules
- **Architecture**: Use Django Best Practices (Fat Models, Thin Views).
- [cite_start]**Views**: Use Django's built-in `auth_views` (LoginView, LogoutView, PasswordResetView, etc.) and Class-Based Views (CBVs) for CRUD[cite: 6].
- **Style**: Follow PEP 8 strictly.

- **Security**: 
    - [cite_start]Always enforce "Content Owner" checks for Edit/Delete actions[cite: 19, 145].
    - [cite_start]Use `LoginRequiredMixin` for all content creation and voting views[cite: 144].
- **Naming**: Use descriptive slug fields for Question URLs.
## Core Entities
- [cite_start]**User**: Standard Django User model (Username, Email, Password)[cite: 20].
- [cite_start]**Question**: Title, Description, Tags, Author, Timestamps[cite: 1].
- [cite_start]**Answer**: Content, Question Link, Author, Timestamps[cite: 1].
- [cite_start]**Comment**: Content, Parent (Question/Answer), Author[cite: 1].
- [cite_start]**Vote**: User, Target Content, Vote Type (Up/Down)[cite: 1].

## Authentication & Identity Requirements
- [cite_start]**Signup**: Custom user registration form with validation[cite: 24, 25].
- **Login/Logout**: Standard session-based management.
- **Password Management**: Full suite of Change Password and Reset via Email logic.

## Discovery & Recommendation Rules
- [cite_start]**Search**: Implement PostgreSQL Full-Text Search using `SearchVector` and `SearchQuery` to index Titles and Descriptions[cite: 1].
- [cite_start]**Filtering**: Enable filtering and sorting by creation date (Newest/Oldest)[cite: 1].
- [cite_start]**Related Content**: Display "Related Questions" on detail pages by filtering for shared Tags[cite: 1].

## App Structure
- **users/**: Dedicated app for Authentication, Signup, Login/Logout, and Password Management.
- **questions/**: Handles Question CRUD, Tags, PostgreSQL Full-Text Search, and Related Questions logic.
- **answers/**: Manages Answers, Comments, and the unified Voting system.
- **core/**: (Optional) For global base templates, custom context processors, and Tailwind CSS configuration.