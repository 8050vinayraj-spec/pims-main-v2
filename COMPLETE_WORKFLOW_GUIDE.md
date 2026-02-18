# PIMS Complete Workflow Guide

## 📋 Complete End-to-End Flow

### **PHASE 1: RECRUITER - Job Publishing**
1. Recruiter logs in → Dashboard
2. Navigate to **Companies** → Select/Add company
3. **Opportunities** → Create new opportunity
4. Fill: Title, Description, CTC, Deadline, Max Applicants
5. Add required skills
6. **Publish** the opportunity

---

### **PHASE 2: STUDENT - Application**
1. Student logs in → **Opportunities**
2. Browse and click on an opportunity
3. Click **"Apply"** button
4. Confirm application
5. Application status: **APPLIED**

**Student can see:** Dashboard shows all applications with status

---

### **PHASE 3: RECRUITER - Screening**
1. Recruiter → **Applications** (sidebar)
2. Click on opportunity to view **Applicants**
3. **Screening** button in workflow bar
4. Set minimum CGPA and allowed branches
5. Click **"Run Screening"**
6. View **Screening Results**

**Application Status:** Still **APPLIED** (auto-screened in backend)

---

### **PHASE 4: RECRUITER - Manual Shortlisting**
1. Recruiter → **Applications** → View **Applicants**
2. For each student, use **Action Buttons:**
   - **Shortlist** - Mark as SHORTLISTED
   - **Reject** - Mark as REJECTED
3. Can undo by toggling status

**Application Status:** Changes to **SHORTLISTED** or **REJECTED**

---

### **PHASE 5: RECRUITER - Interview Scheduling**
1. Recruiter → **Interviews** (from workflow)
2. **Create Interview Rounds:**
   - Click **"Add Interview Round"**
   - Select round type (Technical, HR, etc.)
   - Set duration
3. **Create Interview Slots:**
   - Click round → **Manage Slots**
   - Click **"Add Slot"**
   - Set date, time, location
4. **Assign Students:**
   - Click **"Assign Students"** button (if students are shortlisted)
   - Select students from checkbox list
   - Select interview slot
   - Click **"Assign Students"**

**What's needed for slot assignment:**
- Students must be **SHORTLISTED** first (Phase 4)

**Interview Slot Statuses:**
- **AVAILABLE** → Empty slot, can assign students
- **BOOKED** → Students assigned, can add feedback
- **COMPLETED** → Interview done

---

### **PHASE 6: RECRUITER - Add Interview Feedback**
1. After conducting interviews
2. Go to **Interview Slots** → Students assigned to slot
3. Click student name to add feedback
4. Fill: Interviewer name, comments, result (PASS/FAIL), rating
5. Save feedback

**This marks slot as COMPLETED**

---

### **PHASE 7: RECRUITER - Make Hiring Decisions**
1. Recruiter → **Decisions** (from workflow)
2. View all shortlisted applicants
3. Click **"Add"** button next to each student
4. **Decision Options:**
   - ✅ **SELECTED** - Student gets offer
   - ❌ **REJECTED** - Student doesn't get offer
   - ⏳ **WAITLIST** - Hold for future consideration
5. Add optional comments
6. Click **"Save Decision"**

**Application Status:** Remains SHORTLISTED, but now has a Decision

---

### **PHASE 8: STUDENT - Respond to Offer**
**Student receives notification:**
1. Login → **My Dashboard**
2. See **"Pending Offers"** alert at top (if SELECTED)
3. Shows all pending offers with **"Respond Now"** button
4. Table shows all applications with columns:
   - Opportunity
   - Company
   - Application Status (APPLIED/SHORTLISTED/REJECTED)
   - Screening Result
   - Interview Status
   - **Decision** (SELECTED/REJECTED/WAITLIST)
   - **Offer Response** (This is what student fills)
   - Action buttons

5. Click **"Respond Now"** or **"Respond"** button
6. Choose response:
   - ✅ **ACCEPTED** - Accept the offer
   - ❌ **REJECTED** - Reject the offer
   - ⏳ **PENDING** - Keep it pending
7. Add optional comments
8. Click **"Submit Response"**

**Once Accepted:**
- Officer can now create placement record
- Application shows "✓ Accepted" in Offer Response column

---

### **PHASE 9: OFFICER - Create Placement Record**
**Only after student ACCEPTS offer:**
1. Officer logs in → Sidebar **"Placement Records"**
2. Click **"Add Placement Record"** OR Go to **"Add Record"**
3. Fill:
   - Student (dropdown)
   - Company
   - Position/Designation
   - Package (LPA)
   - Placement Date
   - Status (PLACED/PENDING)
4. Save record

**Result:** Placement recorded in archive

---

### **PHASE 10: OFFICER - View Placement Records**
1. Officer → **Placement Records** (sidebar)
2. View all placements with statistics:
   - Total Placements
   - Average Package
   - Number of Companies
3. Filter by company, year, minimum package
4. View student-wise placements
5. View company-wise statistics

---

## 🎯 Key Status Transitions

```
APPLICATION LIFECYCLE:
APPLIED → SHORTLISTED → (Interview) → Decision Made → Offer Response → ACCEPTED/REJECTED

SCREENING:
- Automatic based on criteria (CGPA, Branch)
- Results shown to recruiter
- Does NOT change application status

DECISION:
- Created manually by recruiter
- Options: SELECTED, REJECTED, WAITLIST
- Sent to student if SELECTED

OFFER RESPONSE:
- Only for SELECTED decisions
- Student can: ACCEPT, REJECT, PENDING
- Once ACCEPTED, placement record can be created
```

---

## 📊 What Everyone Sees

### **RECRUITER Dashboard Shows:**
- Total opportunities, applications, selected students, accepted offers
- Table: Student, Opportunity, Status, Applied Date
- Quick access to applicants, screening, interviews, decisions

### **STUDENT Dashboard Shows:**
- Statistics: Applications, Shortlisted, Offers Made, Accepted, Rejections
- **Pending Offers Alert** (if any SELECTED decisions waiting for response)
- **Complete table with all columns:**
  - Opportunity → Company
  - Application Status (APPLIED/SHORTLISTED/REJECTED)
  - Screening (ELIGIBLE/NOT_ELIGIBLE/PENDING)
  - Interview (SCHEDULED/COMPLETED/-)
  - Decision (SELECTED/REJECTED/WAITLIST/PENDING)
  - Offer Response (ACCEPTED/REJECTED/PENDING/AWAITING)
  - Action button (Respond if SELECTED, View if decision exists)

### **OFFICER Dashboard Shows:**
- Company placements, revenue impact, hiring trends
- Access to **Placement Records**
- Filter and statistics

---

## ✅ Proper Workflow Checklist

- [ ] Recruiter publishes job opportunity
- [ ] Students apply for opportunities
- [ ] Recruiter runs screening (auto-filters based on CGPA/branch)
- [ ] Recruiter manually shortlists students (from applicants list)
- [ ] Recruiter creates interview rounds and slots
- [ ] Recruiter assigns shortlisted students to slots
- [ ] Recruiter conducts interviews and adds feedback
- [ ] Recruiter makes hiring decisions (SELECTED/REJECTED/WAITLIST)
- [ ] Student receives notification and sees in dashboard
- [ ] Student clicks "Respond Now" to accept/reject offer
- [ ] Once ACCEPTED, officer creates placement record
- [ ] Officer views placement records and statistics

---

## 🔗 Key URLs by Role

### Recruiter:
- `/opportunity/` - List opportunities
- `/opportunity/create/` - Create opportunity
- `/opportunity/{id}/` - View opportunity (with workflow buttons)
- `/applications/` - View applications overview
- `/applications/opportunity/{id}/applicants/` - View applicants (with shortlist/reject)
- `/screening/opportunity/{id}/rule/` - Set screening rules
- `/interviews/opportunity/{id}/rounds/` - Interview rounds
- `/interviews/round/{id}/assign/` - Assign students to slots
- `/decisions/opportunity/{id}/` - Make hiring decisions

### Student:
- `/dashboard/student/` - My dashboard (see all applications & offers)
- `/opportunity/` - Browse opportunities
- `/opportunity/{id}/` - Apply to opportunity
- `/decisions/decision/{id}/response/` - Respond to offer (from dashboard or email)

### Officer:
- `/dashboard/officer/` - Officer dashboard
- `/records/placements/` - View placement records
- `/records/student/{id}/placements/add/` - Add placement record

---

## 💡 Important Notes

1. **Student must be SHORTLISTED before assignment** - Interview slot assignment requires SHORTLISTED status
2. **Decision is independent of application status** - Making a decision doesn't change APPLIED/SHORTLISTED status
3. **Offer response only for SELECTED** - If decision is REJECTED/WAITLIST, no offer response needed
4. **Placement record requires student to ACCEPT** - Officer should only create record after acceptance
5. **All status changes are logged** - ApplicationLog tracks every status change

---

## 🚀 Summary Flow in One Sentence

**Job Published → Student Applies → Recruiter Shortlists → Interviews → Decision Made → Student Accepts → Officer Records Placement**
