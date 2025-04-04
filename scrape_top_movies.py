import time
import pandas as pd
import re
from selenium.webdriver.common.by import By
from driver_setup import driver  # Import the Edge driver instance

def scrape_top_250():
    url = "https://www.imdb.com/chart/top/"
    driver.get(url)
    time.sleep(3)  

    # Find all movie title containers (inside <a> tags)
    movie_elements = driver.find_elements(By.XPATH, "//a[@class='ipc-title-link-wrapper']/h3[@class='ipc-title__text']")
    
    # Find all rating elements
    rating_elements = driver.find_elements(By.CLASS_NAME, "ipc-rating-star--rating")
    
    # Find all metadata divs and get the first span (release year)
    year_elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'cli-title-metadata')]/span[1]")

    movies = []
    for title_elem, rating_elem, year_elem in zip(movie_elements, rating_elements, year_elements):
        try:
            # Extract and clean movie title
            full_title = title_elem.text.strip()
            title = re.sub(r"^\d+\.\s", "", full_title)  # Remove rank number
            
            # Extract other fields
            rating = rating_elem.text.strip()
            release_year = year_elem.text.strip()

            movies.append({"Title": title, "Year": release_year, "Rating": rating})
        except Exception as e:
            print(f"Error parsing movie data: {e}")

    # Save to CSV
    df = pd.DataFrame(movies)
    df.to_csv("top_250_movies.csv", index=False, encoding="utf-8")
    print("Data saved to top_250_movies.csv")

if __name__ == "__main__":
    scrape_top_250()
    driver.quit()
