# API Development and Documentation Final Project

## Trivia App

### About
An API used to create Trivia games and quizzes. 
It includes endpoints to display questions, delete, search and play trivia based on a specified category. 

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

#### POST /questions/search
- General:
    - Gets questions based on a search term. It would return any questions for whom the search term
    is a substring of the question, the total matches in list and success value.
-  `curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"search": "title"}'`
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