from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StudentProfile, AcademicRecord, StudentSkill, Skill, Resume
from .forms import (
    StudentProfileForm, AcademicRecordForm, StudentSkillForm,
    AddSkillForm, ResumeUploadForm
)

# ---------------- Dashboard & Profile ----------------

@login_required
def student_dashboard_view(request):
    """Student dashboard showing profile overview"""
    if request.user.role.upper() != 'STUDENT':
        messages.error(request, 'You do not have access to this page.')
        return redirect('home')
    
    try:
        student = request.user.student_profile
    except StudentProfile.DoesNotExist:
        messages.info(request, "Please complete your profile before accessing the dashboard.")
        return redirect('students:complete_profile')
    
    from applications.models import Application
    
    applications_qs = Application.objects.filter(student=student).select_related(
        'opportunity', 'opportunity__company'
    )
    applications = list(applications_qs.prefetch_related(
        'hiring_decision__offer_response', 'screening_result', 'slot_assignment'
    ))
    
    total_apps = len(applications)
    shortlisted = sum(1 for app in applications if app.status == 'SHORTLISTED')
    offers_made = sum(1 for app in applications if app.hiring_decision and app.hiring_decision.result == 'SELECTED')
    offers_accepted = sum(
        1 for app in applications
        if app.hiring_decision and app.hiring_decision.result == 'SELECTED'
        and app.hiring_decision.offer_response
        and app.hiring_decision.offer_response.response == 'ACCEPTED'
    )
    rejected = sum(1 for app in applications if app.status == 'REJECTED')
    
    pending_offers = [
        app for app in applications
        if app.hiring_decision and app.hiring_decision.result == 'SELECTED'
        and (not app.hiring_decision.offer_response or app.hiring_decision.offer_response.response not in ['ACCEPTED', 'REJECTED'])
    ]
    
    context = {
        'student': student,
        'profile_completion': student.profile_completion_percentage(),
        'applications': applications,
        'total_applications': total_apps,
        'shortlisted': shortlisted,
        'offers_made': offers_made,
        'accepted_offers': offers_accepted,
        'rejected': rejected,
        'pending_offers': pending_offers,
    }
    
    return render(request, 'dashboard/student_dashboard.html', context)

@login_required
def complete_profile_view(request):
    """First-time profile completion for students"""
    if request.user.role.upper() != "STUDENT":
        messages.error(request, "Only students can complete this profile.")
        return redirect('home')

    try:
        _ = request.user.student_profile
        messages.info(request, "Profile already exists.")
        return redirect('dashboard:student_dashboard')
    except StudentProfile.DoesNotExist:
        if request.method == "POST":
            form = StudentProfileForm(request.POST, request.FILES)
            if form.is_valid():
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                messages.success(request, "Profile created successfully!")
                return redirect('dashboard:student_dashboard')
        else:
            form = StudentProfileForm()

        return render(request, 'students/complete_profile.html', {'form': form})

@login_required
def profile_view(request):
    """View and edit student profile"""
    if request.user.role.upper() != 'STUDENT':
        messages.error(request, 'You do not have access to this page.')
        return redirect('home')
    
    try:
        student = request.user.student_profile
    except StudentProfile.DoesNotExist:
        messages.info(request, "Please complete your profile first.")
        return redirect('students:complete_profile')
    
    if request.method == 'POST':
        form = StudentProfileForm(request.POST, request.FILES, instance=student)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = StudentProfileForm(instance=student)
    
    return render(request, 'students/profile.html', {
        'form': form,
        'student': student,
        'profile_completion': student.profile_completion_percentage(),
    })

# ---------------- Academic Records ----------------

@login_required
def academic_records_view(request):
    if request.user.role.upper() != 'STUDENT':
        messages.error(request, 'You do not have access to this page.')
        return redirect('home')
    student = get_object_or_404(StudentProfile, user=request.user)
    academic_records = student.academic_records.all()
    return render(request, 'students/academic_records.html', {
        'student': student,
        'academic_records': academic_records,
    })

@login_required
def add_academic_record_view(request):
    """Add academic record"""
    if request.user.role.upper() != 'STUDENT':
        messages.error(request, 'You do not have access to this page.')
        return redirect('home')
    
    student = get_object_or_404(StudentProfile, user=request.user)
    
    if request.method == 'POST':
        form = AcademicRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.student = student
            record.save()
            messages.success(request, f'Semester {record.semester} record added successfully!')
            return redirect('academic_records')
    else:
        form = AcademicRecordForm()
    
    return render(request, 'students/add_academic_record.html', {'form': form, 'student': student})

@login_required
def edit_academic_record_view(request, record_id):
    """Edit existing academic record"""
    if request.user.role.upper() != 'STUDENT':
        messages.error(request, 'You do not have access to this page.')
        return redirect('home')
    
    student = get_object_or_404(StudentProfile, user=request.user)
    record = get_object_or_404(AcademicRecord, id=record_id, student=student)
    
    if request.method == 'POST':
        form = AcademicRecordForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record updated successfully!')
            return redirect('academic_records')
    else:
        form = AcademicRecordForm(instance=record)
    
    return render(request, 'students/add_academic_record.html', {'form': form, 'student': student, 'record': record})

@login_required
def delete_academic_record_view(request, record_id):
    """Delete academic record"""
    if request.user.role.upper() != 'STUDENT':
        messages.error(request, 'You do not have access to this page.')
        return redirect('home')
    
    student = get_object_or_404(StudentProfile, user=request.user)
    record = get_object_or_404(AcademicRecord, id=record_id, student=student)
    
    if request.method == 'POST':
        record.delete()
        messages.success(request, 'Record deleted successfully!')
        return redirect('academic_records')
    
    return render(request, 'students/confirm_delete_record.html', {'record': record, 'student': student})

# ---------------- Skills ----------------

@login_required
def skills_view(request):
    if request.user.role.upper() != 'STUDENT':
        messages.error(request, 'You do not have access to this page.')
        return redirect('home')
    student = get_object_or_404(StudentProfile, user=request.user)
    skills = student.skills.all()
    return render(request, 'students/skills.html', {'student': student, 'skills': skills})

@login_required
def add_skill_view(request):
    """Add skill to profile"""
    if request.user.role.upper() != 'STUDENT':
        messages.error(request, 'You do not have access to this page.')
        return redirect('home')
    
    student = get_object_or_404(StudentProfile, user=request.user)
    
    if request.method == 'POST':
        if 'skill_id' in request.POST:
            form = StudentSkillForm(request.POST)
            if form.is_valid():
                skill_instance = form.save(commit=False)
                skill_instance.student = student
                skill_instance.save()
                messages.success(request, 'Skill added successfully!')
                return redirect('skills')
        else:
            form = AddSkillForm(request.POST)
            if form.is_valid():
                skill_name = form.cleaned_data['skill_name']
                category = form.cleaned_data['category']
                proficiency = form.cleaned_data['proficiency']
                years = form.cleaned_data['years_of_experience']
                
                skill, _ = Skill.objects.get_or_create(
                    name=skill_name,
                    defaults={'category': category}
                )
                
                StudentSkill.objects.create(
                    student=student,
                    skill=skill,
                    proficiency=proficiency,
                    years_of_experience=years
                )
                messages.success(request, 'Skill added successfully!')
                return redirect('skills')
    else:
        form = StudentSkillForm()
    
    return render(request, 'students/add_skill.html', {'form': form, 'student': student})

@login_required
def delete_skill_view(request, skill_id):
    """Delete skill"""
    if request.user.role.upper() != 'STUDENT':
        messages.error(request, 'You do not have access to this page.')
        return redirect('home')
    
# ---------------- Resumes ----------------

@login_required
def resumes_view(request):
    """View and manage resumes"""
    if request.user.role.upper() != 'STUDENT':
        messages.error(request, 'You do not have access to this page.')
        return redirect('home')
    
    student = get_object_or_404(StudentProfile, user=request.user)
    resumes = student.resumes.all()
    
    return render(request, 'students/resumes.html', {
        'student': student,
        'resumes': resumes,
    })

@login_required
def upload_resume_view(request):
    """Upload new resume version"""
    if request.user.role.upper() != 'STUDENT':
        messages.error(request, 'You do not have access to this page.')
        return redirect('home')
    
    student = get_object_or_404(StudentProfile, user=request.user)
    
    if request.method == 'POST':
        form = ResumeUploadForm(request.POST, request.FILES)
        if form.is_valid():
            resume = form.save(commit=False)
            resume.student = student
            
            # Calculate version number
            last_version = student.resumes.order_by('-version').first()
            resume.version = (last_version.version if last_version else 0) + 1
            
            resume.save()
            messages.success(request, f'Resume v{resume.version} uploaded successfully!')
            return redirect('resumes')
    else:
        form = ResumeUploadForm()
    
    return render(request, 'students/upload_resume.html', {'form': form, 'student': student})

@login_required
def delete_resume_view(request, resume_id):
    """Delete resume version"""
    if request.user.role.upper() != 'STUDENT':
        messages.error(request, 'You do not have access to this page.')
        return redirect('home')
    
    student = get_object_or_404(StudentProfile, user=request.user)
    resume = get_object_or_404(Resume, id=resume_id, student=student)
    
    if request.method == 'POST':
        resume.delete()
        messages.success(request, 'Resume deleted successfully!')
        return redirect('resumes')
    
    return render(request, 'students/confirm_delete_resume.html', {'resume': resume, 'student': student})

@login_required
def set_current_resume_view(request, resume_id):
    """Set resume as current"""
    if request.user.role.upper() != 'STUDENT':
        messages.error(request, 'You do not have access to this page.')
        return redirect('home')
    
    student = get_object_or_404(StudentProfile, user=request.user)
    resume = get_object_or_404(Resume, id=resume_id, student=student)
    
    resume.is_current = True
    resume.save()
    messages.success(request, f'Resume v{resume.version} set as current!')
    return redirect('resumes')