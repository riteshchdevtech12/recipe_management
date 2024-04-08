from sqlalchemy.dialects.postgresql import JSON

from app import db
from app.crud import CRUDBase


class Recipe(CRUDBase, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text)
    ingredients = db.Column(JSON)
    instructions = db.Column(db.Text)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('recipes', lazy=True))

    def __repr__(self):
        return '<Recipe {}>'.format(self.title)
