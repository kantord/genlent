import random


# each ingredient should have nutrient stats per 100g
ingredients = [
    {
        # in 100g
        "name": "AbsoRice Pea Protein",
        "price": 2499 / 350.0 * 100.0,
        "calories": 366,  # kcal
        "fat": 4,  # grams
        "carbs": 1.8,  # grams
        "protein": 81.7,
    },
    {
        # in 100g
        "name": "Oatmeal",
        "price": 199 / 500.0 * 100.0,
        "calories": 372,  # kcal
        "fat": 7.0,  # grams
        "carbs": 58.7,  # grams
        "protein": 13.5,
    },
#     {
        # # in 100g
        # "name": "Peanut Butter",
        # "price": 999 / 500.0 * 100.0,
        # "calories": 634,  # kcal
        # "fat": 53,  # grams
        # "carbs": 8.5,  # grams
        # "protein": 27.0,
    # },
    {
        # in 100g
        "name": "Maltodextrin",
        "price": 1090 / 1000.0 * 100.0,
        "calories": 380,  # kcal
        "fat": 0,  # grams
        "carbs": 94,  # grams
        "protein": 0,
    },
    {
        # in 100g
        "name": "Soy flour",
        "price": 674 / 1000.0 * 100.0,
        "calories": 289,  # kcal
        "fat": 2,  # grams
        "carbs": 21,  # grams
        "protein": 47,
    },
    {
        # in 100g
        "name": "Peanuts",
        "price": 1179 / 1000.0 * 100.0,
        "calories": 560,  # kcal
        "fat": 47,  # grams
        "carbs": 19,  # grams
        "protein": 25,
    },
    {
            # in 100g
            "name": "Bananas",
            "price": 390 / 1000.0 * 100.0,
            "calories": 89,  # kcal
            "fat": 0.33,  # grams
            "carbs": 23,  # grams
            "protein": 1,
    },
    {
            # in 100g
            "name": "Flaxseed oil",
            "price": 220 / 1000.0 * 100.0,
            "calories": 884,  # kcal
            "fat": 100,  # grams
            "carbs": 0,  # grams
            "protein": 0,
    },
]


# source: http://daa.asn.au/for-the-public/smart-eating-for-you/nutrition-a-z/daily-intake-guide/

calorie_goal = 2000
protein_goal = 150
fat_goal = 70
carbs_goal = 310
price_goal = 300
number_of_ingredients_goal = 5


def get_random_recipe():
    return list(map(lambda _: random.uniform(0.0, 10.0), ingredients))


def get_inital_gene_pool(count=10000):
    return list(map(lambda _: get_random_recipe(), range(count)))


def get_gene_score_calories(gene):
    return float(calorie_goal - sum(
        amount * ingredients[ingredient]["calories"]
        for ingredient, amount in enumerate(gene)))


def get_gene_score_protein(gene):
    return float(protein_goal - sum(
        amount * ingredients[ingredient]["protein"]
        for ingredient, amount in enumerate(gene)))


def get_gene_score_fat(gene):
    return float(fat_goal - sum(
        amount * ingredients[ingredient]["fat"]
        for ingredient, amount in enumerate(gene)))


def get_score_price(gene):
    return float(sum(
        amount * ingredients[ingredient]["price"]
        for ingredient, amount in enumerate(gene)))


def generate_score_function(attribute, goal):
    def score(gene):
        return float(goal - sum(
            amount * ingredients[ingredient][attribute]
            for ingredient, amount in enumerate(gene))) / goal * 100

    return score


def generate_score_function_only_upper_limit(attribute, goal):
    def score(gene):
            result = sum(
                amount * ingredients[ingredient][attribute]
                for ingredient, amount in enumerate(gene))

            if result > goal:
                return result * 100 / goal
            else:
                return 0

    return score


def number_of_ingredients_score(gene):
    return number_of_ingredients_goal - len([amount for amount in gene if amount >= 1.0]) * 100 / number_of_ingredients_goal


scores = {
    "calories": generate_score_function("calories", goal=calorie_goal),
    "protein": generate_score_function("protein", goal=protein_goal),
    "fat": generate_score_function("fat", goal=fat_goal),
    "carbs": generate_score_function("carbs", goal=carbs_goal),
    # "number_of_ingredients": number_of_ingredients_score,
    "price": generate_score_function_only_upper_limit("price", goal=price_goal),
    # "price": get_score_price,
}


def randomize_gene(gene):
    return list(map(lambda i: i * random.uniform(0.9, 1.1), gene))


def randomize_pool(pool):
    return [randomize_gene(gene) for gene in pool]


pool = get_inital_gene_pool()
for generation in range(1000):
    print("Generation #%d" % generation)
    # score = random.choice(list(scores.values()))

    def score(gene):
        return sum(abs(f(gene)) for f in scores.values())

    best_gene = min(pool, key=lambda gene: score(gene))
    best_gene_r = tuple("%dg %s" % (int(amount * 100), ingredients[i]["name"]) for i, amount in enumerate(best_gene) if int(amount * 100))
    print("Best gene: %s; Score: %s; Price %d Ft" % (best_gene_r, {key: -score(best_gene) for key, score in scores.items()}, sum(amount * ingredients[i]["price"] for i, amount in enumerate(best_gene))))
    # pool = [best_gene] * 5000 + pool[0:(len(pool) - 5000)]
    new_pool = list(sorted(pool, key=score)[0:500]) * 10 + pool[0:5000]
    pool = randomize_pool(new_pool)
