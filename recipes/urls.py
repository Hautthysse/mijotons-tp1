from django.urls import path
from . import views
from . import oidc_views

app_name = "recipes"

urlpatterns = [
    path("", views.recipe_list, name="list"),
    path("recipe/<int:recipe_id>/", views.recipe_detail, name="detail"),

    path("recipe/add/", views.recipe_create, name="add"),
    path("recipe/<int:recipe_id>/edit/", views.recipe_edit, name="edit"),
    path("recipe/<int:recipe_id>/delete/", views.recipe_delete, name="delete"),
    path("oidc/login/", oidc_views.oidc_login, name="oidc_login"),
    path("oidc/callback/", oidc_views.oidc_callback, name="oidc_callback"),
    path("oidc/logout/", oidc_views.oidc_logout, name="oidc_logout"),
]