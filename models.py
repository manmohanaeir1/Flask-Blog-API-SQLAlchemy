from . import db
from sqlalchemy.sql import func

class Users(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(200),  nullable=False)
    lastName = db.Column(db.String(200),  nullable=False)
    email = db.Column(db.String(200), unique=True,  nullable=False)
    password = db.Column(db.String(255),  nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(),  nullable=False)
    blogs = db.relationship('Blogs', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.firstName} {self.id}>'

class Blogs(db.Model):
    __tablename__ = 'Blogs'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    title = db.Column(db.String(200),  nullable=False)
    content = db.Column(db.String(1000),  nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now(),  nullable=False)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'title': self.title,
            'content': self.content,
            'created_at': self.created_at
        }