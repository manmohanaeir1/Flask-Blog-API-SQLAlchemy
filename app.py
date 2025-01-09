from . import app , db
from flask import request, make_response 
from .models import Users, Blogs
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta
import jwt

@app.route("/signup", methods=["POST"])
def signup():
    data = request.json
    email = data.get("email")
    firstName = data.get("firstName")   
    lastName = data.get("lastName")
    password = data.get("password")

    if firstName and lastName and email and password:
       user = Users.query.filter_by(email=email).first()
       if user:
           return make_response(
               {
                   "message": "User already exists"
               }, 200
           )
       user = Users(
                email=email,
                firstName=firstName,
                lastName=lastName,
                password=generate_password_hash(password)
              
         )
       db.session.add(user)
       db.session.commit()
       return make_response(
              {
                "message": "User created successfully"
              }, 201
         )
     
       return make_response(
            {
                "message": "Please provide all required fields"
            }, 400
        )
    
        
       
@app.route("/login", methods=["POST"])  #thisis the login route
def login():
     auth = request.json
     if not auth or not auth.get("email") or not auth.get("password"):
         return make_response(
             {
                 "message": "Please provide email and password"
             }, 400
         ) 
     
     user = Users.query.filter_by(email=auth.get("email")).first()
     if not user: 
         return make_response(
                {
                    "message": "User does not exist ! Please signup"
                }, 404
            )
     if check_password_hash(user.password, auth.get("password")):
        token = jwt.encode(
            {
                'id': user.id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            },
            "secret",
            "HS256"
        )

        return make_response({'token': token}, 201)
        return make_response(
                {
                    "message": "Invalid password! Please try again"
                }, 401
            )
     
     