import os
import sys
import unittest
from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from common.models import (
    Base,
    User,
    Recipe,
    MealPlan,
    MealPlanRecipe,
    Meal,
    GroceryList,
    GroceryListItem,
)


class TestModels(unittest.TestCase):
    engine = create_engine("sqlite:///:memory:")
    Session = sessionmaker(bind=engine)

    def setUp(self):
        Base.metadata.create_all(self.engine)
        self.session = self.Session()

    def tearDown(self):
        Base.metadata.drop_all(self.engine)
        self.session.close()

    def test_user_to_dict(self):
        user = User(name="John Doe", email="john.doe@example.com")
        self.session.add(user)
        self.session.commit()

        expected_dict = {
            "id": str(user.id),
            "name": "John Doe",
            "email": "john.doe@example.com",
        }
        self.assertEqual(user.to_dict(), expected_dict)

    def test_recipe_to_dict(self):
        user = User(name="John Doe", email="john.doe@example.com")
        recipe = Recipe(
            name="Spaghetti Carbonara",
            description="A classic Italian pasta dish",
            image_url="https://example.com/spaghetti-carbonara.jpg",
            creator=user,
        )
        self.session.add(user)
        self.session.add(recipe)
        self.session.commit()

        expected_dict = {
            "id": str(recipe.id),
            "name": "Spaghetti Carbonara",
            "description": "A classic Italian pasta dish",
            "image_url": "https://example.com/spaghetti-carbonara.jpg",
            "created_by": str(user.id),
            "created_at": recipe.created_at.isoformat(),
        }
        self.assertEqual(recipe.to_dict(), expected_dict)

    def test_meal_plan_to_dict(self):
        user = User(name="John Doe", email="john.doe@example.com")
        meal_plan = MealPlan(
            user=user, start_date=datetime.utcnow(), end_date=datetime.utcnow()
        )
        self.session.add(user)
        self.session.add(meal_plan)
        self.session.commit()

        expected_dict = {
            "id": str(meal_plan.id),
            "user_id": str(user.id),
            "start_date": meal_plan.start_date.isoformat(),
            "end_date": meal_plan.end_date.isoformat(),
        }
        self.assertEqual(meal_plan.to_dict(), expected_dict)

    def test_meal_plan_recipe_to_dict(self):
        user = User(name="John Doe", email="john.doe@example.com")
        recipe = Recipe(
            name="Spaghetti Carbonara",
            description="A classic Italian pasta dish",
            image_url="https://example.com/spaghetti-carbonara.jpg",
            creator=user,
        )
        meal_plan = MealPlan(
            user=user, start_date=datetime.utcnow(), end_date=datetime.utcnow()
        )
        meal_plan_recipe = MealPlanRecipe(meal_plan=meal_plan, recipe=recipe)
        self.session.add(user)
        self.session.add(recipe)
        self.session.add(meal_plan)
        self.session.add(meal_plan_recipe)
        self.session.commit()

        expected_dict = {
            "id": str(meal_plan_recipe.id),
            "meal_plan_id": str(meal_plan.id),
            "recipe_id": str(recipe.id),
        }
        self.assertEqual(meal_plan_recipe.to_dict(), expected_dict)

    def test_meal_to_dict(self):
        user = User(name="John Doe", email="john.doe@example.com")
        recipe = Recipe(
            name="Spaghetti Carbonara",
            description="A classic Italian pasta dish",
            image_url="https://example.com/spaghetti-carbonara.jpg",
            creator=user,
        )
        meal_plan = MealPlan(
            user=user, start_date=datetime.utcnow(), end_date=datetime.utcnow()
        )
        meal = Meal(meal_plan=meal_plan, recipe=recipe, meal_type="dinner")
        self.session.add(user)
        self.session.add(recipe)
        self.session.add(meal_plan)
        self.session.add(meal)
        self.session.commit()

        expected_dict = {
            "id": str(meal.id),
            "meal_plan_id": str(meal_plan.id),
            "recipe_id": str(recipe.id),
            "meal_type": "dinner",
        }
        self.assertEqual(meal.to_dict(), expected_dict)

    def test_grocery_list_to_dict(self):
        user = User(name="John Doe", email="john.doe@example.com")
        meal_plan = MealPlan(
            user=user, start_date=datetime.utcnow(), end_date=datetime.utcnow()
        )
        grocery_list = GroceryList(
            user=user, meal_plan=meal_plan, created_at=datetime.utcnow()
        )
        self.session.add(user)
        self.session.add(meal_plan)
        self.session.add(grocery_list)
        self.session.commit()

        expected_dict = {
            "id": str(grocery_list.id),
            "user_id": str(user.id),
            "meal_plan_id": str(meal_plan.id),
            "created_at": grocery_list.created_at.isoformat(),
        }
        self.assertEqual(grocery_list.to_dict(), expected_dict)

    def test_grocery_list_item_to_dict(self):
        user = User(name="John Doe", email="john.doe@example.com")
        recipe = Recipe(
            name="Spaghetti Carbonara",
            description="A classic Italian pasta dish",
            image_url="https://example.com/spaghetti-carbonara.jpg",
            creator=user,
        )
        meal_plan = MealPlan(
            user=user, start_date=datetime.utcnow(), end_date=datetime.utcnow()
        )
        grocery_list = GroceryList(
            user=user, meal_plan=meal_plan, created_at=datetime.utcnow()
        )
        grocery_list_item = GroceryListItem(
            grocery_list=grocery_list, recipe=recipe, quantity=2
        )
        self.session.add(user)
        self.session.add(recipe)
        self.session.add(meal_plan)
        self.session.add(grocery_list)
        self.session.add(grocery_list_item)
        self.session.commit()

        expected_dict = {
            "id": str(grocery_list_item.id),
            "grocery_list_id": str(grocery_list.id),
            "recipe_id": str(recipe.id),
            "quantity": "2",
        }
        self.assertEqual(grocery_list_item.to_dict(), expected_dict)
