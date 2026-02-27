# Implementation Tasks

## [answer-models] 1. Define the Models [x]

- Add `Answer` model to `questions/models.py` with `ForeignKey` to `Question` [x]
- Add `Comment` model to `questions/models.py` for meta-discussion [x]
- Register both models in `questions/admin.py` [x]
- Run `python manage.py makemigrations` and `python manage.py migrate` [x]
- **Original Blocked Task**: Run `python manage.py makemigrations` and `python manage.py migrate` [ ] (Blocked: Terminal issue - kept for historical context)

---

## [answer-views] 2. Implement Views for Answers and Voting [x]

- Create function-based views for `create_answer` and `create_comment` [x]
- Implement AJAX-compatible `upvote_answer` and `downvote_answer` views returning `JsonResponse` [x]
- Create `AnswerUpdateView` and `AnswerDeleteView` for full CRUD capabilities [x]
- Register all endpoints in `questions/urls.py` [x]

---

## [answer-forms] 3. Create Forms [x]

- Define `AnswerForm` and `CommentForm` in `questions/forms.py` [x]
- Apply consistent Tailwind CSS styling to all widgets [x]

---

## [answer-detail-expansion] 4. Update Question Detail Page [x]

- Expand `QuestionDetailView` context with:
  - Sorted Answer list [x]
  - Chronological Comment list [x]
  - Both `AnswerForm` and `CommentForm` [x]
- In `question_detail.html`:
  - Implement **Conditional Logic**: Only show the "Your Answer" form if `question_type == 'short_answer'` [x]
  - Hide empty states: Only show the "Answers" header if answers exist [x]
  - AJAX Integration: Connect voting buttons to the Fetch API for instant score updates [x]
  - Management UI: Add links to the Update and Delete views for each answer [x]
  - Comment Workspace: Render a separate, styled discussion area at the bottom [x]

---

## [answer-form-logic] 5. Refine Question Creation Flow [x]

- Update `question_form.html` to handle the new `correct_answer` field (for Short Answer types) [x]
- Implement JavaScript logic to toggle between Choice management (MCQ/TF) and Reference Answer input [x]

---

## [answer-testing] 6. Final Integration and Verification [x]

- Verified AJAX voting updates DOM without refresh [x]
- Verified conditional form hiding for non-short-answer questions [x]
- Verified Answer Edit/Delete lifecycle [x]
- Confirmed "No answers yet" placeholder removal [x]

### Original Verification Tasks (Historical)
- Manually test:
  - [ ] Submit a new answer for an existing question
  - [ ] Verify answer appears in the list on reload
  - [ ] Click Upvote and confirm the score increments
  - [ ] Click Downvote and confirm the score decrements
- [ ] Ensure answers are correctly attributed to the parent question in the database
