# PIMS - Complete Workflow Guide

## End-to-End Recruitment Process

This guide walks through the complete recruitment lifecycle from publishing a job to archiving placement records.

---

## Phase 1: Setup & Job Posting (Recruiter)

### 1.1 Login as Recruiter
- Navigate to `/` and login with recruiter credentials
- You'll be redirected to Recruiter Dashboard

### 1.2 Create/Manage Company
- Go to **Companies** from sidebar
- Add or select your company
- Wait for Officer approval if needed

### 1.3 Create Opportunity
- Go to **Opportunities** from sidebar
- Click "Create Opportunity"
- Fill in details:
  - Title (e.g., "Software Engineer Intern")
  - Type (Placement/Internship)
  - CTC/Stipend
  - Deadline
  - Max applicants
  - Description
- Save as DRAFT

### 1.4 Add Required Skills
- View your opportunity
- Click "Add Skill" in the Required Skills section
- Add relevant skills (e.g., Python, Django, React)

### 1.5 Publish Opportunity
- Once ready, click "Publish" button
- Opportunity is now visible to students

---

## Phase 2: Student Application (Student)

### 2.1 Login as Student
- Navigate to `/` and login with student credentials
- Complete profile if needed:
  - Go to **Profile** from sidebar
  - Add personal details, CGPA, branch
  
### 2.2 Add Academic Records
- Go to **Academic Records** from sidebar
- Add semester-wise marks

### 2.3 Add Skills
- Go to **Skills** from sidebar
- Add your technical skills

### 2.4 Upload Resume
- Go to **Resumes** from sidebar
- Upload PDF resume
- Set as current resume

### 2.5 Browse & Apply
- Go to **Opportunities** from sidebar
- Browse published opportunities
- Click on opportunity to view details
- Click "Apply" button
- Confirm application

---

## Phase 3: Screening (Recruiter)

### 3.1 View Applications
- Login as Recruiter
- Go to **Applications** from sidebar
- Click on opportunity to view applicants
- OR navigate to **Opportunities** → Select opportunity → "View Applicants"

### 3.2 Set Screening Rules
- From Applicant List, click **Screening** button in workflow bar
- OR directly navigate to `/screening/opportunity/<id>/rule/`
- Set rules:
  - Minimum CGPA (e.g., 7.0)
  - Allowed Branches (e.g., CSE, ECE, EEE)
- Save rules

### 3.3 Run Screening
- Click "Run Screening" button
- System automatically evaluates all applications
- Applications are marked as SHORTLISTED or REJECTED

### 3.4 View Results
- Click "View Results" to see screening outcomes
- See which students passed/failed with reasons

---

## Phase 4: Interviews (Recruiter)

### 4.1 Create Interview Rounds
- From Applicant List, click **Interviews** button
- OR navigate to `/interviews/opportunity/<id>/rounds/`
- Click "Add Interview Round"
- Fill details:
  - Round order (1, 2, 3...)
  - Type (Technical/HR/Group Discussion)
  - Duration (e.g., 60 minutes)
  - Description
- Create multiple rounds as needed

### 4.2 Create Interview Slots
- For each round, click "Manage Slots"
- Click "Create Slot"
- Add:
  - Date & Time
  - Location/Link
  - Interviewer name
- Create multiple slots for different time windows

### 4.3 Assign Students to Slots
- For each round, click "Assign"
- Select shortlisted students
- Assign them to available slots
- Save assignments

### 4.4 Add Interview Feedback
- After interviews, navigate to application
- Click "Add Feedback"
- Fill:
  - Rating (1-5)
  - Comments
  - Overall impression
- Submit feedback

---

## Phase 5: Hiring Decisions (Recruiter)

### 5.1 View Decision Dashboard
- From Applicant List, click **Decisions** button
- OR navigate to `/decisions/opportunity/<id>/`
- See all applications with current status

### 5.2 Make Hiring Decisions
- For each application, click "Add" under Actions
- Select decision:
  - **SELECTED** - Offer will be sent
  - **REJECTED** - Candidate not selected
  - **WAITLIST** - Keep in reserve
- Add comments/justification
- Set offer details if SELECTED:
  - Final CTC/Stipend
  - Joining date
  - Other terms
- Submit decision

### 5.3 View Decision Details
- Click "View" to see complete decision
- Track offer response status

---

## Phase 6: Offer Response (Student)

### 6.1 View Decision
- Login as Student
- Go to Dashboard
- See hiring decision notification

### 6.2 Respond to Offer
- If selected, navigate to offer details
- Choose response:
  - **ACCEPTED** - Accept the offer
  - **REJECTED** - Decline the offer
  - **PENDING** - Still deciding
- Add response comments
- Submit response

---

## Phase 7: Placement Records (Officer)

### 7.1 View All Records
- Login as Officer
- Go to **Placement Records** from sidebar
- OR navigate to `/records/placements/`
- See statistics:
  - Total placements
  - Average package
  - Unique companies

### 7.2 Filter Records
- Use filters:
  - Company
  - Year
  - Minimum package
- View filtered results

### 7.3 Add Placement Record (Manual)
- Navigate to `/records/student/<id>/placements/add/`
- Fill:
  - Student
  - Company
  - Opportunity (if applicable)
  - Position/Role
  - CTC/Stipend
  - Placement date
  - Offer letter (upload)
- Submit record

### 7.4 View Company Statistics
- Click on company in records
- Navigate to `/records/company/<id>/stats/`
- See:
  - Total placements from this company
  - Average package
  - Year-wise breakdown
  - Student list

### 7.5 View Student Placements
- Click on student
- Navigate to `/records/student/<id>/placements/`
- See all placements for that student

---

## Navigation Summary

### Recruiter Dashboard Quick Actions
```
Dashboard → Applications → Select Opportunity → Workflow Bar:
  1. Screening → Set Rules → Run → View Results
  2. Interviews → Create Rounds → Add Slots → Assign Students → Add Feedback
  3. Decisions → Make Decisions → Track Responses
  4. Records → View Final Placements
```

### Opportunity Detail Quick Actions (Recruiter)
```
Opportunity Detail → Sidebar Card "Manage Applications":
  - View Applicants
  - Screening
  - Interviews
  - Decisions
```

### Officer Dashboard Quick Actions
```
Dashboard → Placement Records → Filter/Search → View Details
```

---

## Key URLs Reference

### Opportunities
- List: `/opportunity/`
- Create: `/opportunity/create/`
- Detail: `/opportunity/<id>/`
- Edit: `/opportunity/<id>/edit/`
- Publish: `/opportunity/<id>/publish/`

### Applications
- Recruiter Overview: `/applications/recruiter/`
- Applicant List: `/applications/opportunity/<id>/`
- Apply: `/applications/apply/<opportunity_id>/`

### Screening
- Set Rules: `/screening/opportunity/<id>/rule/`
- Run Screening: `/screening/opportunity/<id>/run/`
- View Results: `/screening/opportunity/<id>/results/`

### Interviews
- Rounds: `/interviews/opportunity/<id>/rounds/`
- Create Round: `/interviews/opportunity/<id>/rounds/create/`
- Slots: `/interviews/round/<id>/slots/`
- Assign: `/interviews/round/<id>/assign/`
- Feedback: `/interviews/application/<id>/feedback/`

### Decisions
- List: `/decisions/opportunity/<id>/`
- Add Decision: `/decisions/application/<id>/decision/add/`
- View Detail: `/decisions/decision/<id>/`
- Offer Response: `/decisions/decision/<id>/response/`

### Records
- All Records: `/records/placements/`
- Student Records: `/records/student/<id>/placements/`
- Add Record: `/records/student/<id>/placements/add/`
- Company Stats: `/records/company/<id>/stats/`

---

## Testing Checklist

- [ ] Recruiter can create and publish opportunity
- [ ] Student can view and apply to opportunity
- [ ] Recruiter can set screening rules and run screening
- [ ] Screening correctly filters applications
- [ ] Recruiter can create interview rounds and slots
- [ ] Recruiter can assign students to interview slots
- [ ] Recruiter can add interview feedback
- [ ] Recruiter can make hiring decisions
- [ ] Student receives decision notification
- [ ] Student can respond to offers
- [ ] Officer can view placement records
- [ ] Officer can filter and search records
- [ ] All navigation links work correctly
- [ ] All forms have CSRF tokens
- [ ] All URLs are properly namespaced

---

## Common Issues & Solutions

### Issue: Can't see Screening/Interviews in UI
**Solution:** Use the workflow bar at the top of the Applicant List page, or use the "Manage Applications" card on the Opportunity Detail page.

### Issue: Screening doesn't shortlist anyone
**Solution:** Check your screening rules. Make sure minimum CGPA and branch requirements match at least some applicants.

### Issue: Can't assign students to interview slots
**Solution:** Ensure students are shortlisted first via screening. Only shortlisted students can be assigned to interviews.

### Issue: Student can't respond to offer
**Solution:** Ensure recruiter has made a decision with result="SELECTED". Only selected candidates can respond to offers.

### Issue: Records not showing
**Solution:** Placement records are created when a student accepts an offer. Make sure the complete flow from decision → offer → acceptance is completed.

---

## Notes

- All forms include CSRF protection
- Role-based access control is enforced
- Officer approval required for companies and student registrations
- Students can only apply once per opportunity
- Applications can be withdrawn before deadline
- Screening can be re-run multiple times
- Interview feedback helps in making decisions
- Records are automatically created when offers are accepted
- Navigation is intuitive with workflow bars guiding the process

