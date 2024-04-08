## Recipe Management System

### Objective
The Recipe Management System is a feature-rich web application developed using Python and Flask. It allows users to manage and share their favorite recipes. The application includes user authentication, database interactions, and dynamic content.

### Requirements
- Allow users to register and log in
- Enable users to create, view, update, and delete recipes
- Implement a search feature for recipes

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/riteshchdevtech12/recipe_management.git
   ```

2. Navigate to the project directory:
   ```bash
   cd recipe_management
   ```

3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Unix/Linux
   venv\Scripts\activate      # On Windows
   ```

4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

5. Create a .env file in the root directory of the project and copy the contents from .example.env and update the values in .env:
  


6. Run the Flask application:
   ```bash
   python run.py
   ```

7. Access the application in your web browser at http://localhost:5000.


## Endpoints

### Authentication
- **POST /login**: Log in with username and password.
- **POST /register**: Register a new user account.
- **POST /refresh**: Refresh access token.

### Recipes
- **POST /recipes**: Create a new recipe.
- **GET /recipes/:recipe_id**: Get details of a recipe by ID.
- **GET /recipes/search?q=title**: Search recipes.
- **PUT /recipes/:recipe_id**: Update a recipe.
- **DELETE /recipes/:recipe_id**: Delete a recipe.




