import openai
import os


# Set up OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")


def format_meal_history(meal_history):
    formatted_history = ""
    for meal in meal_history:
        formatted_history += (
            f"{meal['day']} - {meal['meal_type']} - Recipe ID: {meal['recipe_id']}\n"
        )
    return formatted_history


def generate_meal_suggestions(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=200,
        n=1,
        stop=None,
        temperature=0.7,
    )

    # Parse the response to extract the meal plan details
    # return parse_meal_plan(response.choices[0].text.strip())

    return response.choices[0].text.strip()


def parse_meal_plan(meal_plan):
    days_of_week = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    meal_types = ["breakfast", "lunch", "dinner"]

    output = "Weekly Meal Plan:\n\n"

    for day in days_of_week:
        output += f"{day}:\n"

        for meal_type in meal_types:
            meal = get_meal_by_day_and_type(meal_plan, day, meal_type)

            if meal:
                output += f"  {meal_type.capitalize()}:\n"
                output += f"    Recipe Name: {meal['name']}\n"
                output += f"    Description: {meal['description']}\n"
            else:
                output += f"  {meal_type.capitalize()}: No meal assigned\n"

        output += "\n"

    return output


def get_meal_by_day_and_type(meal_plan, day, meal_type):
    for meal in meal_plan:
        if meal["day"] == day and meal["meal_type"] == meal_type:
            return meal
    return None


# # Retrieve the user's meal history and average calorie intake from the database
# meal_history = get_meal_history(user_id, days=14)
# average_calorie_intake = get_average_calorie_intake(user_id, days=14)

# # Format the meal history
# formatted_meal_history = format_meal_history(meal_history)

# # Call create_meal_plan with the additional data
# create_meal_plan(user, objective, formatted_meal_history, average_calorie_intake)
