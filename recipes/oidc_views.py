import secrets
import requests
from django.conf import settings
from django.shortcuts import redirect


def oidc_login(request):
    state = secrets.token_urlsafe(24)
    request.session["oidc_state"] = state

    auth_url = (
        f"{settings.KEYCLOAK_BASE_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/auth"
        f"?client_id={settings.KEYCLOAK_CLIENT_ID}"
        f"&response_type=code"
        f"&scope=openid"
        f"&redirect_uri={settings.KEYCLOAK_REDIRECT_URI}"
        f"&state={state}"
    )
    return redirect(auth_url)


def oidc_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")

    if not code or not state or state != request.session.get("oidc_state"):
        return redirect("recipes:list")

    token_url = f"{settings.KEYCLOAK_BASE_URL}/realms/{settings.KEYCLOAK_REALM}/protocol/openid-connect/token"

    data = {
        "grant_type": "authorization_code",
        "client_id": settings.KEYCLOAK_CLIENT_ID,
        "client_secret": settings.KEYCLOAK_CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.KEYCLOAK_REDIRECT_URI,
    }

    r = requests.post(token_url, data=data, timeout=10)
    r.raise_for_status()
    token_data = r.json()

    request.session["access_token"] = token_data.get("access_token")
    request.session["refresh_token"] = token_data.get("refresh_token")

    return redirect("recipes:list")


def oidc_logout(request):
    request.session.pop("access_token", None)
    request.session.pop("refresh_token", None)
    request.session.pop("oidc_state", None)
    return redirect("recipes:list")