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
        matched_ingredients = []
        missing_ingredients = []
        
        for recipe_ingredient in recipe_info['ingredients']:
            best_match = None
            best_ratio = 0
            
            for available_ingredient in ingredient_set:
                # Check for brand + ingredient match first
                brand_ingredient_ratio = fuzz.ratio(available_ingredient.lower(), recipe_ingredient.lower())
                if brand_ingredient_ratio > 80:
                    best_match = available_ingredient
                    best_ratio = brand_ingredient_ratio
                    break
                
                # If no brand match, check for partial ingredient match
                words = available_ingredient.lower().split()
                for word in words:
                    partial_ratio = fuzz.partial_ratio(word, recipe_ingredient.lower())
                    if partial_ratio > best_ratio:
                        best_match = available_ingredient
                        best_ratio = partial_ratio
            
            if best_match and best_ratio > 80:
                matched_ingredients.append(best_match)
            else:
                missing_ingredients.append(recipe_ingredient)
        
        # Calculate a match score based on the number of matched ingredients
        match_score = len(matched_ingredients) / len(recipe_info['ingredients'])
        
        # Only recommend recipes with at least one matched ingredient
        if matched_ingredients:
            recommendations.append({
                'recipe': recipe_info['recipe'],
                'description': recipe_info['description'],
                'ingredients': recipe_info['ingredients'],
                'matched_ingredients': matched_ingredients,
                'missing_ingredients': missing_ingredients,
                'steps': recipe_info['steps'],
                'cooking_time': recipe_info['cooking_time'],
                'servings': recipe_info['servings'],
                'category': recipe_info['category'],
                'match_score': match_score
            })
    
    # Sort recommendations by match score, highest first
    recommendations.sort(key=lambda x: x['match_score'], reverse=True)
    
    return recommendations