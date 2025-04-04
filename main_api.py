# File: main_api.py

from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from urllib.parse import quote

# ------------------------------------------------------------------------------
# Load environment variables from .env file
# ------------------------------------------------------------------------------
load_dotenv()

# ------------------------------------------------------------------------------
# Database Configuration using .env variables
# ------------------------------------------------------------------------------
DB_USERNAME = os.getenv("DB_USERNAME")
# URL-encode the password to handle special characters like '@'
DB_PASSWORD = quote(os.getenv("DB_PASSWORD"))
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "imdb_data")

if not all([DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    raise Exception("One or more required environment variables are missing.")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)
print("DATABASE_URL:", DATABASE_URL)

engine = create_engine(DATABASE_URL)

# ------------------------------------------------------------------------------
# Initialize FastAPI Application
# ------------------------------------------------------------------------------
app = FastAPI(
    title="IMDB Data API",
    description="API endpoints to access scraped IMDB data",
    version="1.0"
)

# ------------------------------------------------------------------------------
# API Endpoints
# ------------------------------------------------------------------------------
@app.get("/movies", response_model=list)
def get_top_movies():
    """Retrieve the top 250 movies from the database."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM top_250_movies"))
            movies = [dict(row._mapping) for row in result]
        return movies
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/filmography", response_model=list)
def get_filmography():
    """Retrieve filmography data from the database."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM filmography_roles"))
            filmography = [dict(row._mapping) for row in result]
        return filmography
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/reviews", response_model=list)
def get_movie_reviews():
    """Retrieve movie reviews from the database."""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM movie_reviews"))
            reviews = [dict(row._mapping) for row in result]
        return reviews
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ------------------------------------------------------------------------------
# Run the API locally using uvicorn:
# uvicorn main_api:app --reload
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
