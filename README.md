# IMDB Movie & Reviews Scraper – A Fully Automated Data Extraction System

> "Hi, I found a gig like this on Upwork... but alas, I didn't have the fortune to buy connects. The market is brutally competitive, and I struggle to write compelling proposals. So, I decided to turn my rejection into a project — not just any project, but one that reflects my potential. I took up the challenge, added some extra functionalities for fun, and here we are. This is what I am capable of."

---

## 🔹 Project Summary
A full-fledged scraping + API + deployment solution that scrapes IMDb's Top 250 Movies, actor filmographies, and movie reviews — handles JavaScript-heavy content, cleans the data, stores it in PostgreSQL, and finally exposes it via beautiful FastAPI endpoints... and yes, it is live on Heroku!

---

## 🎓 Tech Stack
**Languages & Libraries:**
- Python
- Selenium
- BeautifulSoup
- Playwright
- Pandas

**Databases & ORM:**
- SQLite (initial)
- PostgreSQL (final)
- SQLAlchemy

**API Framework:**
- FastAPI + Uvicorn

**Deployment:**
- Render.com / Heroku (free-tier)
- `.env` for config

---

## 🚀 Features Implemented

### 🔘 Top 250 Movie Scraper
- Extracts titles, release years, IMDb ratings, and URLs.
- Saves structured data in CSV & JSON.

### 🔘 Actor Filmography Scraper
- Input: IMDb profile URL (e.g., Leonardo DiCaprio).
- Dynamically clicks on roles like Actor/Producer.
- Extracts roles, movie titles, and release years.

### 🔘 Movie Review Scraper
- Scrolls through infinite content using JavaScript scroll.
- Extracts top user reviews and avoids page slowdown.

---

## 🔧 Robust Error Handling
- Handles missing containers, gender-based selectors (Actor/Actress).
- Timeout & no-element exceptions covered with grace.
- Empty section logs, clear debug output.
- Clean session shutdown using `driver.quit()`.

---

## 📊 Data Storage
- CSV / JSON: For local validation.
- PostgreSQL: For deployment with full schema.
- SQLAlchemy ORM used with `.env` variable security.

---

## 🎮 API Development with FastAPI
**Endpoints:**
- `/movies` - Top 250 Movie data
- `/filmography` - Actor's movie history
- `/reviews` - User-generated reviews

**Additional Features:**
- 404 & 500 error management
- Response models and status validation

---

## 🚗 Deployment
- Heroku (free-tier)
- `Procfile`, `requirements.txt`, `runtime.txt` included
- `.env` is excluded via `.gitignore`
- PostgreSQL connected with automatic parsing of `DATABASE_URL`

---

## 🔍 How to Run It Locally?
```bash
# Clone the repo
git clone https://github.com/yourusername/imdb-scraper-api
cd imdb-scraper-api

# Set up a virtual environment
python -m venv env
source env/bin/activate   # On Windows: env\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up your .env file
cp .env.example .env
# Fill in your PostgreSQL credentials

# Run the API
uvicorn main_api:app --reload

# Visit endpoints
http://127.0.0.1:8000/movies
```

---

## 📄 Deliverables
- ✉ Clean and modular Python code
- ✉ Scraper scripts with dynamic handling
- ✉ CSV + JSON + PostgreSQL backups
- ✉ REST API built with FastAPI
- ✉ Deployed on Heroku.com

---

## 🔎 Why It Matters
This project wasn't just about proving technical skills. It was about determination, resourcefulness, and turning adversity into accomplishment. It highlights:

- Proficiency with modern scraping tools.
- Clean, production-ready REST APIs.
- Secure, cloud-integrated deployments.
- A strong grasp of edge cases and backend system design.

---

## 🚀 Final Thoughts
> If you've scrolled this far, dear recruiter/client, here's the kicker: I didn't just build a project. I built a case study of what I can deliver when given the opportunity.

And hey, if I can scrape IMDb so elegantly, imagine what I could build for *you*.

---

## ✨ Live Demo
> (will add after Heroku approves my account)

---

## 🙏 Special Thanks
To insomnia, curiosity, and a lack of Upwork connects.

---

## 🌐 Author
**Aman Ullah**  
Backend Developer | Automation Specialist | Tech Storyteller  
[GitHub](https://github.com/theamaan) | [LinkedIn](https://linkedin.com/in/amaanullah13) | [Upwork](https://www.upwork.com/freelancers/~013e11c314277db25b)

