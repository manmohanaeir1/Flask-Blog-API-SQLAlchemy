from . import app , db
from flask import request, jsonify, make_response 
from .models import Users, Blogs
from werkzeug.security import generate_password_hash, check_password_hash

from datetime import datetime, timedelta

from functools import wraps
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

        return make_response(jsonify({"token": token}), 200)
     
     return make_response(
            {
                "message": "Invalid password"
            }, 401
        )

   

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return make_response(
                {
                    "message": "Token is missing!"
                }, 401
            )
        try:
            data = jwt.decode(token, "secret", algorithms=["HS256"])
            current_user = Users.query.filter_by(id=data['id']).first()
        except:
            return make_response(
                {
                    "message": "Token is invalid"
                }, 401
            )
        return f(current_user, *args, **kwargs)
    return decorated

@app.route("/blogs", methods=["GET"])
@token_required
def get_blogs(current_user):
    blogs = Blogs.query.filter_by(user_id=current_user.id).all()
    return make_response(
        {
            "blogs": [blog.serialize for blog in blogs]
        }, 200
    )

@app.route("/blogs", methods=["POST"])
@token_required
def create_blog(current_user):
    data = request.json
    title = data.get("title")
    content = data.get("content")

    if title and content:
        blog = Blogs(
            user_id=current_user.id,
            title=title,
            content=content
        )
        db.session.add(blog)
        db.session.commit()
        return make_response(
            {
                "message": "Blog created successfully"
            }, 201
        )
    return make_response(
        {
            "message": "Please provide all required fields"
        }, 400
    )