# API Development and Documentation Final Project

## Trivia App

Udacity is invested in creating bonding experiences for its employees and students. A bunch of team members got the idea to hold trivia on a regular basis and created a webpage to manage the trivia app and play the game, but their API experience is limited and still needs to be built out.

That's where you come in! Help them finish the trivia app so they can start holding trivia and seeing who's the most knowledgeable of the bunch. The application must:

1. Display questions - both all questions and by category. Questions should show the question, category and difficulty rating by default and can show/hide the answer.
2. Delete questions.
3. Add questions and require that they include question and answer text.
4. Search for questions based on a text query string.
5. Play the quiz game, randomizing either all questions or within a specific category.

Completing this trivia app will give you the ability to structure plan, implement, and test an API - skills essential for enabling your future applications to communicate with others.

## Starting and Submitting the Project

[Fork](https://help.github.com/en/articles/fork-a-repo) the project repository and [clone](https://help.github.com/en/articles/cloning-a-repository) your forked repository to your machine. Work on the project locally and make sure to push all your changes to the remote repository before submitting the link to your repository in the Classroom.

## About the Stack

We started the full stack application for you. It is designed with some key functional areas:

### Backend

The [backend](./backend/README.md) directory contains a partially completed Flask and SQLAlchemy server. You will work primarily in `__init__.py` to define your endpoints and can reference models.py for DB and SQLAlchemy setup. These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

> View the [Backend README](./backend/README.md) for more details.

### Frontend

The [frontend](./frontend/README.md) directory contains a complete React frontend to consume the data from the Flask server. If you have prior experience building a frontend application, you should feel free to edit the endpoints as you see fit for the backend you design. If you do not have prior experience building a frontend application, you should read through the frontend code before starting and make notes regarding:

1. What are the end points and HTTP methods the frontend is expecting to consume?
2. How are the requests from the frontend formatted? Are they expecting certain parameters or payloads?

Pay special attention to what data the frontend is expecting from each API response to help guide how you format your API. The places where you may change the frontend behavior, and where you should be looking for the above information, are marked with `TODO`. These are the files you'd want to edit in the frontend:

1. `frontend/src/components/QuestionView.js`
2. `frontend/src/components/FormView.js`
3. `frontend/src/components/QuizView.js`

By making notes ahead of time, you will practice the core skill of being able to read and understand code and will have a simple plan to follow to build out the endpoints of your backend API.

> View the [Frontend README](./frontend/README.md) for more details.

# ENDPOINTS

## CATEGORIES

The Categories endpoint is accessible via GET-Method and returns a JSON object that contains a success-flag and a dictionary with all categories and their respective id in the database.

Request as follows:
```
curl http://localhost:5000/categories
```

The result will look similar to this (if there have been no changes in the database the exact response will be returned):
```
{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "success": true
}
```

### GET-QUESTIONS ENDPOINT

The get all questions of category endpoint is accessible via GET-METHOD needing a category number as input parameter and returns a JSON object that contains a success-flag, an array of all questions, the amount of questions and the current category.

Request as follows and replace ```<category_id>``` with the number of the category that is being searched for:
```
curl -X GET http://localhost:5000/categories/<category_id>/questions
```

The result will look similar to this for a successful request:
```
{
  "current_category": 1,
  "questions": [
    {
      "answer": "The Liver",
      "category": 1,
      "difficulty": 4,
      "id": 20,
      "question": "What is the heaviest organ in the human body?"
    },
    {
      "answer": "Alexander Fleming",
      "category": 1,
      "difficulty": 3,
      "id": 21,
      "question": "Who discovered penicillin?"
    },
    {
      "answer": "Blood",
      "category": 1,
      "difficulty": 4,
      "id": 22,
      "question": "Hematology is a branch of medicine involving the study of what?"
    }
  ],
  "success": true,
  "total_questions": 3
}
```

An erroneous request will lead to this response:
```
{
  "error": 404,
  "message": "The requested resource could not be found",
  "success": false
}
```

## QUESTIONS

### GET-ENDPOINT

The read all questions endpoint is accessible via GET-METHOD needing a page number as input parameter and returns a JSON object that contains a success-flag, a dictionary with all categories and their respective id in the database, a list of 10 questions objects including their answers, categories and difficulties as well as the number of total questions in the database. The questions returned are depending on the page that has been requested.

Request as follows:
```
curl http://localhost:5000/questions?page=<pagenr>
```
replace ```<pagenr>``` with an integer you want to see the questions of

For a successful request the answer will look like this:
```{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "currentCategroy": "ALL",
  "questions": [
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
    },
    {
      "answer": "Uruguay",
      "category": 6,
      "difficulty": 4,
      "id": 11,
      "question": "Which country won the first ever soccer World Cup in 1930?"
    },
    {
      "answer": "George Washington Carver",
      "category": 4,
      "difficulty": 2,
      "id": 12,
      "question": "Who invented Peanut Butter?"
    },
    {
      "answer": "Lake Victoria",
      "category": 3,
      "difficulty": 2,
      "id": 13,
      "question": "What is the largest lake in Africa?"
    },
    {
      "answer": "The Palace of Versailles",
      "category": 3,
      "difficulty": 3,
      "id": 14,
      "question": "In which royal palace would you find the Hall of Mirrors?"
    }
  ],
  "success": true,
  "totalQuestions": 19
}
```
For an unsuccessful request the response will look like this:
```
{
  "error": 404,
  "message": "The requested resource could not be found",
  "success": false
}
```

### POST-ENDPOINT

#### Creation

The questions creation endpoint is accessible via POST-METHOD needing a JSON-Object containing a string each for question and answer and integers for the difficulty (1-5) and the category of the question. All of the named options are mandatory. It returns a JSON-Object with a success status as well as the id, question, answer, difficulty and category of the created object.

Request as follows:
```
curl -X POST http://localhost:5000/questions -H "Content-Type: application/json" -d "{\"question\":\"Test\", \"answer\":\"answer\", \"category\":1,  \"difficulty\":1}"
```

Successful request will result in this response:
```
{
  "answer": "answer",
  "category": 1,
  "difficulty": 1,
  "id": 25,
  "question": "Test",
  "success": true
}
```

For an erroneous request the response will look like this:
```
{
  "error": 400,
  "message": "The request was not formatted correctly",
  "success": false
}
```

#### Search

The search questions endpoint is accessible via POST-METHOD needing a JSON-Object containing a string called by the key searchTerm. It returns a JSON object with a success status, an array with all questions that match the search-term, the amount of identified questions and the current category.

Request as follows replacing ```<search-string>``` with the string that should be searched:
```
curl -X POST http://localhost:5000/questions -H "Content-Type: application/json" -d "{\"searchTerm\":\"<search-string>\"}"
```

Successful request will lead to following result (example made with "title" as search-string):
```
{
  "currentCategroy": "ALL",
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
  "total_questions": 2
}
```

Erroneous request will result in this response:
```
{
  "error": 400,
  "message": "The request was not formatted correctly",
  "success": false
}
```


### DELETE-ENDPOINT

The deletion of a question is accessible via DELETE-METHOD needing the id of the question that shall be deleted in the url and will return a JSON-Object containing the success-status and the id of the deleted question.

Request as follows and replace ```<id>``` with the integer id of the question to delete:
```
curl -X DELETE http://localhost:5000/questions/<id>
```

Successful request will lead to following response:
```
{
  "id": 25,
  "success": true
}
``` 

Trying to delete a non-existing questions will lead to this response:
```
{
  "error": 404,
  "message": "The requested resource could not be found",
  "success": false
}
```

## QUIZZES

### POST-ENDPOINT

This endpoint is accessible via the POST-METHOD and needs a JSON-object containing an array of already posted questions (previous_questions) and the category of the quiz (quiz_category). It returns a JSON-Object with a success status and the object of the next question.

Request as follows replacing ```<previous_ids>``` with the ids of all questions that have already been posted separated by a comma (,) and ```<category_id>``` by the id of the category of the quiz (0 for all categories):
```
curl -X POST http://localhost:5000/quizzes -H "Content-Type: application/json" -d "{\"previous_questions\":[<previous_ids>], \"quiz_category\":{\"id\":<category_id>}}" 
```

A correct request will result in following response:
```
{
  "question": {
    "answer": "The Liver",
    "category": 1,
    "difficulty": 4,
    "id": 20,
    "question": "What is the heaviest organ in the human body?"
  },
  "success": true
}
```

Searching for a non existent category will lead to this response:
```
{
  "error": 404,
  "message": "The requested resource could not be found",
  "success": false
}
```
