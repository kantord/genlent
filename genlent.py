import random


# each ingredient should have nutrient stats per 100g
ingredients = [
    {
        "name": "Peanut Butter",
        "price": 100,
        "calories": 500,
        "fat": 50.0,
        "carbs": 20.0,
        "protein": 30.0,
    },
    {
        "name": "Oat flour",
        "price": 80,
        "calories": 200,
        "fat": 5.0,
        "carbs": 80.0,
        "protein": 15.0,
    },
]

calorie_goal = 2500


def get_random_recipe():
    return list(map(lambda _: random.uniform(0.0, 10.0), ingredients))


def get_inital_gene_pool(count=1000):
    return list(map(lambda _: get_random_recipe(), range(count)))


def get_gene_score(gene):
    # this is only calories for now
    return abs(calorie_goal - sum(
        amount * ingredients[ingredient]["calories"]
        for ingredient, amount in enumerate(gene)))


def randomize_gene(gene):
    return list(map(lambda i: i * random.uniform(0.9, 1.1), gene))


def randomize_pool(pool):
    return [randomize_gene(gene) for gene in pool]


pool = get_inital_gene_pool()
for generation in range(1000):
    print("Generation #%d" % generation)
    best_gene = min(pool, key=lambda gene: get_gene_score(gene))
    print("Best gene: %s; Score: %f" % (best_gene, get_gene_score(best_gene)))
    pool = [best_gene] * 300 + pool[0:(len(pool) - 300)]
    pool = randomize_pool(pool)
