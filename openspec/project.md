# Project Worldview: Collaborative Q&A Platform

## Tech Stack
- [cite_start]**Framework**: Django (Python) [cite: 1]
- **Database**: PostgreSQL (Required for Full-Text Search features)
- **Frontend**: Django Templates + Tailwind CSS
- [cite_start]**Authentication**: Django Contrib Auth (Session-based) [cite: 1]

## Coding Standards & Rules
- **Architecture**: Use Django Best Practices (Fat Models, Thin Views).
- [cite_start]**Views**: Prefer Class-Based Views (CBVs) for CRUD operations[cite: 1].
- **Style**: Follow PEP 8 strictly.
- [cite_start]**Security**: Always enforce "Content Owner" checks for Edit/Delete actions[cite: 1].
- [cite_start]**Naming**: Use descriptive slug fields for Question URLs[cite: 1].

## Core Entities
- [cite_start]**Question**: Title, Description, Tags, Author, Timestamps[cite: 1].
- [cite_start]**Answer**: Content, Question Link, Author, Timestamps[cite: 1].
- [cite_start]**Comment**: Content, Parent (Question/Answer), Author[cite: 1].
- [cite_start]**Vote**: User, Target Content, Vote Type (Up/Down)[cite: 1].

## Discovery & Recommendation Rules
- [cite_start]**Search**: Implement PostgreSQL Full-Text Search using `SearchVector` and `SearchQuery` to index Titles and Descriptions[cite: 1].
- [cite_start]**Filtering**: Enable filtering and sorting by creation date (Newest/Oldest)[cite: 1].
- [cite_start]**Related Content**: Display "Related Questions" on detail pages by filtering for shared Tags[cite: 1].
