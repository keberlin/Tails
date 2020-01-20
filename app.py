from flask import Flask, render_template

import stores

# Flask application
application = Flask(__name__)
application.debug = True

# Initialise the stores data (from stores.json)
harness = stores.Stores()

# Ensure that each store's location has been populated
harness.populate_location_info()


# Route for html page 'stores'
@application.route("/stores")
def html_stores():
    stores = harness.sort_by_name()
    return render_template("stores.html", stores=stores)


if __name__ == "__main__":
    application.run(host="0.0.0.0", port=81)
