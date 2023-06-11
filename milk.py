from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup
import json
import re

app = Flask(__name__)

state_mapping = {
    'al': 'alabama',
    'ak': 'alaska',
    'az': 'arizona',
    'ar': 'arkansas',
    'ca': 'california',
    'co': 'colorado',
    'ct': 'connecticut',
    'de': 'delaware',
    'fl': 'florida',
    'ga': 'georgia',
    'hi': 'hawaii',
    'id': 'idaho',
    'il': 'illinois',
    'in': 'indiana',
    'ia': 'iowa',
    'ks': 'kansas',
    'ky': 'kentucky',
    'la': 'louisiana',
    'me': 'maine',
    'md': 'maryland',
    'ma': 'massachusetts',
    'mi': 'michigan',
    'mn': 'minnesota',
    'ms': 'mississippi',
    'mo': 'missouri',
    'mt': 'montana',
    'ne': 'nebraska',
    'nv': 'nevada',
    'nh': 'new-hampshire',
    'nj': 'new-jersey',
    'nm': 'new-mexico',
    'ny': 'new-york',
    'nc': 'north-carolina',
    'nd': 'north-dakota',
    'oh': 'ohio',
    'ok': 'oklahoma',
    'or': 'oregon',
    'pa': 'pennsylvania',
    'ri': 'rhode-island',
    'sc': 'south-carolina',
    'sd': 'south-dakota',
    'tn': 'tennessee',
    'tx': 'texas',
    'ut': 'utah',
    'vt': 'vermont',
    'va': 'virginia',
    'wa': 'washington',
    'wv': 'west-virginia',
    'wi': 'wisconsin',
    'wy': 'wyoming'
}

# Route for homepage
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

# Route for searching raw milk data based on state
@app.route('/search', methods=['GET'])
def search():
    state = request.args.get('state', default = 'arkansas', type = str).lower()
    state = state_mapping.get(state, state)  
    url = f'https://getrawmilk.com/search/{state}'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    script_tag = soup.find('script', {'type': 'application/json'})
    json_str = script_tag.string
    data = json.loads(json_str)
    listings = data['props']['pageProps']['listings']
    results = []
    
    # Loop over each listing
    for listing in listings:
        # location 
        location = listing['location']
        # address
        address = re.search('^(.*\d{5})', location['formattedAddress']).group(1)
        # farm name
        farm_name = listing.get('name')
        # phone number
        phone_number = listing.get('phone')
        # email address
        email_address = listing.get('email')

        # Add the result to the results list
        results.append({
            'Location': location['coordinates'],
            'Address': address,
            'Farm Name': farm_name,
            'Phone Number': phone_number,
            'Email Address': email_address
        })

    # Render the results
    return render_template('results.html', results=results)

if __name__ == "__main__":
    app.run(debug=True)
