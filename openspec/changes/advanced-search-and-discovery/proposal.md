# Proposal: Advanced Search and Discovery

## Overview
As the QnA application grows, finding relevant content becomes more difficult with basic search. This proposal outlines the implementation of a high-performance discovery system including PostgreSQL Full-Text Search (FTS), advanced filtering, and a "Related Questions" sidebar.

## Objectives
- **Speed & Relevance**: Replace standard database lookups with PostgreSQL Full-Text Search.
- **Precision Discovery**: Allow users to filter questions by specific date ranges.
- **Increased Engagement**: Surface related content on detail pages to keep users exploring.

## Core Features
1. **Enhanced Keyword Search**:
   - Implement robust multi-field filtering across title, body, and tags using Django's `icontains`.
   - Support for multiple keywords (AND/OR logic).
2. **Advanced Filtering**:
   - Sidebar filters for the question list page.
   - Date range filtering (Today, This Week, This Month, Custom).
   - Status filtering (Answered vs. Unanswered).
3. **Related Questions Sidebar**:
   - A new dynamic component on the `question_detail.html` page.
   - Uses shared tags and FTS similarity to suggest 5 most relevant other questions.

## Success Criteria
- Search results appear in < 200ms.
- Related questions have at least one shared tag or high text similarity.
- UI remains responsive and follows the premium Dark Mode theme.
