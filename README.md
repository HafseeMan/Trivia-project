# API Development and Documentation Final Project

## Trivia App

### About
An API used to create Trivia games and quizzes. 
It includes endpoints to display questions, delete, search and play trivia questions randomly based on a specified category. 

## Getting Started

### Pre-requisites
Developers using this project should already have Python3, pip, node, and npm installed.

#### Frontend Dependencies

This project uses NPM to manage software dependencies. From the`frontend` directory of this repository. After cloning, open your terminal and run:

```bash
npm install  # <--- when running the first time
npm start
```

#### Starting Virtual environment
From `/backend` folder run:
```bash
# Mac users
python3 -m venv venv
source venv/bin/activate
# Windows users
> py -3 -m venv venv
> venv\Scripts\activate
```


#### Backend Dependencies

After setting up your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:

```bash
# All required packages are included in the requirements file. 
pip install -r requirements.txt
```

## Running the Frontend in Dev Mode

The frontend app was built using create-react-app. In order to run the app in development mode use ```npm start```. You can change the script in the ```package.json``` file. 

Open [http://localhost:3000](http://localhost:3000) to view it in the browser. The page will reload if you make edits.<br>

```bash
npm start
```

## Running the Server

From the `backend` directory first ensure you are working using your created virtual environment.

To run the server:

```bash
export FLASK_APP=flaskr
export FLASK_ENV=development
flask run
```

## Testing
To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```

NB: don't include dropdb the first time running the command.


## API Reference

### Getting Started
- Base URL: At present this app can only be run locally and is not hosted as a base URL. The backend app is hosted at the default, `http://127.0.0.1:5000/`, which is set as a proxy in the frontend configuration. 
- Authentication: This version of the application does not require authentication or API keys. 

### Endpoints 

#### GET /categories
- General:
    - Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category.
    - Request Arguments: None
    - Returns: An object with a single key, `categories`, that contains an object of id: `category_string` key: value pairs.
- Sample test: `curl http://127.0.0.1:5000/categories`
- Output:
``` 
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

#### GET /questions
- General:
    - Returns a list of question objects, success value, and total number of questions
    - Results are paginated in groups of 10. Include a request argument to choose page number, starting from 1. 
- Sample: `curl http://127.0.0.1:5000/questions`

``` {
  {
  "categories": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 9, 
      "question": "What boxer's original name is Cassius Clay?"
    }, 
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 2, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    }, 
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }, 
    {
      "answer": "Brazil", 
      "category": 6, 
      "difficulty": 3, 
      "id": 10, 
      "question": "Which is the only team to play in every soccer World Cup tournament?"
    }
  ],
"success": true,
"total_books": 18
}
```


#### POST /questions
- General:
    - Creates a new question using the submitted question, answer, category and difficulty. Returns the id of the created , success value, total questions displayed in a list based on current page number to update the frontend. 
- `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"answer": "Tom Cruise", "category": 5, "difficulty": 4, "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"}'`
```
{
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 1, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "The Palace of Versailles", 
      "category": 3, 
      "difficulty": 3, 
      "id": 2, 
      "question": "In which royal palace would you find the Hall of Mirrors?"
    },
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 3, 
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 5, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "created": 5,
  "success": true,
  "total_books": 5
}
```

#### POST /questions
- General:
    - Gets questions based on a search term. It would return any questions for whom the search term
    is a substring of the question, the total matches in list and success value.
-  `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"searchTerm": "title"}'`
```
{
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 5, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    }, 
    {
      "answer": "Edward Scissorhands", 
      "category": 5, 
      "difficulty": 3, 
      "id": 6, 
      "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
    }
  ], 
  "success": true, 
  "total_match": 2
}
```



#### DELETE /questions/{question_id}
- General:
    - Deletes the question of the given ID if it exists. Returns the id of the deleted question, success value, total questions remaining, and questions list based on current page number to update the frontend. 
- `curl -X DELETE http://127.0.0.1:5000/questions/16?page=2`

```
{
  "questions": [
    {
      "answer": "Maya Angelou", 
      "category": 4, 
      "difficulty": 2, 
      "id": 1, 
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    },
    {
      "answer": "Muhammad Ali", 
      "category": 4, 
      "difficulty": 1, 
      "id": 3, 
      "question": "What boxer's original name is Cassius Clay?"
    },
    {
      "answer": "Apollo 13", 
      "category": 5, 
      "difficulty": 4, 
      "id": 4, 
      "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?"
    },
    {
      "answer": "Tom Cruise", 
      "category": 5, 
      "difficulty": 4, 
      "id": 5, 
      "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
    }
  ],
  "deleted": 2,
  "success": true,
  "total_questions": 4
}
```
#### POST /quizzes
- General: Gets questions to play the quiz. This endpoint should take category and previous question parameters
  and return a random questions within the given category, if provided, and that is not one of the previous questions.
- Example: `curl -X POST "Content-Type: application/json" -d '{"previous-questions": [2,6], "quiz_category":{"type":"Entertainment", "id":"5"}}' http://127.0.0.1:5000/quizzes`
- 
```
{
  "question": {
    "answer":"Tom Cruise",
    "category": 5,
    "difficulty": 4,
    "id": 4,
    "question": "What actor did Anne Rice first denounce, then praise in the role of her beloved Lestat?"
  },
  "success": true
}
```


## Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 

## Authors

Hafsah El-Yakubu authored the API (`__init__.py`), test suite (`test_flaskr.py`), and this README.<br>
All other project files, including the models and frontend, were created by [Udacity](https://www.udacity.com/) as a project template for the [Full Stack Web Developer Nanodegree](https://www.udacity.com/course/full-stack-web-developer-nanodegree--nd0044).