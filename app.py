from flask import Flask,request,session
from flask import render_template
from flask import abort, redirect, url_for
from werkzeug.utils import secure_filename
from datetime import datetime
#import sys
#sys.path.append("./recipe_recomendation")
import recipe_recomendation.recipie_recomendation as rcp_recomendation

import json
import requests

import setting
import flask_util
import db


app = Flask(__name__)
app.secret_key = setting.APP_SECRETE_KEY


    
@app.route("/")
@flask_util.login_required
def home():
    if not session.get("USER"):
        return redirect()
    return render_template("home.jinja",user=session["USER"])

@app.route("/login",methods=["POST","GET"])
@flask_util.only_not_loged_in
def login():
    if request.method=="GET":
        return render_template("login.jinja")
    if request.method=="POST":
        phone_num=request.form["phone_num"]
        passowrd=request.form["password"]
        user=db.User.select().where(db.User.phone_num==phone_num)
        if not user.exists():
            return render_template("login.jinja",error_msg="User doesnot exist")
        user=user.get()
        if user.check_password(passowrd):
            session["USER"]=user.to_dict()
            print(f"[+] {session['USER']['phone_num']} Loged in ...")
            return redirect(url_for("home"))
        return render_template("login.jinja",error_msg="Incorrect passowrd")

@app.route("/logout",methods=["POST"])
@flask_util.login_required
def logout():
    session.pop('USER', None)
    return redirect(url_for('home'))

@app.route("/register",methods=["POST","GET"])
@flask_util.only_not_loged_in
def register():
    if request.method=="GET":
        return render_template("register.jinja")
    if request.method=="POST":
        phone_num=request.form["phone_num"]
        passowrd=request.form["password"]
        uname=request.form["u_name"]
        if len(phone_num)!=10 or not phone_num.isdigit():
            return render_template("register.jinja",error_msg="Please enter a valid number")
        
        user=db.User.select().where(db.User.phone_num==phone_num)
        if user.exists():
            return render_template("register.jinja",error_msg="User already exist with given phone number")
        
        user=db.User(u_name=uname,phone_num=phone_num)
        user.set_password(passowrd)
        user.save()
        return redirect(url_for("home"))

@app.route("/recomendation",methods=["POST","GET"])
@flask_util.login_required
def recomendation():
    if request.method=="GET":
        data=rcp_recomendation.get_random_recomendation(N=5,to_dict=True)
        #data=flask_util.fill_with_image(data)
        return render_template("recomendation.jinja",user=session["USER"],rcp=data,query=None)
    if request.method=="POST":
        query=request.form["query"]
        data=rcp_recomendation.get_recomendation(query,N=5,to_dict=True)
        #data=flask_util.fill_with_image(data)
        return render_template("recomendation.jinja",user=session["USER"],rcp=data,query=query)

@app.route("/recomendation/<int:rcp_id>",methods=["GET"])
@flask_util.login_required
def recomendation_id(rcp_id):
    data=rcp_recomendation.get_by_id(rcp_id,to_dict=True)[0]
    return render_template("recomendation_id.jinja",user=session["USER"],rcp=data)

@app.route("/meal_planning",methods=["GET","POST"])
@flask_util.login_required
def meal_planning():
    days=["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    slide_to=0
    if request.method=="POST":
        action=request.form["action"]
        u_id=session["USER"]["id"]
        slide_to=days.index(request.form["day"])
        if action=="add" :
            day=request.form["day"]
            time=request.form["time"]
            food=request.form["food"]
            
            meal_record=db.MealPlan(u_id=u_id,day=day,time=time,food=food)
            meal_record.save()
        if action=="delete":
            m_id=request.form["id"]
            record=db.MealPlan.delete().where((db.MealPlan.id==m_id) & (db.MealPlan.u_id==u_id))
            record.execute()
        if action=="edit":
            time=request.form["time"]
            food=request.form["food"]
            m_id=request.form["id"]
            record=db.MealPlan.update({db.MealPlan.food:food,
                                        db.MealPlan.time:time
                                    }).where((db.MealPlan.id==m_id) & (db.MealPlan.u_id==u_id))
            record.execute()
            


    meal={}
    for i in days:
        meal[i]=[]
    for i in db.MealPlan.select().where(db.MealPlan.u_id==session["USER"]["id"]):
        meal[i.day].append(i.to_dict())
    
    return render_template("meal_planing.jinja",user=session["USER"],meal=meal,slide_to=slide_to)

@app.route("/inventory",methods=["GET","POST"])
@flask_util.login_required
def inventory():
    if request.method=="POST":
        action=request.form["action"]
        u_id=session["USER"]["id"]
        if action=="add" :
            label=request.form["label"]
            status=0
            api_key=db.Inventory.gen_api_key()
            record=db.Inventory(u_id=u_id,label=label,status=status,api_key=api_key)
            record.save()
        if action=="delete":
            m_id=request.form["id"]
            record=db.Inventory.delete().where((db.Inventory.id==m_id) & (db.Inventory.u_id==u_id))
            record.execute()


    inventory=[]
    for i in db.Inventory.select().where(db.Inventory.u_id==session["USER"]["id"]):
        inventory.append(i.to_dict())
    return render_template("inventory.jinja",user=session["USER"],inventory=inventory)

@app.route("/api/inventory",methods=["POST","GET"])
def inventory_api():
    if request.method=="GET":
        if not session.get("USER"):
            return "Login required",404
        inventory=[]
        for i in db.Inventory.select().where(db.Inventory.u_id==session["USER"]["id"]):
            inventory.append(i.to_dict())
        return inventory

    if request.method=="POST":
        api_key=request.form["api_key"]
        status=request.form["status"]
        record=db.Inventory.update({db.Inventory.status:status
                                        }).where((db.Inventory.api_key==api_key))
        record.execute()
        return ""



@app.route("/api/notification",methods=["GET","POST"])
@flask_util.login_required
def notification_api():
    time=flask_util.get_current_time_string()
    dt = datetime.now()
    day=dt.strftime('%A')
    meal_plan=[]
    inventory=[]
    for i in db.MealPlan.select().where((db.MealPlan.u_id==session["USER"]["id"]) & 
                                        (db.MealPlan.day==day)):
        meal_plan.append(i.to_dict())
    

    return {"inventory":None,"meal_plan":meal_plan}


@app.route("/notification",methods=["GET"])
@flask_util.login_required
def notification():
    time=flask_util.get_current_time_string()
    dt = datetime.now()
    day=dt.strftime('%A')
    occured=[]
    to_occur=[]
    current_time = [int(i) for i in dt.strftime("%H:%M").split(":")]
    for i in db.MealPlan.select().where((db.MealPlan.u_id==session["USER"]["id"]) & 
                                        (db.MealPlan.day==day)):
        d=i.to_dict()
        t=[int(j) for j in d["time"].split(":")]
        if current_time[0]==t[0] :
            if current_time[1]<t[1]: to_occur.append(d)
            else: occured.append(d)
        elif current_time[0]<t[0] :
            to_occur.append(d)
        else :
            occured.append(d)
    #data={"inventory":None,"meal_plan":meal_plan}
    
    return render_template("notification.jinja",user=session["USER"],occured=occured,to_occur=to_occur)


@app.route("/image_recognization",methods=["GET"])
@flask_util.login_required
def image_recognization():
    return render_template("image_recognization.jinja",user=session["USER"])

app.run(host="0.0.0.0", port=8080,debug=True)