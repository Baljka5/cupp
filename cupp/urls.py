"""
xbook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.conf import settings

from django.contrib.auth import views as auth_views
from cupp.common import views as common_views
from cupp.point import views as point_views
from cupp.point.views import get_districts
from cupp.license import views_lic as license_views
from cupp.event import views_event as event_views

urlpatterns = [

    path('ajax/get_districts/', get_districts, name='ajax_get_districts'),
    path('', auth_views.LoginView.as_view(redirect_authenticated_user=True), name='login'),

    path('groups/', point_views.display_groups, name='display-groups'),
    path('', point_views.index, name='event_index'),
    # path('register-license/', license_views.MainTableCreateView, name='register_license'),
    path('event-index/', event_views.index, name='event_index'),
    path('event-create', event_views.event_addnew, name='event-create'),
    path('event-edit/<int:id>', event_views.edit, name='event-edit'),
    path('event-update/<int:id>', event_views.update, name='event_update'),
    path('event-delete/<int:id>', event_views.destroy, name='event_destroy'),

    path('register-license/', license_views.index, name='index'),
    path('addnew', license_views.addnew, name='addnew'),
    path('edit/<int:id>', license_views.edit, name='edit'),
    path('update/<int:id>', license_views.update, name='update'),
    path('delete/<int:id>', license_views.destroy, name='destroy'),

    path('map/', common_views.Map.as_view(), name='map'),
    path('my-settings/', common_views.MySettings.as_view(), name='my_settings'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('create/', point_views.Create.as_view(), name='point_create'),
    path('edit/<int:pk>/', point_views.Edit.as_view(), name='point_edit'),
    path('delete/<int:pk>/', point_views.Delete.as_view(), name='point_delete'),
    path('info/<int:pk>/', point_views.AjaxInfo.as_view(), name='point_ajax_info'),
    path('detail/<int:pk>/', point_views.Detail.as_view(), name='point_detail'),
    path('ajax-points/', point_views.AjaxList.as_view(), name='point_ajax_list'),

    path('password-change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password-recover/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password-recover/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title = 'PP Management'
admin.site.site_header = 'PP Management'
admin.site.index_title = 'Administration'
