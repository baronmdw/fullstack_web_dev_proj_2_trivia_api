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

## Starting the Project

### Backend

#### IMPORTANT
Create a .ENV file in the backend folder containing following information/variables and replace with your information:
```
DB_USER = "<username>"
DB_PASSWORD = "<password>"
DB_HOST = "<host:port>"
DB_NAME = "<databasename>"
DB_TEST_USER = "<username_for_test>"
DB_TEST_PASSWORD = "<password_for_test>"
DB_TEST_HOST = "<host:port_for_test>"
DB_TEST_NAME = "<databasename_for_test>"
```

#### SETTING UP THE BACKEND
> View the [Backend README](./backend/README.md) for more details.

### Frontend

> View the [Frontend README](./frontend/README.md) for more details.

# ENDPOINTS

## CATEGORIES

The Categories endpoint is accessible via GET-Method and returns a JSON object that contains a success-flag and a dictionary with all categories and their respective id in the database.

Request as follows:
```bash
curl http://localhost:5000/categories
```

The result will look similar to this (if there have been no changes in the database the exact response will be returned):
```json
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
```bash
curl -X GET http://localhost:5000/categories/<category_id>/questions
```

The result will look similar to this for a successful request:
```json
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
```json
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
```bash
curl http://localhost:5000/questions?page=<pagenr>
```
replace ```<pagenr>``` with an integer you want to see the questions of

For a successful request the answer will look like this:
```json
{
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
```json
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
```bash
curl -X POST http://localhost:5000/questions -H "Content-Type: application/json" -d "{\"question\":\"Test\", \"answer\":\"answer\", \"category\":1,  \"difficulty\":1}"
```

Successful request will result in this response:
```json
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
```json
{
  "error": 400,
  "message": "The request was not formatted correctly",
  "success": false
}
```

#### Search

The search questions endpoint is accessible via POST-METHOD needing a JSON-Object containing a string called by the key searchTerm. It returns a JSON object with a success status, an array with all questions that match the search-term, the amount of identified questions and the current category.

Request as follows replacing ```<search-string>``` with the string that should be searched:
```bash
curl -X POST http://localhost:5000/questions -H "Content-Type: application/json" -d "{\"searchTerm\":\"<search-string>\"}"
```

Successful request will lead to following result (example made with "title" as search-string):
```json
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
```json
{
  "error": 400,
  "message": "The request was not formatted correctly",
  "success": false
}
```


### DELETE-ENDPOINT

The deletion of a question is accessible via DELETE-METHOD needing the id of the question that shall be deleted in the url and will return a JSON-Object containing the success-status and the id of the deleted question.

Request as follows and replace ```<id>``` with the integer id of the question to delete:
```bash
curl -X DELETE http://localhost:5000/questions/<id>
```

Successful request will lead to following response:
```json
{
  "id": 25,
  "success": true
}
``` 

Trying to delete a non-existing questions will lead to this response:
```json
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
```bash
curl -X POST http://localhost:5000/quizzes -H "Content-Type: application/json" -d "{\"previous_questions\":[<previous_ids>], \"quiz_category\":{\"id\":<category_id>}}" 
```

A correct request will result in following response:
```json
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
```json
{
  "error": 404,
  "message": "The requested resource could not be found",
  "success": false
}
```

# ERROR HANDLING

Following Error-Codes can be expected:

400: Request was not formatted correctly -> please check if your request matches to the specification of the endpoint
404: Resource was not found -> please change for example the id of your search since no matching result was found
422: Request could not be handled -> you might have found an edge case, please report to us
500: server internal error -> this should not be a case that happens often