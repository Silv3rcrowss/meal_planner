from sqlalchemy import create_engine, Column, Integer, String, Text, Enum, ForeignKey, Date
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.types import DateTime
import datetime

engine = create_engine('mysql+pymysql://root:password@localhost/meal_planner')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    image_url = Column(String(255))
    created_by = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    creator = relationship('User', backref='recipes')

class MealPlan(Base):
    __tablename__ = 'meal_plans'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship('User', backref='meal_plans')
    meals = relationship('Meal', backref='meal_plan')

class Meal(Base):
    __tablename__ = 'meals'

    id = Column(Integer, primary_key=True)
    meal_plan_id = Column(Integer, ForeignKey('meal_plans.id'))
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    meal_type = Column(Enum('breakfast', 'lunch', 'dinner'), nullable=False)

    recipe = relationship('Recipe', backref='meals')

class GroceryList(Base):
    __tablename__ = 'grocery_lists'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    meal_plan_id = Column(Integer, ForeignKey('meal_plans.id'))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    user = relationship('User', backref='grocery_lists')
    items = relationship('GroceryListItem', backref='grocery_list')

class GroceryListItem(Base):
    __tablename__ = 'grocery_list_items'

    id = Column(Integer, primary_key=True)
    grocery_list_id = Column(Integer, ForeignKey('grocery_lists.id'))
    recipe_id = Column(Integer, ForeignKey('recipes.id'))
    quantity = Column(Integer, nullable=False)

    recipe = relationship('Recipe', backref='grocery_list_items')