# Freemasons flask app
a web app that shows you the info of the  freemasons in your city as long as they create a profile on the app and add their details, only works in nigeria for now.


This is a Flask web application that allows users to register, login, update their profile, and interact with various services.

## Features

- User registration and login with password hashing for security.
- Profile editing where users can update their details.
- Location fetching using the Geopy library.
- Fetching towns and cities based on the state selected by the user.
- Image uploading and retrieval.
- Fetching and displaying services, states, towns, masons, and user details.
- Profile updating with validation to ensure at least one detail is provided.

## Libraries Used

- Flask: A micro web framework written in Python.
- Flask-Session: A Flask extension for handling server-side sessions.
- CS50: A library for teaching purposes.
- Werkzeug: A comprehensive WSGI web application library.
- Requests: A simple HTTP library for Python.
- Geopy: A client for several popular geocoding web services.
- JSON: A lightweight data interchange format.
- OS: Provides functions for interacting with the operating system.
- Random: Implements pseudo-random number generators for various distributions.

## Installation

1. Clone the repository.
2. Install the dependencies using `pip install -r requirements.txt`.
3. Run the application using `flask run`.

## Usage

Visit the homepage and register as a new user. After logging in, you can edit your profile by filling in the form with your details. You can also interact with various services and fetch location, town, and city details.


## License

MIT

