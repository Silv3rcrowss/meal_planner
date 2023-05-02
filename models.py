import datetime
from typing import Dict, Any

from sqlalchemy import Column, ForeignKey, Integer, String, Enum, Text
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.types import DateTime

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id: Column = Column(Integer, primary_key=True)
    name: Column = Column(String)
    email: Column = Column(String)

    def to_dict(self) -> Dict[str, str]:
        return {
            "id": str(self.id),
            "name": str(self.name),
            "email": str(self.email),
        }


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(String(255))
    created_by = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    @declared_attr
    def creator(cls):
        return relationship("User", backref="recipes")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "name": self.name,
            "description": self.description,
            "image_url": self.image_url,
            "created_by": str(self.created_by),
            "created_at": self.created_at.isoformat(),
        }


class MealPlan(Base):
    __tablename__ = "meal_plans"

    id: Column = Column(Integer, primary_key=True)
    user_id: Column = Column(Integer, ForeignKey("users.id"))
    start_date: Column = Column(DateTime, default=datetime.datetime.utcnow)
    end_date: Column = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", backref="meal_plans")
    recipes = relationship("MealPlanRecipe", backref="meal_plan")

    def to_dict(self) -> Dict[str, str]:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
        }


class MealPlanRecipe(Base):
    __tablename__ = "meal_plan_recipes"

    id: Column = Column(Integer, primary_key=True)
    meal_plan_id: Column = Column(Integer, ForeignKey("meal_plans.id"))
    recipe_id: Column = Column(Integer, ForeignKey("recipes.id"))

    recipe = relationship("Recipe", backref="meal_plans")

    def to_dict(self) -> Dict[str, str]:
        return {
            "id": str(self.id),
            "meal_plan_id": str(self.meal_plan_id),
            "recipe_id": str(self.recipe_id),
        }


class Meal(Base):
    __tablename__: str = "meals"

    id: Column[int] = Column(Integer, primary_key=True)
    meal_plan_id: Column[int] = Column(Integer, ForeignKey("meal_plans.id"))
    recipe_id: Column[int] = Column(Integer, ForeignKey("recipes.id"))
    meal_type: Column[str] = Column(
        Enum("breakfast", "lunch", "dinner"), nullable=False
    )

    recipe = relationship("Recipe", backref="meals")

    def to_dict(self) -> dict[str, str]:
        return {
            "id": str(self.id),
            "meal_plan_id": str(self.meal_plan_id),
            "recipe_id": str(self.recipe_id),
            "meal_type": str(self.meal_type),
        }


class GroceryList(Base):
    __tablename__: str = "grocery_lists"

    id: Column = Column(Integer, primary_key=True)
    user_id: Column = Column(Integer, ForeignKey("users.id"))
    meal_plan_id: Column = Column(Integer, ForeignKey("meal_plans.id"))
    created_at: Column = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship("User", backref="grocery_lists")
    items = relationship("GroceryListItem", backref="grocery_list")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "user_id": str(self.user_id),
            "meal_plan_id": str(self.meal_plan_id),
            "created_at": self.created_at.isoformat(),
        }


class GroceryListItem(Base):
    __tablename__: str = "grocery_list_items"

    id: Column = Column(Integer, primary_key=True)
    grocery_list_id: Column = Column(Integer, ForeignKey("grocery_lists.id"))
    recipe_id: Column = Column(Integer, ForeignKey("recipes.id"))
    quantity: Column = Column(Integer, nullable=False)

    recipe = relationship("Recipe", backref="grocery_list_items")

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": str(self.id),
            "grocery_list_id": str(self.grocery_list_id),
            "recipe_id": str(self.recipe_id),
            "quantity": str(self.quantity),
        }
