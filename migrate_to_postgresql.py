# File: migrate_to_postgresql.py
import os
import pandas as pd
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from urllib.parse import quote

# ----------------------------------------------------------------------
# Configure Logging
# ----------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Load environment variables from .env file
load_dotenv()

# ----------------------------------------------------------------------
# Step 1: Retrieve Database Configuration
# ----------------------------------------------------------------------
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = quote(os.getenv("DB_PASSWORD", ""))  # URL-encode password
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

if not all([DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME]):
    logging.error("One or more required database credentials are missing in .env. Exiting.")
    exit(1)

DATABASE_URL = f"postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# ----------------------------------------------------------------------
# Step 2: Create SQLAlchemy Engine
# ----------------------------------------------------------------------
try:
    engine = create_engine(DATABASE_URL)
    logging.info("Database engine created successfully.")
except Exception as e:
    logging.error("Failed to create database engine: %s", e)
    exit(1)

# ----------------------------------------------------------------------
# Step 3: Migrate CSV Files to PostgreSQL
# ----------------------------------------------------------------------
def migrate_csv_to_table(csv_filename, table_name):
    """Reads a CSV file and writes its contents to a PostgreSQL table."""
    try:
        df = pd.read_csv(csv_filename)
        logging.info("Loaded '%s' with %d records.", csv_filename, len(df))
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        logging.info("Data from '%s' migrated to '%s' table successfully.", csv_filename, table_name)
    except Exception as e:
        logging.error("Error migrating '%s': %s", csv_filename, e)

# ----------------------------------------------------------------------
# Step 4: Migrate Each CSV File
# ----------------------------------------------------------------------
if __name__ == "__main__":
    csv_files = {
        "top_250_movies.csv": "top_250_movies",
        "filmography_roles.csv": "filmography_roles",
        "movie_reviews.csv": "movie_reviews",
    }

    for csv_file, table_name in csv_files.items():
        migrate_csv_to_table(csv_file, table_name)

    logging.info("All migrations completed successfully.")
