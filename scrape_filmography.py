# File: scrape_filmography.py
import time
import logging
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from driver_setup import driver  # Import the Edge driver instance

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def click_expand_button():
    """
    Scrolls to and clicks the 'Expand below' button to reveal filmography details.
    """
    try:
        logging.info("Locating 'Expand below' button.")
        expand_button = driver.find_element(
            By.CSS_SELECTOR, "button[data-testid='nm-flmg-all-accordion-expander']"
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", expand_button)
        logging.info("Waiting for 'Expand below' button to be clickable.")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-testid='nm-flmg-all-accordion-expander']"))
        )
        driver.execute_script("arguments[0].click();", expand_button)
        logging.info("'Expand below' button clicked successfully.")
        time.sleep(5)  # Allow expanded content to load
    except Exception as e:
        logging.error("Unable to click 'Expand below' button: %s", e)
        raise e

def get_container_ids(role, section):
    """
    Returns a list of possible container IDs for a given role and section.
    For 'Actor', both actor and actress containers are tried.
    """
    role_key = role.lower()
    section_key = section.lower()
    if role_key == "actor":
        return [f"accordion-item-actor-{section_key}-projects",
                f"accordion-item-actress-{section_key}-projects"]
    else:
        return [f"accordion-item-{role_key}-{section_key}-projects"]

def process_role_section(role, section):
    """
    Processes a filmography section for a given role and section type.
    
    Parameters:
      role (str): The filmography role (e.g., 'Producer', 'Actor', 'Writer', or 'Actress').
      section (str): The section type (e.g., 'Upcoming' or 'Previous').
      
    Returns:
      list: A list of movie titles captured from the specified section.
    """
    container_ids = get_container_ids(role, section)
    movies = []
    container_found = False

    for cid in container_ids:
        try:
            logging.info("Attempting to locate container with id: %s", cid)
            container = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.ID, cid))
            )
            container_found = True
            logging.info("Container located: %s", cid)
            movie_elements = container.find_elements(By.CSS_SELECTOR, "a.ipc-metadata-list-summary-item__t")
            movies = [movie.text.strip() for movie in movie_elements]
            break  # Stop after the first successful container is found
        except (TimeoutException, NoSuchElementException):
            logging.info("Container with id '%s' not found. Trying next option (if any).", cid)

    if not container_found:
        logging.info("No %s movies found for %s.", section, role)
    else:
        logging.info("%s %s movies found: %s", role, section, movies)
    return movies

def scrape_filmography(actor_url):
    logging.info("Navigating to actor URL: %s", actor_url)
    driver.get(actor_url)
    time.sleep(5)  # Allow the page to load completely

    # Click the "Expand below" button
    try:
        click_expand_button()
    except Exception as e:
        logging.error("Aborting filmography scraping due to error with expand button.")
        return

    # Define the roles to process.
    # For actor profiles, the header might be 'Actor' or 'Actress'. We handle that in get_container_ids.
    roles = ["Producer", "Actor", "Writer"]
    results = {}

    # Process each section (Upcoming and Previous) for each role.
    for role in roles:
        for section in ["Upcoming", "Previous"]:
            key = f"{role} {section}"
            movies = process_role_section(role, section)
            results[key] = ", ".join(movies)

    logging.info("Captured role data: %s", results)

    # Export the captured data to CSV (as a single row).
    df = pd.DataFrame([results])
    df.to_csv("filmography_roles.csv", index=False, encoding="utf-8")
    logging.info("Data saved to filmography_roles.csv")

if __name__ == "__main__":
    # Example actor URL (Leonardo DiCaprio or any profile)
    actor_url = "https://www.imdb.com/name/nm0000138/"
    driver.maximize_window()
    scrape_filmography(actor_url)
    driver.quit()
