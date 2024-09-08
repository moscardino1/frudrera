from recipes_config import recipes
from fuzzywuzzy import fuzz

def extract_all_ingredients():
    """Extract all unique ingredients from the recipes."""
    all_ingredients = set()
    for recipe_info in recipes.values():
        all_ingredients.update(recipe_info['ingredients'])
    return all_ingredients

def recommend_recipe(available_ingredients):
    recommendations = []
    ingredient_set = set(available_ingredients)  # Convert to set for faster lookup

    for recipe_key, recipe_info in recipes.items():
        # Check if any ingredient matches
        if any(fuzz.ratio(ingredient.lower(), recipe_ingredient.lower()) > 80 for ingredient in ingredient_set for recipe_ingredient in recipe_info['ingredients']):
            # Find missing ingredients
            missing_ingredients = [ingredient for ingredient in recipe_info['ingredients'] if ingredient not in ingredient_set]
            recommendations.append({
                'recipe': recipe_info['recipe'],
                'description': recipe_info['description'],
                'ingredients': recipe_info['ingredients'],
                'missing_ingredients': missing_ingredients,  # Highlight missing ingredients
                'steps': recipe_info['steps'],
                'cooking_time': recipe_info['cooking_time'],
                'servings': recipe_info['servings'],
                'category': recipe_info['category'],
                'image': recipe_info['image']
            })

    return recommendations