from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Accounts
    path('', include(('accounts.urls', 'accounts'), namespace='accounts')),

    # Students (with namespace)
    path('students/', include(('students.urls', 'students'), namespace='students')),

    # Companies
    path('companies/', include(('companies.urls', 'companies'), namespace='companies')),

    # Opportunities
    path('opportunity/', include(('opportunities.urls', 'opportunities'), namespace='opportunities')),

    # Applications
    path('applications/', include(('applications.urls', 'applications'), namespace='applications')),

    # Screening
    path('screening/', include(('screening.urls', 'screening'), namespace='screening')),

    # Interviews
    path('interviews/', include(('interviews.urls', 'interviews'), namespace='interviews')),

    # Decisions
    path('decisions/', include(('decisions.urls', 'decisions'), namespace='decisions')),

    # Records
    path('records/', include(('records.urls', 'records'), namespace='records')),

    # Dashboard
    path('dashboard/', include(('dashboard.urls', 'dashboard'), namespace='dashboard')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)