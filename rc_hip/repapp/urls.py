"""
Urls of RepApp.
"""
from django.urls import path
from . import views

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path(
        "cafe/<int:cafe>/",
        views.RegisterDeviceFormView.as_view(),
        name="register_device"
    ),
    path(
        "cafe/<int:cafe>/device/<str:device_identifier>/mail/<str:mail>/",
        views.RegisterGuestFormView.as_view(),
        name="register_guest"
    ),
    path("cafe/<int:cafe>/device/<str:device_identifier>/confirm/",
         views.register_device_final, name="register_device_final"),
    path("device/<str:device_identifier>/",
         views.device_view, name="view_device"),
    path("guest/profile/",
         views.profile, name="guest_profile"),
    path("onetimelogin/<str:secret>/",
         views.one_time_login, name="one_time_login"),
    path("member/", views.member, name="member"),
    path("member/settings/", views.MemberSettingsFormView.as_view(),
         name="member_settings"),
    path("logout/", views.user_logout, name="logout"),
    path("orga/select/", views.select_role, name="select_role"),
    path("orga/", views.orga, name="orga"),
    path("orga/review/<int:device>/", views.review_device, name="review_device"),
    path("orga/review/<int:device>/accept/",
         views.review_device_accept, name="review_device_accept"),
    path("orga/review/<int:device>/reject/",
         views.RejectDeviceFormView.as_view(), name="review_device_reject"),
    path("member/device/<int:device>/question/",
         views.QuestionDeviceFormView.as_view(), name="device_question"),
    path("member/device/<int:pk>/question/edit",
         views.QuestionUpdateView.as_view(), name="edit_device_question"),
    path("member/question/<int:question>/",
         views.question, name="view_device_question"),
    path("member/question/",
         views.questions, name="device_questions"),
    path("repa/", views.repa, name="repa"),
    path("cafe/", views.CafeView.as_view(), name="cafe"),
    path("cafe/create", views.CafeCreateView.as_view(), name="create_cafe"),
    path("cafe/<int:pk>/edit", views.CafeUpdateView.as_view(), name="edit_cafe"),
    path("cafe/<int:pk>/delete",
         views.CafeDeleteView.as_view(), name="delete_cafe"),
    path("guest/", views.GuestView.as_view(), name="guest"),
    path("guest/<int:pk>/edit", views.GuestUpdateView.as_view(), name="edit_guest"),
    path("cron", views.cron, name="cron"),
    path("bootstrap", views.bootstrap, name="bootstrap"),
    path("process_mails", views.process_mails, name="process_mails"),
]
