# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createbd trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Documentation

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 404,
    "message": "bad request"
}
```
The API will return three error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found

### API End Points

`GET '/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category


Response JSON may look like : 
```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```

`GET '/questions'`

- This API End point allows GET requests for questions, including pagination

- Response JSON may look like : 

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
    "current_category": null,
    "questions": [
        {
            "answer": "Tom Cruise",
            "category": 5,
            "difficulty": 4,
            "id": 4,
            "question": "What actor did author Anne Rice first denounce, then praise in the role of her beloved Lestat?"
        }
    ],
    "success": true,
    "total_questions": 22
}
```
`DELETE '/questions/<int: id>'`
- This API End point allows Delete question based on ID

- Response JSON may look like : 

```json
{
  "deleted_question_id": 4, 
  "message": "Question deleted", 
  "success": true
}

```
`POST '/questions'`

- This API End point allows to create new questions
- Reqest Body may look like

```json
{
    "question": "axaxax",
    "answer": "xaxax",
    "difficulty": 1,
    "category": "2"
}
```
- Response JSON may look like : 

```json
{
    "id": 29,
    "success": true
}
```
`GET '/categories/<int:category_id>/questions'`
 
- This API End point allows to Get questions by category ID

- Response JSON may look like : 

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
    }
  ], 
  "success": true, 
  "total_questions": 7
}

```
`POST '/quizzes'`

- This API End point allows to Get questions to play the quiz based on previous_questions & quiz_category
- Reqest Body may look like

```json
{
    "previous_questions": [],
    "quiz_category": {
        "type": "Science",
        "id": "1"
    }
}
```
- Response JSON may look like : 

```json
{
    "question": {
        "answer": "qwfwqfwqf",
        "category": 1,
        "difficulty": 1,
        "id": 25,
        "question": "wcwqcwq"
    },
    "success": true
}
```

`POST '/questions/search'`

- This API End point allows to Search the question based on search term
- Reqest Body may look like

```json
{
  "searchTerm": "what"
}
```
- Response JSON may look like : 

```json
{
    "current_category": null,
    "questions": [
        {
            "answer": "Edward Scissorhands",
            "category": 5,
            "difficulty": 3,
            "id": 6,
            "question": "What was the title of the 1990 fantasy directed by Tim Burton about a young man with multi-bladed appendages?"
        }
    ],
    "success": true,
    "total_questions": 6
}
```

``

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
