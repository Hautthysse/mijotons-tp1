import requests
from django.conf import settings
from django.shortcuts import render, redirect
from .forms import RecipeForm

CATEGORIES = {
    "entree": "Entrée",
    "plat": "Plat",
    "dessert": "Dessert",
    "cocktail": "Cocktail",
}


def _auth_headers(request):
    token = request.session.get("access_token")
    if not token:
        return None
    return {"Authorization": f"Bearer {token}"}


def recipe_list(request):
    q = (request.GET.get("q") or "").strip().lower()
    cat = (request.GET.get("cat") or "").strip().lower()

    resp = requests.get(f"{settings.API_BASE_URL}/recipes", timeout=5)
    resp.raise_for_status()
    recipes = resp.json()

    if cat:
        recipes = [r for r in recipes if r.get("category") == cat]
    if q:
        recipes = [r for r in recipes if q in (r.get("title") or "").lower()]

    for r in recipes:
        r["category_label"] = CATEGORIES.get(r.get("category"), r.get("category"))

    context = {
        "title": "Mijotons",
        "recipes": recipes,
        "selected_cat": cat,
        "query": q,
        "count": len(recipes),
        "categories": CATEGORIES,
    }
    return render(request, "recipes/list.html", context)


def recipe_detail(request, recipe_id: int):
    resp = requests.get(f"{settings.API_BASE_URL}/recipes/{recipe_id}", timeout=5)
    if resp.status_code == 404:
        return render(request, "recipes/not_found.html", {"recipe_id": recipe_id}, status=404)
    resp.raise_for_status()
    recipe = resp.json()

    recipe["category_label"] = CATEGORIES.get(recipe.get("category"), recipe.get("category"))
    recipe["ingredients_list"] = [x.strip() for x in (recipe.get("ingredients") or "").splitlines() if x.strip()]
    recipe["steps_list"] = [x.strip() for x in (recipe.get("steps") or "").splitlines() if x.strip()]
    recipe["utensils_list"] = [x.strip() for x in (recipe.get("utensils") or "").splitlines() if x.strip()]

    return render(request, "recipes/detail.html", {"title": recipe.get("title", "Recette"), "recipe": recipe})


def recipe_create(request):
    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            headers = _auth_headers(request)
            if headers is None:
                return redirect("recipes:oidc_login")

            payload = form.cleaned_data
            resp = requests.post(
                f"{settings.API_BASE_URL}/recipes",
                json=payload,
                headers=headers,
                timeout=5
            )
            resp.raise_for_status()
            return redirect("recipes:list")
    else:
        form = RecipeForm()

    return render(request, "recipes/recipe_form.html", {"title": "Ajouter une recette", "form": form})


def recipe_edit(request, recipe_id: int):
    resp = requests.get(f"{settings.API_BASE_URL}/recipes/{recipe_id}", timeout=5)
    if resp.status_code == 404:
        return render(request, "recipes/not_found.html", {"recipe_id": recipe_id}, status=404)
    resp.raise_for_status()
    recipe = resp.json()

    if request.method == "POST":
        form = RecipeForm(request.POST)
        if form.is_valid():
            headers = _auth_headers(request)
            if headers is None:
                return redirect("recipes:oidc_login")

            payload = form.cleaned_data
            put = requests.put(
                f"{settings.API_BASE_URL}/recipes/{recipe_id}",
                json=payload,
                headers=headers,
                timeout=5,
            )
            put.raise_for_status()
            return redirect("recipes:detail", recipe_id=recipe_id)
    else:
        form = RecipeForm(initial={
            "title": recipe.get("title", ""),
            "category": recipe.get("category", ""),
            "prep_time": recipe.get("prep_time", 0),
            "servings": recipe.get("servings", 1),
            "difficulty": recipe.get("difficulty", "facile"),
            "ingredients": recipe.get("ingredients", ""),
            "steps": recipe.get("steps", ""),
            "utensils": recipe.get("utensils", ""),
            "image": recipe.get("image", ""),
        })

    return render(request, "recipes/recipe_form.html", {"title": "Modifier la recette", "form": form})


def recipe_delete(request, recipe_id: int):
    resp = requests.get(f"{settings.API_BASE_URL}/recipes/{recipe_id}", timeout=5)
    recipe = None
    if resp.status_code == 200:
        recipe = resp.json()

    if request.method == "POST":
        headers = _auth_headers(request)
        if headers is None:
            return redirect("recipes:oidc_login")

        delete = requests.delete(
            f"{settings.API_BASE_URL}/recipes/{recipe_id}",
            headers=headers,
            timeout=5
        )
        if delete.status_code not in (200, 204, 404):
            delete.raise_for_status()
        return redirect("recipes:list")

    return render(
        request,
        "recipes/recipe_confirm_delete.html",
        {"title": "Supprimer la recette", "recipe": recipe, "recipe_id": recipe_id},
    )