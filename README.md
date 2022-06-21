# API Documentation For Trivia App

### Getting Started

+ **Base URL**: At the moment this app can only be run locally and is not hosted as a base URL. The API is hosted by default on http://127.0.0.1:5000/
+ **Authentication**:Interacting with the present version of this app doesnt require any authentication or API Keys

### Endpoints

1. Questions
   1. [GET api/questions](#get-questions)
   2. [POST api/questions](#post-questions)
   3. [DELETE api/questions/<question_id>](#delete-questions)
   4. [POST api/searchquestions](#search-questions)
2. Quizzes
   1. [POST api/quizzes](#post-quizzes)
3. Categories
   1. [GET api/categories](#get-categories)
   2. [GET api/categories/<category_id>/questions](#get-categories-questions)


Each ressource documentation is clearly structured:
1. Description in a few words
2. `curl` example that can directly be used in terminal
3. More descriptive explanation of input & outputs.
4. Example Response.
5. Error Handling (`curl` command to trigger error + error response)

# <a name="get-questions"></a>
### 1. GET /questions

Fetch paginated questions:
```bash
$ curl -X GET http://127.0.0.1:5000/api/questions?page=1
```
- Fetches a list of dictionaries of questions in which the keys are the ids with all available fields, a list of all categories and number of total questions.
- Request Arguments: 
    - **integer** `page` (optional, 10 questions per page, defaults to `1` if not given)
- Request Headers: **None**
- Returns: 
  1. List of dict of questions with following fields:
      - **integer** `id`
      - **string** `question`
      - **string** `answer`
      - **string** `category`
      - **integer** `difficulty`
  2. **list** `categories`
  3. **Null** `current_category`
  4. **integer** `total_questions`

#### Example response
```js
{
"categories": [
    "music",
    "Art",
    "Stories",
    "Animation",
    "design",
    "Fashion"
  ],
"current_category":Null,
"questions": [
    {
      "answer": "David Mark",
      "category": 5,
      "difficulty": 4,
      "id": 2,
      "question": "Who is the first man to win a nobel prize in physics?"
    },
    {
      "answer": "Ronaldo",
      "category": 5,
      "difficulty": 4,
      "id": 4,
      "question": "Who is the best football player in the world?"
    },

 [...]

  ],
  "total_questions": 19
}

```
#### Errors
A request with an invalid page will return a `404` statuscode have the below response:

```bash
curl -X GET http://127.0.0.1:5000/api/questions?page=124
```

will return

```js
{
   "status":"fail",
    "message":"resource not found"
}

```

# <a name="search-questions"></a>
### 2. POST /searchquestions

Search Questions
```bash
curl -X POST http://127.0.0.1:5000/api/searchquestions -d '{"searchTerm" : "name"}' -H 'Content-Type: application/json'
```


- Searches all questions in the database for questions containing the search term 
- Request Arguments: **None**
- Request Headers :
       1. **string** `searchTerm` (<span style="color:red">*</span>required)

- Returns: 
    1. List of dict of `questions` which match the `searchTerm` with following fields:
        - **integer** `id`
        - **string** `question`
        - **string** `answer`
        - **string** `category`
        - **integer** `difficulty`
    2. **None** `current_category`
    3. **integer** `total_questions`
  

#### Example response
Search Questions
```js
{
  "current_category":None,
  "questions": [
    {
      "answer": "free",
      "category": 1,
      "difficulty": 1,
      "id": 24,
      "question": "name of names?"
    }

  .. with all questions that contains the search term
  
  ],
  "total_questions": 6
}

```


#### Errors
**Search related**

Searching for a question that does not exist return a 404 status code below:

```bash
curl -X POST http://127.0.0.1:5000/api/searchquestions -d '{"searchTerm" : "this does not exist"}' -H'Content-Type: application/json' 
```

will return

```js
{
  "status":"fail",
  "message":"resource not found"
}
```

If you try to search for question, but forget to provide a required field in the request body, it will throw an `400` error:
```bash
curl -X POST http://127.0.0.1:5000/api/searchquestions  -H 'Content-Type: application/json'
```

will return

```js
{
   "status":"fail",
   "message":"Invalid request body"
}
```



# <a name="delete-questions"></a>
### 3. DELETE api/questions/<question_id>

Delete Questions
```bash
curl -X DELETE http://127.0.0.1:5000/api/questions/10
```
- Deletes specific question based on given id
- Request Arguments: 
  - **integer** `question_id`
- Request Headers : **None**
- Returns: None
- Satus code `204`


### Errors

If you try to delete a `question` which does not exist, it will throw a `404` error:

```bash
curl -X DELETE http://127.0.0.1:5000/api/questions/7
```
will return
```js
{
      "status":"fail",
      "message":"resource not found"
}
```

# <a name="post-quizzes"></a>
### 4. POST /api/quizzes

Play quiz game.
```bash
curl -X POST http://127.0.0.1:5000/api/quizzes -d '{"previous_questions" : [1, 2, 5], "quiz_category" : {"type" : "Science", "id" : "1"}} ' -H 'Content-Type: application/json'
```
- Plays quiz game by providing a list of already asked questions and a category to ask for a fitting, random question.
- Request Arguments: **None**
- Request Headers : 
     1. **list** `previous_questions` with **integer** ids from already asked questions
     1. **dict** `quiz_category` (optional) with keys:
        1.  **string** type
        2. **integer** id from category
- Returns: 
  1. Exactly one `question` as **dict** with following fields:
      - **integer** `id`
      - **string** `question`
      - **string** `answer`
      - **string** `category`
      - **integer** `difficulty`

#### Example response
```js
{
  "question": {
    "answer": "Yes",
    "category": 1,
    "difficulty": 1,
    "id": 12,
    "question": "Is udacity a good learning platform?"
  }
}

```
### Errors

If you try to play the quiz game without a a valid JSON body, it will response with an  `400` error.

```bash
curl -X POST http://127.0.0.1:5000/api/quizzes
```
will return
```js
{
   "status":"fail",
   "message":"Invalid request body"

}

```
# <a name="get-categories"></a>
### 5. GET /api/categories

Fetch all available categories

```bash
curl -X GET http://127.0.0.1:5000/api/categories
```

- Fetches a dict of all available categories with their `ID` as keys and `type` as values
- Request Arguments: **None**
- Request Headers: **None**

- Returns: 
  1. **dict** containing different  `categories` 
 
### Example Response

```{
    "categories": {
      "1": "Science",
      "2": "Art",
      "3": "Geography",
      "4": "History",
      "5": "Entertainment",
      "6": "Sports"
    }
  }
```

### Errors

If there are no categories, it will throw a `404` error:

```bash
curl -X DELETE http://127.0.0.1:5000/api/categories
```
will return
```js
{
      "status":"fail",
      "message":"resource not found"
}
```




# <a name="get-categories-questions"></a>
### 6. GET api/categories/<category_id>/questions

Get all questions from a specific `category`.
```bash
curl -X GET http://127.0.0.1:5000/api/categories/2/questions
```
- Fetches all `questions` from one specific category.
- Request Arguments:
  - **integer** `category_id` (<span style="color:red">*</span>required)
- Request Headers: **None**
- Returns: 
  1. **integer** `current_category` id from inputted category
  2. List of dict of all questions with following fields:
     - **integer** `id` 
     - **string** `question`
     - **string** `answer`
     - **string** `category`
     - **integer** `difficulty`
  3. **integer** `total_questions`

#### Example response

```js
{
  "current_category": "2",
  "questions": [
    {
      "answer": "Escher",
      "category": 2,
      "difficulty": 1,
      "id": 16,
      "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?"
    },
    {
      "answer": "Mona Lisa",
      "category": 2,
      "difficulty": 3,
      "id": 17,
      "question": "La Giaconda is better known as what?"
    },
    {
      "answer": "One",
      "category": 2,
      "difficulty": 4,
      "id": 18,
      "question": "How many paintings did Van Gogh sell in his lifetime?"
    },
    {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?"
    }
  ],
  "total_questions": 4
}
```

### Errors
You get a 404 error when you query with a category that doesn't exist or for the wrong page:
```bash
curl -X GET http://127.0.0.1:5000/api/categories/10/questions?page=1
```
will return
```js
{
      "status":"fail",
      "message":"resource not found"
            
}
```


