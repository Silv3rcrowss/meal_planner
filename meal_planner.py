from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api, Resource
from models import GroceryList, GroceryListItem, Meal, MealPlan, Recipe, User
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from chatgpt import create_meal_plan

app = Flask(__name__)
api = Api(app)
CORS(app)
engine = create_engine("mysql+pymysql://root:password@localhost/meal_planner")
Session = sessionmaker(bind=engine)
session = Session()


class MealResource(Resource):
    def post(self):
        meal_data = request.json
        meal = Meal(**meal_data)
        session.add(meal)
        session.commit()
        return meal.to_dict(), 201

    def get(self, meal_id=None):
        if meal_id:
            meal = session.query(Meal).filter_by(id=meal_id).first()
            if meal:
                return meal.to_dict()
            else:
                return {"error": "Meal not found"}, 404
        else:
            meals = session.query(Meal).all()
            return [meal.to_dict() for meal in meals]

    def put(self, meal_id):
        meal_data = request.json
        meal = session.query(Meal).filter_by(id=meal_id).first()
        if meal:
            for key, value in meal_data.items():
                setattr(meal, key, value)
            session.commit()
            return meal.to_dict()
        else:
            return {"error": "Meal not found"}, 404

    def delete(self, meal_id):
        meal = session.query(Meal).filter_by(id=meal_id).first()
        if meal:
            session.delete(meal)
            session.commit()
            return {"message": "Meal deleted"}
        else:
            return {"error": "Meal not found"}, 404


class UserResource(Resource):
    def post(self):
        user_data = request.json
        user = User(**user_data)
        session.add(user)
        try:
            session.commit()
            return user.to_dict(), 201
        except IntegrityError:
            session.rollback()
            return {"error": "Username or email already exists"}, 400

    def get(self, user_id=None):
        if user_id:
            user = session.query(User).filter_by(id=user_id).first()
            if user:
                return user.to_dict()
            else:
                return {"error": "User not found"}, 404
        else:
            users = session.query(User).all()
            return [user.to_dict() for user in users]

    def put(self, user_id):
        user_data = request.json
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            for key, value in user_data.items():
                setattr(user, key, value)
            session.commit()
            return user.to_dict()
        else:
            return {"error": "User not found"}, 404

    def delete(self, user_id):
        user = session.query(User).filter_by(id=user_id).first()
        if user:
            session.delete(user)
            session.commit()
            return {"message": "User deleted"}
        else:
            return {"error": "User not found"}, 404


class GroceryListResource(Resource):
    def post(self):
        grocery_list_data = request.json
        grocery_list = GroceryList(**grocery_list_data)
        session.add(grocery_list)
        session.commit()
        return grocery_list.to_dict(), 201

    def get(self, grocery_list_id=None):
        if grocery_list_id:
            grocery_list = (
                session.query(GroceryList).filter_by(id=grocery_list_id).first()
            )
            if grocery_list:
                return grocery_list.to_dict()
            else:
                return {"error": "Grocery list not found"}, 404
        else:
            grocery_lists = session.query(GroceryList).all()
            return [grocery_list.to_dict() for grocery_list in grocery_lists]

    def put(self, grocery_list_id):
        grocery_list_data = request.json
        grocery_list = session.query(GroceryList).filter_by(id=grocery_list_id).first()
        if grocery_list:
            for key, value in grocery_list_data.items():
                setattr(grocery_list, key, value)
            session.commit()
            return grocery_list.to_dict()
        else:
            return {"error": "Grocery list not found"}, 404

    def delete(self, grocery_list_id):
        grocery_list = session.query(GroceryList).filter_by(id=grocery_list_id).first()
        if grocery_list:
            session.delete(grocery_list)
            session.commit()
            return {"message": "Grocery list deleted"}
        else:
            return {"error": "Grocery list not found"}, 404


class GroceryListItemResource(Resource):
    def post(self):
        item_data = request.json
        item = GroceryListItem(**item_data)
        session.add(item)
        try:
            session.commit()
            return item.to_dict(), 201
        except IntegrityError:
            session.rollback()
            return {"error": "Item already exists in grocery list"}, 400

    def get(self, item_id=None):
        if item_id:
            item = session.query(GroceryListItem).filter_by(id=item_id).first()
            if item:
                return item.to_dict()
            else:
                return {"error": "Item not found"}, 404
        else:
            items = session.query(GroceryListItem).all()
            return [item.to_dict() for item in items]

    def put(self, item_id):
        item_data = request.json
        item = session.query(GroceryListItem).filter_by(id=item_id).first()
        if item:
            for key, value in item_data.items():
                setattr(item, key, value)
            session.commit()
            return item.to_dict()
        else:
            return {"error": "Item not found"}, 404

    def delete(self, item_id):
        item = session.query(GroceryListItem).filter_by(id=item_id).first()
        if item:
            session.delete(item)
            session.commit()
            return {"message": "Item deleted"}
        else:
            return {"error": "Item not found"}, 404


class MealPlanResource(Resource):
    def post(self):
        meal_plan_data = request.json
        meal_plan = MealPlan(**meal_plan_data)
        session.add(meal_plan)
        session.commit()
        return meal_plan.to_dict(), 201

    def get(self, meal_plan_id=None):
        return [
            create_meal_plan(
                objective="lose weight",
                past_meals=[],
                calorie_intake="2500",
                bmi="28",
                user="Alentz",
            )
        ]

    def put(self, meal_plan_id):
        meal_plan_data = request.json
        meal_plan = session.query(MealPlan).filter_by(id=meal_plan_id).first()
        if meal_plan:
            for key, value in meal_plan_data.items():
                setattr(meal_plan, key, value)
            session.commit()
            return meal_plan.to_dict()
        else:
            return {"error": "Meal plan not found"}, 404

    def delete(self, meal_plan_id):
        meal_plan = session.query(MealPlan).filter_by(id=meal_plan_id).first()
        if meal_plan:
            session.delete(meal_plan)
            session.commit()
            return {"message": "Meal plan deleted"}
        else:
            return {"error": "Meal plan not found"}, 404


class RecipeResource(Resource):
    def post(self):
        recipe_data = request.json
        recipe = Recipe(**recipe_data)
        session.add(recipe)
        session.commit()
        return recipe.to_dict(), 201

    def get(self, recipe_id=None):
        if recipe_id:
            recipe = session.query(Recipe).filter_by(id=recipe_id).first()
            if recipe:
                return recipe.to_dict()
            else:
                return {"error": "Recipe not found"}, 404
        else:
            recipes = session.query(Recipe).all()
            return [recipe.to_dict() for recipe in recipes]

    def put(self, recipe_id):
        recipe_data = request.json
        recipe = session.query(Recipe).filter_by(id=recipe_id).first()
        if recipe:
            for key, value in recipe_data.items():
                setattr(recipe, key, value)
            session.commit()
            return recipe.to_dict()
        else:
            return {"error": "Recipe not found"}, 404

    def delete(self, recipe_id):
        recipe = session.query(Recipe).filter_by(id=recipe_id).first()
        if recipe:
            session.delete(recipe)
            session.commit()
            return {"message": "Recipe deleted"}
        else:
            return {"error": "Recipe not found"}, 404


# Routes
api.add_resource(MealResource, "/meals", "/meals/<int:meal_id>")
api.add_resource(UserResource, "/users", "/users/<int:user_id>")
api.add_resource(
    GroceryListResource, "/grocery-lists", "/grocery-lists/<int:grocery_list_id>"
)
api.add_resource(
    GroceryListItemResource, "/grocery-list-items", "/grocery-list-items/<int:item_id>"
)
api.add_resource(MealPlanResource, "/meal-plans", "/meal-plans/<int:meal_plan_id>")
api.add_resource(RecipeResource, "/recipes", "/recipes/<int:recipe_id>")


if __name__ == "__main__":
    app.run(debug=True)
