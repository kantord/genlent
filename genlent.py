import random
import csv
import sys
import collections


scores = []
headers = set()


def exactly(goal, nutrient):
    def score(total_amounts):
        return abs(float(total_amounts[nutrient]) - float(goal)) / goal

    scores.append(score)
    headers.add(nutrient)


def minimum(goal, nutrient):
    def score(total_amounts):
        if total_amounts[nutrient] < goal:
            return abs(float(total_amounts[nutrient]) - float(goal)) / goal
        else:
            return 0

    scores.append(score)
    headers.add(nutrient)


def maximum(goal, nutrient):
    def score(total_amounts):
        if total_amounts[nutrient] > goal:
            return abs(float(total_amounts[nutrient]) - float(goal)) / goal
        else:
            return 0

    scores.append(score)
    headers.add(nutrient)


def ratio(goal, nutrient1, nutrient2):
    def score(total_amounts):
        if total_amounts[nutrient2]:
            actual_ration = float(
                total_amounts[nutrient1]) / float(total_amounts[nutrient2])
            return abs(actual_ration - goal) / goal
        else:
            return 99999

    scores.append(score)
    headers.add(nutrient1)
    headers.add(nutrient2)

# Personal information
body_mass_kg = 80

# Price requirement
maximum(800, "HUF price")

# Daily requirements
exactly(2000, "kcal")
minimum(body_mass_kg * .75, "g protein")
exactly(65, "g fat")
exactly(2400, "mg sodium")
minimum(3500, "mg potassium")
exactly(300, "g carbs")
minimum(25, "g fiber")

# Amino acids
# source: http://www.ncbi.nlm.nih.gov/books/NBK234922/table/ttt00008/?report=objectonly
minimum(10 * body_mass_kg, "mg histidine"),
minimum(10 * body_mass_kg, "mg isoleucine"),
minimum(14 * body_mass_kg, "mg leucine"),
minimum(12 * body_mass_kg, "mg lysine"),
minimum(13 * body_mass_kg, "mg methionine plus cystine"),
minimum(14 * body_mass_kg, "mg phenylalanine plus tyrosine"),
minimum(7 * body_mass_kg, "mg threonine"),
minimum(5 * body_mass_kg, "mg tryptophan"),
minimum(10 * body_mass_kg, "mg valine"),

# Minerals and vitamins
minimum(900, "μg vitamin a")
minimum(90, "mg ascorbic acid vitamin c")
minimum(1300, "mg calcium")
minimum(18, "mg iron")
minimum(800, "iu cholecalciferol vitamin d")
minimum(33, "mg tocopherol vitamin e")
minimum(120, "μg vitamin k")
minimum(1.2, "mg thiamin vitamin b1")
minimum(1.3, "mg riboflavin vitamin b2")
minimum(16, "mg niacin vitamin b3")
minimum(1.7, "mg pyridoxine vitamin b6")
minimum(400, "μg folate")
minimum(2.4, "μg cobalamine vitamin b12")
minimum(30, "μg biotin")
minimum(5, "mg pantothenic acid vitamin b5")
minimum(1250, "mg phosphorus")
minimum(150, "μg iodine")
minimum(420, "mg magnesium")
minimum(11, "mg zinc")
minimum(55, "μg selenium")
minimum(900, "μg copper")
minimum(2.3, "mg manganese")
minimum(35, "μg chromium")
minimum(45, "μg molybdenum")
minimum(2300, "mg chloride")

# Fatty acids
minimum(17, "g omega-6")
minimum(1.7, "g omega-3")
ratio(1.0, "g omega-6", "g omega-3")

print(headers)

special_formatting = {
    "name": str,
    "source": str
}


def get_variable_formatting(variable_name):
    if variable_name in special_formatting:
        return special_formatting[variable_name]
    else:
        return float


def validate_ingredient(ingredient):
    for key in headers:
        ingredient[key]

# values should be for 100g
ingredients = []

with open(sys.argv[1]) as input_file:
    for ingredient in csv.DictReader(input_file):
        validate_ingredient(ingredient)
        ingredients.append({
            key: get_variable_formatting(key)(value)
            for key, value in ingredient.items()
        })

print(ingredients)


def get_random_recipe():
    return list(map(lambda _: random.uniform(0.0, 10.0), ingredients))


def get_inital_gene_pool(count=10000):
    return list(map(lambda _: get_random_recipe(), range(count)))


def randomize_gene(gene):
    return list(map(lambda i: i * random.uniform(0.9, 1.1), gene))


def randomize_pool(pool):
    return [randomize_gene(gene) for gene in pool]


def get_total_recipe_content(gene):
    totals = collections.defaultdict(float)
    for i, amount in enumerate(gene):
        ingredient = ingredients[i]
        for variable, value in ingredient.items():
            if get_variable_formatting(variable) == float:
                totals[variable] += value * amount

    return totals


def get_total_gene_score(gene):
    totals = get_total_recipe_content(gene)
    return sum(
        score(totals) for score in scores
    )


pool = get_inital_gene_pool()
for generation in range(1000):
    print("Generation #%d" % generation)
    # score = random.choice(list(scores.values()))

    best_gene = min(pool, key=get_total_gene_score)
    print(get_total_gene_score(best_gene))
#     best_gene_r = tuple("%dg %s" % (int(amount * 100), ingredients[i]["Name"]) for i, amount in enumerate(best_gene) if int(amount * 100))
#     print("Best gene: %s; Score: %s; Price %d Ft" % (best_gene_r, {key: -score(best_gene) for key, score in scores.items()}, sum(amount * 1 for i, amount in enumerate(best_gene))))
    # pool = [best_gene] * 5000 + pool[0:(len(pool) - 5000)]
    new_pool = list(sorted(pool, key=get_total_gene_score)[0:500]) * 10 + pool[0:5000]
    pool = randomize_pool(new_pool)
