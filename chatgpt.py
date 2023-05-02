from open_ai_client import generate_meal_suggestions


def create_meal_plan(user, objective, past_meals, calorie_intake, bmi):
    prompt = f"Create a weekly meal plan for {user} with the main objective of {objective}. Please consider their meal history over the past 2 weeks, average daily calorie intake of {calorie_intake} calories, and a Body Mass Index (BMI) of {bmi}. Please provide the meal plan as a list of meals with their corresponding recipe names, descriptions, and meal types (breakfast, lunch, or dinner) for each day of the week."

    meal_suggestions = generate_meal_suggestions(prompt)
    return {"suggestions": meal_suggestions}

    # for meal in meal_suggestions:
    #     # Store the recipe in the recipes table and get the recipe_id
    #     recipe_id = store_recipe(meal["name"], meal["description"], user["id"])

    #     # Add the meal to the meal plan using the recipe_id
    #     add_meal_to_meal_plan(meal_plan_id, recipe_id, meal["meal_type"])


# def store_recipe(name, description, created_by):
#     query = "INSERT INTO recipes (name, description, created_by) VALUES (%s, %s, %s)"
#     values = (name, description, created_by)
#     cursor.execute(query, values)
#     connection.commit()

#     return cursor.lastrowid
