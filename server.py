from flask import Flask, render_template, request

from pprint import pformat
import os
import requests


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['TICKETMASTER_KEY']

@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')


@app.route('/afterparty')
def show_afterparty_form():
    """Show event search form"""

    return render_template('search-form.html')


@app.route('/afterparty/search')
def find_afterparties():
    """Search for afterparties on Eventbrite"""


    keyword = request.args.get('keyword', '')
    postalcode = request.args.get('zipcode', '')
    radius = request.args.get('radius', '')
    unit = request.args.get('unit', '')
    sort = request.args.get('sort', '')

#   print ("####################################")
#   print ("keyword: ", keyword)
#   print ("postalcode: ", postalcode)
#   print ("radius: ", radius)
#   print ("unit: ", unit)      
#   print ("sort: ", sort)


    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey': API_KEY, 'postalCode': postalcode, 'radius': radius, 'unit': unit, 'keyword': keyword, 'sort': sort}
    # payload = {'apikey': API_KEY, 'postalCode': '94102', 'keyword': keyword}
    print ("    our payload is: ", payload)


    results = requests.get(url, params=payload)

    data = results.json()
    # TODO: Make a request to the Event Search endpoint to search for events
    #
    # - Use form data from the user to populate any search parameters
    #
    # - Make sure to save the JSON data from the response to the `data`
    #   variable so that it can display on the page. This is useful for
    #   debugging purposes!
    #
    # - Replace the empty list in `events` with the list of events from your
    #   search results

    if '_embedded' in data:
        events = data['_embedded']['events']
    else:
        events = []


    return render_template('search-results.html',
                           pformat=pformat,
                           data=data,
                           results=events)


# ===========================================================================
# FURTHER STUDY
# ===========================================================================


@app.route('/event/<id>')
def get_event_details(id):
    """View the details of an event."""

    url = f'https://app.ticketmaster.com/discovery/v2/events/{id}'
    payload = {'apikey': API_KEY}

#    print (" ********* id: ", id)
#    results = requests.get(url, params=id)
    results = requests.get(url, params=payload)
    print (" ------- endpoint for single event: ", results.url)

    data = results.json()

    name = data['name']
    date = data['dates']['start']['localDate']
    time = data['dates']['start']["localTime"]

    venue = data['_embedded']['venues'][0]
    venue_name = venue['name']    

    event_detials = []

    return render_template('event-details.html', name = name, date = date, venue= venue_name, time= time )


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
