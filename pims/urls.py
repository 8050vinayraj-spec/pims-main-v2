from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts
    path('', include('accounts.urls')),

    # Students (with namespace)
    path('student/', include(('students.urls', 'students'), namespace='students')),

    # Companies
    path('', include('companies.urls')),

    # Opportunities
    path('opportunity/', include('opportunities.urls')),

    # Applications
    path('applications/', include(('applications.urls', 'applications'), namespace='applications')),

    # Screening
    path('screening/', include(('screening.urls', 'screening'), namespace='screening')),

    # Interviews
    path('interviews/', include('interviews.urls')),

    # Decisions
    path('decisions/', include('decisions.urls')),

    # Records
    path('records/', include('records.urls')),

    # Dashboard
    path('dashboard/', include('dashboard.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)