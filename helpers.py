import pytz
import requests
from flask import redirect, render_template, session

from functools import wraps

def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def apology(message, linkmsg, link):
    return render_template("apology.html", Message=message, linkmsg=linkmsg, link=link)

def get_services():
   services = ['Plumbing', 'Photography','Fashion & Lifestyle', 'Furniture/Wood Work', 'Food and Catering', 'Electrical/Electronics Repairs & Maintenance', 'Computer/IT-Services', 'Teaching/Education', 'Welding/Metal Work', 'Beauty and Salon', 'Auto Repairs', 'Laundry and Cleaning', 'Transportation services', 'Farming and Agriculture'] 
   return services


