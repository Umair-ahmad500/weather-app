from flask import Flask, render_template, request
import requests

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():

    weather = None
    error = None

    if request.method == "POST":

        city = request.form["city"]

        url = f"https://wttr.in/{city}?format=j1"

        try:
            response = requests.get(url)

            if response.status_code == 200:

                data = response.json()

                current = data["current_condition"][0]

                weather = {
                    "city": city,
                    "temperature": current["temp_C"],
                    "feels_like": current["FeelsLikeC"],
                    "humidity": current["humidity"],
                    "wind": current["windspeedKmph"],
                    "condition": current["weatherDesc"][0]["value"]
                }

            else:
                error = "Could not find weather information."

        except Exception:
            error = "Something went wrong. Please try again."

    return render_template(
        "index.html",
        weather=weather,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)