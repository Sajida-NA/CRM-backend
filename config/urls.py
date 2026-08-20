"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,

)
from apps.accounts.views import TestView
urlpatterns = [
    path('admin/', admin.site.urls),
    
    path("api/accounts/", include("apps.accounts.urls")),

    path("api/", include("apps.companies.urls")),

    path("api/leads/",include("apps.leads.urls")),
    
    path("api/deals/",include("apps.deals.urls")),

    path("api/tickets/", include("apps.tickets.urls")),
    
# Activities
    path("api/activities/activity/", include("apps.activities.activity.urls")),

    # path("api/activities/call/", include("apps.activities.call.urls")),

    path("api/activities/email/", include("apps.activities.email.urls")),

    path("api/activities/meeting/", include("apps.activities.meeting.urls")),

    path("api/activities/note/", include("apps.activities.note.urls")),

   

    path("api/token/",TokenObtainPairView.as_view(), name="token_obtain_pair",),

    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh",),

    # path("api/test/", TestView.as_view()),

]
