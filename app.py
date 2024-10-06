from flask import Flask, render_template, request, url_for
import requests

app = Flask(__name__)

GOOGLE_API_KEY = 'AIzaSyC4fSVZFjeTaZhcbV8aWmkYLAIBvEVZR_s'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/marketplace')
def marketplace():
    location = '1.3521,103.8198'  # Latitude and Longitude for Singapore
    radius = 50000  # Search radius in meters
    query = 'apartment for rent in Singapore'
    url = f"https://maps.googleapis.com/maps/api/place/textsearch/json?query={query}&location={location}&radius={radius}&key={GOOGLE_API_KEY}"

    response = requests.get(url)
    data = response.json()

    # Check if the response contains results
    if data.get('status') == 'OK':
        properties = data.get('results', [])

        # Add photo URL and Google Maps link to each property if available
        for property in properties:
            # Add photo URL if available
            if 'photos' in property:
                photo_reference = property['photos'][0]['photo_reference']
                photo_url = f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference={photo_reference}&key={GOOGLE_API_KEY}"
                property['photo_url'] = photo_url
            else:
                property['photo_url'] = url_for('static', filename='images/no_image.png')

            # Add link to the place details on Google Maps
            property['place_url'] = f"https://www.google.com/maps/place/?q=place_id:{property['place_id']}"

    else:
        properties = []

    return render_template('marketplace.html', properties=properties)

if __name__ == "__main__":
    app.run(debug=True)
