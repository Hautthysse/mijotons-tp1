from django.shortcuts import render
from .data import RECIPES

CATEGORIES = {
    "entree": "Entrée",
    "plat": "Plat",
    "dessert": "Dessert",
    "cocktail": "Cocktail",
}


def recipe_list(request):
    q = (request.GET.get("q") or "").strip().lower()
    cat = (request.GET.get("cat") or "").strip().lower()

    recipes = RECIPES

    if cat:
        recipes = [r for r in recipes if r["category"] == cat]

    if q:
        recipes = [r for r in recipes if q in r["title"].lower()]

    # Ajoute un libellé de catégorie utilisable directement dans le template
    for r in recipes:
        r["category_label"] = CATEGORIES.get(r["category"], r["category"])

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
    recipe = next((r for r in RECIPES if r["id"] == recipe_id), None)

    if recipe is None:
        return render(
            request,
            "recipes/not_found.html",
            {"recipe_id": recipe_id},
            status=404,
        )

    context = {
        "title": recipe["title"],
        "recipe": recipe,
        "category_label": CATEGORIES.get(recipe["category"], recipe["category"]),
    }
    return render(request, "recipes/detail.html", context)