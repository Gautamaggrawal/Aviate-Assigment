# Applicant Tracking System (ATS) for Recruiters

This project is an Applicant Tracking System (ATS) built with Django Rest Framework to help recruiters keep track of job applications. The application includes functionalities to create, update, delete, and search candidates based on their name.

## Project Structure
- `models.py`: Contains the Candidate model with attributes such as Name, Age, Gender, Email, and Phone number.
- `views.py`: API views to handle CRUD operations and candidate search.
- `serializers.py`: Serializers to convert model data to JSON format for API responses.
- `urls.py`: URL routes for API endpoints.
- `management/commands/generate_candidates.py`: Custom Django management command to generate dynamic test candidate data.

## Requirements
- Python 3.x
- Django 3.x
- Django Rest Framework (DRF) 3.x
- Faker library for generating random test data

## Setup Instructions

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Gautamaggrawal/Aviate-Assigment.git
    cd ats-recruiter
    ```

2. **Create a virtual environment and install dependencies:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # For Windows use: venv\Scripts\activate
    pip install -r requirements.txt
    ```

3. **Set up the database:**

    Update the `DATABASES` setting in `settings.py` if needed. By default, Django uses SQLite for development.

4. **Run migrations:**

    Apply the migrations to set up the `Candidate` table:

    ```bash
    python manage.py migrate
    ```

5. **Run the server:**

    Start the development server:

    ```bash
    python manage.py runserver
    ```

    The API will be available at `http://127.0.0.1:8000/api/v1/`.

## API Endpoints

### 1. Create Candidate
- **URL:** `/api/v1/candidates/`
- **Method:** `POST`
- **Request Body:**

    ```json
    {
        "name": "Ajay Kumar Yadav",
        "age": 30,
        "gender": "Male",
        "email": "ajay@example.com",
        "phone_number": "1234567890"
    }
    ```

- **Response:**

    ```json
    {
        "id": 1,
        "name": "Ajay Kumar Yadav",
        "age": 30,
        "gender": "Male",
        "email": "ajay@example.com",
        "phone_number": "1234567890"
    }
    ```

### 2. Update Candidate
- **URL:** `/api/v1/candidates/{id}/`
- **Method:** `PUT`
- **Request Body:**

    ```json
    {
        "name": "Ajay Kumar",
        "age": 31,
        "gender": "Male",
        "email": "ajay_updated@example.com",
        "phone_number": "0987654321"
    }
    ```

- **Response:**

    ```json
    {
        "id": 1,
        "name": "Ajay Kumar",
        "age": 31,
        "gender": "Male",
        "email": "ajay_updated@example.com",
        "phone_number": "0987654321"
    }
    ```

### 3. Delete Candidate
- **URL:** `/api/v1/candidates/{id}/`
- **Method:** `DELETE`
- **Response:** `204 No Content` (No content, the candidate is deleted).

### 4. Search Candidates
- **URL:** `/api/v1/candidates/search/`
- **Method:** `GET`
- **Query Parameters:**
    - `query`: The search term to find candidates (partial matches allowed).
  
    Example query:
    ```bash
    /api/v1/candidates/search/?query=Ajay Kumar yadav
    ```

- **Response:**

    ```json
    [
        {
            "id": 1,
            "name": "Ajay Kumar Yadav",
            "age": 30,
            "gender": "Male",
            "email": "ajay@example.com",
            "phone_number": "1234567890"
        },
        {
            "id": 2,
            "name": "Ajay Kumar",
            "age": 32,
            "gender": "Male",
            "email": "ajay_kumar@example.com",
            "phone_number": "0987654321"
        },
        ...
    ]
    ```

## Search Query Explanation
The search API returns candidates sorted by the number of words in the search query that match the candidate’s name. The results are sorted in descending order of relevance.

### Example
If the search query is `Ajay Kumar Yadav`, the results will be sorted as follows:
1. "Ajay Kumar Yadav"
2. "Ajay Kumar"
3. "Ajay Yadav"
4. "Kumar Yadav"
5. "Ramesh Yadav"
6. "Ajay Singh"

### Important Note:
The search is handled entirely via ORM queries for efficiency. No Python-based filtering or sorting is used.

## Management Command for Generating Test Data

This project includes a custom Django management command that generates random test candidate data. This is useful for testing and development purposes.

### Command Details

The command generates a specified number of random candidates and populates the `Candidate` table. It uses the `Faker` library to generate random names, ages, genders, emails, and phone numbers.

#### Usage

To generate test candidates, run the following command:

```bash
python manage.py generate_candidates --count <number>
