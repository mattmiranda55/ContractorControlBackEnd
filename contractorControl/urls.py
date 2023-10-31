"""contractorControl URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path
from contractorControl import views

urlpatterns = [
    path("admin/", admin.site.urls),

    # time clock endpoints
    path("api/clock-in/", views.clock_in),
    path("api/clock-out/", views.clock_out),
    path("api/time-clock/<int:employee_id>/", views.get_employee_time_clocks),
    path("api/all-time-clocks/", views.get_all_time_clocks),

    # inventory endpoints
    path("api/create-new-item/", views.create_new_item),
    path("api/update-item-quantity/", views.update_item_quantity),
]
