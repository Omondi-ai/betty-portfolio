from django.urls import path
from django.contrib.auth import views as auth_views
from . import studio_views

app_name = "studio"

urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="studio/login.html",
            redirect_authenticated_user=True,
        ),
        name="login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", studio_views.dashboard, name="dashboard"),
    path("profile/", studio_views.profile_edit, name="profile_edit"),
    path("story/", studio_views.story_edit, name="story_edit"),
    path("messages/", studio_views.messages_list, name="messages_list"),
    path("messages/<int:pk>/", studio_views.message_detail, name="message_detail"),
    path("messages/<int:pk>/delete/", studio_views.message_delete, name="message_delete"),
    path("upload-image/", studio_views.upload_image, name="upload_image"),
    path("<slug:section>/", studio_views.section_list, name="section_list"),
    path("<slug:section>/new/", studio_views.section_create, name="section_create"),
    path("<slug:section>/<int:pk>/edit/", studio_views.section_edit, name="section_edit"),
    path("<slug:section>/<int:pk>/delete/", studio_views.section_delete, name="section_delete"),
    path("<slug:section>/<int:pk>/restore/", studio_views.section_restore, name="section_restore"),
    path(
        "<slug:section>/<int:pk>/move/<str:direction>/",
        studio_views.section_move,
        name="section_move",
    ),
]