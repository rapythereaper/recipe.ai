from functools import wraps
from flask import g, request, redirect, url_for,session
import requests
import setting
from datetime import datetime
import json
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get("USER"):
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

def only_not_loged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("USER"):
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def fill_with_image(recipe_dict):
    url = setting.PEXELS_API_URl
    headers = {'Authorization':setting.PEXELS_API_KEY} 
    try: 
        for i in recipe_dict:
            name=i["name"].split("-")[0].strip()
            payload = {'query':name, 'orientation ': 'square',"per_page":1}
            r = requests.get(url, params=payload,headers=headers)
            print(r.status_code)
            if r.status_code==200:
                data=r.json()
                i["img-url"]=data["photos"][0]["src"]["original"]
            else:
                i["img-url"]=None
    except:
        i["img-url"]=None
    
    return recipe_dict



def get_current_time_string():
    # Get the current time
    current_time = datetime.now().time()

    # Format the time as a string in "HH:mm" format
    time_string = current_time.strftime("%H:%M")

    return time_string