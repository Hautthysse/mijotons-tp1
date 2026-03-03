from django import forms

class RecipeForm(forms.Form):
    title = forms.CharField(max_length=120)
    category = forms.ChoiceField(choices=[
        ("entree", "Entrée"),
        ("plat", "Plat"),
        ("dessert", "Dessert"),
        ("cocktail", "Cocktail"),
    ])
    prep_time = forms.IntegerField(min_value=0, required=False, initial=0)
    servings = forms.IntegerField(min_value=1, required=False, initial=1)
    difficulty = forms.CharField(max_length=30, required=False, initial="facile")
    ingredients = forms.CharField(widget=forms.Textarea, required=False)
    steps = forms.CharField(widget=forms.Textarea, required=False)
    utensils = forms.CharField(widget=forms.Textarea, required=False)
    image = forms.CharField(max_length=255, required=False)