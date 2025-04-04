# File: main.py
from scrape_top_movies import scrape_top_250
from scrape_filmography import scrape_filmography
from scrape_reviews import scrape_movie_reviews
from driver_setup import driver  # Ensure the driver is only instantiated once

def main():
    # Task A: Scrape Top 250 Movies
    scrape_top_250()
    
    # Task B: Scrape Filmography (Example: Leonardo DiCaprio)
    actor_url = "https://www.imdb.com/name/nm0000189/"
    scrape_filmography(actor_url)
    
    # Task C: Scrape Reviews (Example: The Shawshank Redemption)
    reviews_url = "https://www.imdb.com/title/tt1663202/reviews/"
    scrape_movie_reviews(reviews_url, max_reviews=30)

if __name__ == "__main__":
    main()
    driver.quit()  # Terminate the browser session at the end of the project
