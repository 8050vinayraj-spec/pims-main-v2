from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseForbidden
from django.db.models import Q, Avg, Count
from companies.models import RecruiterProfile, Company
from students.models import StudentProfile
from .models import PlacementRecord
from .forms import PlacementRecordForm, PlacementFilterForm


@login_required
def placement_records_view(request):
    """List placement records based on user role"""
    # Check user role
    is_officer = hasattr(request.user, 'role') and request.user.role == 'OFFICER'
    is_recruiter = RecruiterProfile.objects.filter(user=request.user).exists()
    
    if not (is_officer or is_recruiter):
        return HttpResponseForbidden("You don't have permission to view records.")
    
    records = PlacementRecord.objects.select_related('student', 'company')
    
    # Filter by company if recruiter
    if is_recruiter:
        recruiter = RecruiterProfile.objects.get(user=request.user)
        records = records.filter(company=recruiter.company)
    
    # Apply search filters
    form = PlacementFilterForm(request.GET)
    if form.is_valid():
        company_search = form.cleaned_data.get('company')
        year = form.cleaned_data.get('year')
        min_package = form.cleaned_data.get('min_package')
        
        if company_search:
            records = records.filter(company__name__icontains=company_search)
        if year:
            records = records.filter(placement_year=year)
        if min_package:
            records = records.filter(package__gte=min_package)
    
    # Calculate stats
    stats = {
        'total_placements': records.count(),
        'avg_package': records.aggregate(avg=Avg('package'))['avg'],
        'unique_companies': records.values('company').distinct().count(),
    }
    
    context = {
        'records': records,
        'form': form,
        'stats': stats,
        'is_officer': is_officer,
    }
    return render(request, 'records/placement_records.html', context)


@login_required
def placement_reports_view(request):
    """Officer-only placement reports"""
    if not (hasattr(request.user, 'role') and request.user.role == 'OFFICER'):
        return HttpResponseForbidden("Only officers can view reports.")

    records = PlacementRecord.objects.select_related('student', 'company')

    stats = {
        'total_placements': records.count(),
        'avg_package': records.aggregate(avg=Avg('package'))['avg'] or 0,
        'max_package': records.aggregate(max=Max('package'))['max'] or 0,
        'min_package': records.aggregate(min=Min('package'))['min'] or 0,
        'unique_companies': records.values('company').distinct().count(),
    }

    by_year = records.values('placement_year').annotate(
        count=Count('id'),
        avg_package=Avg('package')
    ).order_by('-placement_year')

    by_company = records.values('company__name').annotate(
        count=Count('id'),
        avg_package=Avg('package')
    ).order_by('-count')[:10]

    context = {
        'stats': stats,
        'by_year': by_year,
        'by_company': by_company,
    }
    return render(request, 'records/placement_reports.html', context)


@login_required
def add_placement_record_view(request, student_id):
    """Add placement record for a student (Officer only)"""
    if not (hasattr(request.user, 'role') and request.user.role == 'OFFICER'):
        return HttpResponseForbidden("Only officers can add placement records.")
    
    student = get_object_or_404(StudentProfile, id=student_id)
    
    if request.method == 'POST':
        form = PlacementRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.student = student
            try:
                record.save()
                messages.success(request, f"Placement record created for {student.user.get_full_name()}")
                return redirect('records:placement-records')
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
    else:
        form = PlacementRecordForm()
    
    context = {
        'form': form,
        'student': student,
        'page_title': 'Add Placement Record',
    }
    return render(request, 'records/add_placement_record.html', context)


@login_required
def student_placements_view(request, student_id):
    """View placement records for a specific student"""
    student = get_object_or_404(StudentProfile, id=student_id)
    
    # Check permissions
    is_student = StudentProfile.objects.filter(
        user=request.user
    ).filter(user=student.user).exists()
    is_officer = hasattr(request.user, 'role') and request.user.role == 'OFFICER'
    
    if not (is_student or is_officer):
        return HttpResponseForbidden("You don't have permission.")
    
    records = PlacementRecord.objects.filter(
        student=student
    ).select_related('company')
    
    context = {
        'student': student,
        'records': records,
    }
    return render(request, 'records/student_placements.html', context)


@login_required
def company_placement_stats_view(request, company_id):
    """View placement statistics for a company (Recruiter only)"""
    company = get_object_or_404(Company, id=company_id)
    
    # Check if user is recruiter for this company
    try:
        recruiter = RecruiterProfile.objects.get(user=request.user)
        if recruiter.company != company:
            return HttpResponseForbidden("You don't have permission.")
    except RecruiterProfile.DoesNotExist:
        return HttpResponseForbidden("Only recruiters can view stats.")
    
    records = PlacementRecord.objects.filter(company=company).select_related('student')
    
    # Calculate statistics
    stats = {
        'total_placements': records.count(),
        'avg_package': records.aggregate(avg=Avg('package'))['avg'] or 0,
        'max_package': records.aggregate(max=Max('package'))['max'] or 0,
        'min_package': records.aggregate(min=Min('package'))['min'] or 0,
        'by_year': records.values('placement_year').annotate(count=Count('id')),
    }
    
    context = {
        'company': company,
        'records': records,
        'stats': stats,
    }
    return render(request, 'records/company_placement_stats.html', context)


from django.db.models import Max, Min

