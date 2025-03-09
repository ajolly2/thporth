from flask import Flask, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

# ✅ Scraper function (update URL & selectors as needed)
def scrape_sports_schedule():
    url = "https://www.livesportsontv.com/"  # Replace with the real sports schedule URL
    headers = {"User-Agent": "Mozilla/5.0"}  # Mimic a real browser

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        return [{"title": "Error fetching data", "time": "Try again later"}]

    soup = BeautifulSoup(response.text, "html.parser")
    events = soup.find_all("div", class_="event")  # Adjust to match the actual site

    schedule = []
    for event in events:
        title = event.find("h3").text if event.find("h3") else "No Title"
        time = event.find("span", class_="time").text if event.find("span", class_="time") else "No Time"
        schedule.append({"title": title, "time": time})

    return schedule

@app.route("/")
def home():
    sports_schedule = scrape_sports_schedule()
    return render_template("index.html", schedule=sports_schedule)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # Makes it accessible on Render
