# File: scrape_reviews.py
import time
import logging
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from driver_setup import driver  # Import the Edge driver instance

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def click_hide_spoilers_checkbox():
    """
    Locates and clicks the "Hide spoilers" checkbox.
    """
    try:
        logging.info("Locating 'Hide spoilers' checkbox.")
        # Wait until the checkbox is present in the DOM.
        checkbox = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[aria-label='Hide spoilers']"))
        )
        logging.info("Scrolling 'Hide spoilers' checkbox into view.")
        driver.execute_script("arguments[0].scrollIntoView(true);", checkbox)
        logging.info("Clicking 'Hide spoilers' checkbox.")
        driver.execute_script("arguments[0].click();", checkbox)
        logging.info("'Hide spoilers' checkbox clicked.")
        time.sleep(5)  # Allow the page to update after clicking
    except Exception as e:
        logging.error("Unable to click 'Hide spoilers' checkbox: %s", e)
        # Continue processing even if this step fails.

def extract_reviews(max_reviews=20):
    """
    Extracts review titles and review texts from the reviews page.
    Returns a list of dictionaries with keys "Review Title" and "Review Text".
    """
    reviews = []
    try:
        logging.info("Waiting for review title elements to be present.")
        review_title_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "div[data-testid='review-summary'] a.ipc-title-link-wrapper h3.ipc-title__text")
            )
        )
        logging.info("Review title elements found: %d", len(review_title_elements))
        
        # Review texts may load dynamically; locate them after the titles.
        review_text_elements = driver.find_elements(By.CSS_SELECTOR, "div.ipc-html-content-inner-div[role='presentation']")
        logging.info("Review text elements found: %d", len(review_text_elements))
        
        # Iterate over the paired elements (titles and texts).
        for idx, (title_elem, text_elem) in enumerate(zip(review_title_elements, review_text_elements)):
            if idx >= max_reviews:
                break
            review_title = title_elem.text.strip()
            review_text = text_elem.text.strip()
            reviews.append({"Review Title": review_title, "Review Text": review_text})
            logging.info("Extracted review %d: %s", idx + 1, review_title)
    except Exception as e:
        logging.error("Error extracting reviews: %s", e)
    return reviews

def scrape_movie_reviews(movie_reviews_url, max_reviews=20):
    """
    Navigates to the movie reviews URL, clicks the 'Hide spoilers' checkbox,
    extracts up to max_reviews reviews, and saves them in CSV format.
    """
    logging.info("Navigating to movie reviews URL: %s", movie_reviews_url)
    driver.get(movie_reviews_url)
    time.sleep(3)  # Allow reviews to load

    # Click the "Hide spoilers" checkbox.
    click_hide_spoilers_checkbox()

    # Extract reviews.
    reviews = extract_reviews(max_reviews=max_reviews)
    if reviews:
        df = pd.DataFrame(reviews)
        df.to_csv("movie_reviews.csv", index=False, encoding="utf-8")
        logging.info("%d reviews saved to movie_reviews.csv", len(reviews))
    else:
        logging.warning("No reviews were extracted.")

if __name__ == "__main__":
    # Example movie reviews URL (The Shawshank Redemption)
    reviews_url = "https://www.imdb.com/title/tt0111161/reviews"
    scrape_movie_reviews(reviews_url)
    driver.quit()
