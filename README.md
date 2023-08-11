# Challenge

This project was built per the specifications [here](https://form.jotform.com/213416754424555).

# Table of Contents
- Requirements
- Installation
- Configuration
- Usage
- API Endpoints
- Bonus Features

# Requirements
Before you proceed, ensure you have the following dependencies installed:

- Python (>=3.6)
- pip (Python package manager)
- Virtualenv (recommended for isolating dependencies)

# Installation
Clone this repository to your local machine:
```
git clone https://github.com/Onyenso/quickcheck-challenge2.git
cd quickcheck-challenge2
```

Create a virtual environment and activate it:
```
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

Install the required Python packages:
```
pip install -r requirements.txt
```

# Configuration
Create a Postgres DB on any Postgres client (e.g. PgAdmin), or via commandline.

Create a new `.env` file in the root directory based on the provided [.env.example](https://github.com/Onyenso/quickcheck-challenge2/blob/main/.env.example) file:
```
cp .env.example .env
```

Edit the .env file to configure your environment variables, specifically change these:
```
DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=****
```

# Usage
Apply the database migrations:
```
python manage.py migrate
```

Start the development server:
```
python manage.py runserver
```

Access the web application front-end on your browser at https://quickcheck.onrender.com/all/ or (http://localhost:8000/all/ on your local machine).

# API Endpoints
This project provides a RESTful API for consuming and managing news items. You can view the full ReDoc and Swagger documentaion at:
- ReDoc documentation: https://quickcheck.onrender.com/docs or (http://localhost:8000/docs on your local machine)
- Swagger documentation: https://quickcheck.onrender.com/swagger-docs or (http://localhost:8000/swagger-docs on your local machine)

But here's a summary:

- `POST /users/`
  Sign up as a new user. This is neccessary if you wish to create new items.

- `POST /users/login/`
  Login in order to get a JWT token in which you can pass into the `Authorization` header for authenticated requests, like so `Authorization: Bearer <token>`.

- `POST /token/refresh/`
  To refresh a token using its access token.

- `POST token/verify/`
  To verify if a token is valid.
  
- `GET /all`:
  Lists all news items, allowing filters to be specified. This endpoint is dynamic and returns JSON or HTML response based on the source of the request.
  When returning JSON, it returns every type of news item, but when returning HTML, it returns only the top level items (stories, jobs ands polls). Items with
  null `HN_id` means they were created on our app, not Hacker News.

- `GET /all/{id}`:
  Get a specific item by id (not its id on HackerNews). This endpoint returns both HTML and JSON response.

- `GET /stories/`:
  Get all stories.

- `POST /stories/`:
  Add new story to the database (not present in Hacker News).

- `GET /stories/{id}/`
  Get a single story.

- `PATCH /stories/{id}/`:
  Update an existing story. Only the creator of a story can update it.

- `DELETE /stories/{id}/`
  Delete an existing story. Only the creator of a story can delete it.

The other endpoints perform CRUD operations similar to this. See full documentation using the swagger or redoc interface.

# Bonus Features
The project also includes the bonus features that were requested and a bit more:

- Top-level items are displayed in the front-end list, and their children (e.g., comments) are shown on a detail page.
- The API allows updating and deleting items if they were created in the API (but never data that was retrieved from Hacker News). This was
achieved by the use of permissions.
- Permissions were implemented allowing only the creator of instances to edit or delete them.
- Swagger, Redoc and Postman documentation [here](https://www.postman.com/switch-vibes/workspace/quickcheck).
- Authentication using JWT.
- Endpoints allow filtering and search by text and title (not just text).
- Hacker News has no endpoint to list all items at once. This endpoints allows that feature at `GET /all`.
