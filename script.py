from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup
import os  # Import for environment variables

app = Flask(__name__)

# ✅ Scraper function (update URL & selectors as needed)
def scrape_sports_schedule():
    url = "https://www.livesportsontv.com/"  # Replace with the real sports schedule URL
    headers = {"User-Agent": "Mozilla/5.0"}  # Mimic a real browser

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()  # Raises an error for non-200 responses
    except requests.RequestException as e:
        print(f"Error fetching data: {e}")
        return [{"title": "Error fetching data", "time": "Try again later"}]

    soup = BeautifulSoup(response.text, "html.parser")
    events = soup.find_all("div", class_="event")  # Adjust selector for actual site

    schedule = []
    for event in events:
        title = event.find("h3").text.strip() if event.find("h3") else "No Title"
        time = event.find("span", class_="time").text.strip() if event.find("span", class_="time") else "No Time"
        schedule.append({"title": title, "time": time})

    return schedule if schedule else [{"title": "No events found", "time": "Check later"}]

@app.route("/")
def home():
    sports_schedule = scrape_sports_schedule()
    return render_template("index.html", schedule=sports_schedule)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Uses environment variable for the port, defaults to 5000
    app.run(host="0.0.0.0", port=port, debug=True)  # Makes it accessible on Render
