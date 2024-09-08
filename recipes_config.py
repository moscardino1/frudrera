# Configuration file for recipes without hardcoded synonyms

recipes = {
    'tomato': {
        'recipe': 'Tomato Soup',
        'description': 'A warm and comforting soup made with fresh tomatoes and herbs.',
        'ingredients': ['4 ripe tomatoes', '1 onion', '2 cloves garlic', '1 cup vegetable broth', 'Fresh basil', 'Salt', 'Pepper'],
        'steps': [
            'Chop the onions and garlic.',
            'In a pot, sauté onions and garlic until translucent.',
            'Add chopped tomatoes and cook for 10 minutes.',
            'Pour in the vegetable broth and simmer for 20 minutes.',
            'Blend until smooth and season with salt, pepper, and fresh basil.'
        ],
        'cooking_time': '30 minutes',
        'servings': '4',
        'category': 'Soup',
        'image': 'url_to_image_of_tomato_soup'
    },
    'lettuce': {
        'recipe': 'Lettuce Salad',
        'description': 'A refreshing salad with crisp lettuce and a tangy dressing.',
        'ingredients': ['1 head of lettuce', '1/2 cup cherry tomatoes', '1/4 cup olives', '2 tbsp olive oil', '1 tbsp vinegar', 'Salt', 'Pepper'],
        'steps': [
            'Wash and chop the lettuce.',
            'Halve the cherry tomatoes and add to the bowl.',
            'Add olives, olive oil, vinegar, salt, and pepper.',
            'Toss everything together and serve chilled.'
        ],
        'cooking_time': '10 minutes',
        'servings': '2',
        'category': 'Salad',
        'image': 'url_to_image_of_lettuce_salad'
    },
    'cheese': {
        'recipe': 'Cheese Sandwich',
        'description': 'A classic sandwich with melted cheese and crispy bread.',
        'ingredients': ['2 slices of bread', '2 slices of cheese', 'Butter'],
        'steps': [
            'Butter one side of each slice of bread.',
            'Place cheese between the unbuttered sides of the bread.',
            'Heat a skillet over medium heat and grill the sandwich until golden brown on both sides.'
        ],
        'cooking_time': '10 minutes',
        'servings': '1',
        'category': 'Snack',
        'image': 'url_to_image_of_cheese_sandwich'
    },
    'chicken': {
        'recipe': 'Grilled Chicken',
        'description': 'Juicy chicken marinated with spices and grilled to perfection.',
        'ingredients': ['2 chicken breasts', '1 tbsp olive oil', '1 tsp paprika', '1 tsp garlic powder', 'Salt', 'Pepper'],
        'steps': [
            'Marinate chicken breasts with olive oil, paprika, garlic powder, salt, and pepper for at least 30 minutes.',
            'Preheat the grill to medium-high heat.',
            'Grill chicken for 6-7 minutes on each side or until fully cooked.'
        ],
        'cooking_time': '40 minutes (including marination)',
        'servings': '2',
        'category': 'Main Course',
        'image': 'url_to_image_of_grilled_chicken'
    },
    'pasta': {
        'recipe': 'Pasta Aglio e Olio',
        'description': 'A simple yet flavorful pasta dish with garlic and olive oil.',
        'ingredients': ['200g spaghetti', '4 cloves garlic', '1/2 cup olive oil', 'Red pepper flakes', 'Parsley', 'Salt'],
        'steps': [
            'Cook spaghetti according to package instructions.',
            'In a pan, heat olive oil and sauté minced garlic until golden.',
            'Add red pepper flakes and cooked spaghetti to the pan.',
            'Toss with chopped parsley and serve immediately.'
        ],
        'cooking_time': '20 minutes',
        'servings': '2',
        'category': 'Pasta',
        'image': 'url_to_image_of_pasta_aglio_e_olio'
    },
    'tiramisu': {
        'recipe': 'Tiramisu',
        'description': 'A classic Italian dessert made with coffee-soaked ladyfingers and mascarpone cheese.',
        'ingredients': ['250g mascarpone cheese', '3 eggs', '100g sugar', '200ml coffee', '200g ladyfingers', 'Cocoa powder'],
        'steps': [
            'Whisk egg yolks with sugar until creamy.',
            'Add mascarpone cheese and mix well.',
            'Dip ladyfingers in coffee and layer in a dish.',
            'Spread mascarpone mixture over the ladyfingers and repeat layers.',
            'Chill for at least 4 hours and dust with cocoa powder before serving.'
        ],
        'cooking_time': '30 minutes (plus chilling time)',
        'servings': '6',
        'category': 'Dessert',
        'image': 'url_to_image_of_tiramisu'
    },
    'pasta_ragu': {
        'recipe': 'Pasta al Ragu',
        'description': 'A hearty pasta dish with a rich meat sauce.',
        'ingredients': ['400g pasta (tagliatelle or pappardelle)', '300g ground beef', '1 onion', '2 cloves garlic', '1 carrot', '1 celery stalk', '400g canned tomatoes', '1/2 cup red wine', 'Olive oil', 'Salt', 'Pepper', 'Parmesan cheese'],
        'steps': [
            'Chop the onion, garlic, carrot, and celery finely.',
            'In a large pan, heat olive oil and sauté the chopped vegetables until soft.',
            'Add the ground beef and cook until browned.',
            'Pour in the red wine and let it evaporate.',
            'Add the canned tomatoes, salt, and pepper. Simmer for 30-40 minutes.',
            'Cook the pasta according to package instructions. Drain and mix with the ragu sauce.',
            'Serve with grated Parmesan cheese on top.'
        ],
        'cooking_time': '1 hour',
        'servings': '4',
        'category': 'Main Course',
        'image': 'url_to_image_of_pasta_ragu'
    },
}