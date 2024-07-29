
# NutriPix API

NutriPix API is an API that was made based on the NutriPix mobile application. NutriPix is an interactive educational tool designed to help children learn about nutrition in a fun and engaging way. By using image classification technology, NutriPix can identify various fruits and vegetables and provide interesting facts and nutritional information about them.

## API Features

- **Image Classification**: Identifies fruits and vegetables from images taken by the user. As of right now, it can identifies 6 types of fruits and vegetables which are: Apples, Bananas, Broccolis, Grapes, Mangoes, and Strawberries.
- **User Authentication and Authorization**: Uses token-based authentication using JSON Web Tokens (JWT).

## Getting Started

### Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.x, preferably 3.10
- PostgreSQL client, e.g. pgAdmin
- A modern web browser (for web-based applications)


## Run Locally

1. Clone the repository:
```bash
git clone https://github.com/dha-lang/Nutripix-API.git
```

2. Navigate to the project directory:
```bash
cd nutripix-api
```

3. Make a virtual environment and activate the virtual environment:
```bash
python -m venv .venv

.venv/Scripts/Activate.ps1
```

4. Install the required dependencies:
```bash
pip install -r requirements.txt
```

5. Create the PostgreSQL database:
You can use pgAdmin to make the PostgreSQL database.

6. Create and assign variables on the .env file:
You can follow the **.env.example** file for guide.

7. Create static and images folder for temporary image storage:
```bash
From the nutripix-api directory:

mkdir static

cd static

mkdir images
```
The file structure now should look like this:

nutripix-api/
│
│ ── app
│ ── model
│ ── static/
│ └──  images
.
.
.

8.Start the uvicorn server:
```bash
  uvicorn app.main:app
```

Open your web browser and navigate to 'http://127.0.0.1:8000/docs' to try the API.

## Tech Stack
### ML Model
Mediapipe and Mediapipe Model Maker for customized model.

### API
- FastAPI
- PostgreSQL

_For more detailed used technologies, see the requirements.txt file._ 


## License

This project is licensed under the [MIT](https://choosealicense.com/licenses/mit/) License. 
