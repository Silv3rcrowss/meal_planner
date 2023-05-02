-- Create the meal_planner database
CREATE DATABASE meal_planner;

-- Use the meal_planner database
USE meal_planner;

-- Create the users table
CREATE TABLE users (
  id INT PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the recipes table
CREATE TABLE recipes (
  id INT PRIMARY KEY AUTO_INCREMENT,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  image_url VARCHAR(255),
  created_by INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_recipes_created_by FOREIGN KEY (created_by) REFERENCES users(id)
);

-- Create the meal_plans table
CREATE TABLE meal_plans (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  start_date DATE NOT NULL,
  end_date DATE NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_meal_plans_user_id FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create the meals table
CREATE TABLE meals (
  id INT PRIMARY KEY AUTO_INCREMENT,
  meal_plan_id INT NOT NULL,
  recipe_id INT NOT NULL,
  meal_type ENUM('breakfast', 'lunch', 'dinner') NOT NULL,
  CONSTRAINT fk_meals_meal_plan_id FOREIGN KEY (meal_plan_id) REFERENCES meal_plans(id),
  CONSTRAINT fk_meals_recipe_id FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);

-- Create the grocery_lists table
CREATE TABLE grocery_lists (
  id INT PRIMARY KEY AUTO_INCREMENT,
  user_id INT NOT NULL,
  meal_plan_id INT NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT fk_grocery_lists_user_id FOREIGN KEY (user_id) REFERENCES users(id),
  CONSTRAINT fk_grocery_lists_meal_plan_id FOREIGN KEY (meal_plan_id) REFERENCES meal_plans(id)
);

-- Create the grocery_list_items table
CREATE TABLE grocery_list_items (
  id INT PRIMARY KEY AUTO_INCREMENT,
  grocery_list_id INT NOT NULL,
  recipe_id INT NOT NULL,
  quantity INT NOT NULL,
  CONSTRAINT fk_grocery_list_items_grocery_list_id FOREIGN KEY (grocery_list_id) REFERENCES grocery_lists(id),
  CONSTRAINT fk_grocery_list_items_recipe_id FOREIGN KEY (recipe_id) REFERENCES recipes(id)
);
