# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

api = Api(app)
movie_ns = api.namespace("movies")


class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    description = db.Column(db.String(255))
    trailer = db.Column(db.String(255))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"))
    genre = db.relationship("Genre")
    director_id = db.Column(db.Integer, db.ForeignKey("director.id"))
    director = db.relationship("Director")


class MovieSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Int()
    rating = fields.Float()
    genre_id = fields.Int()
    genre = fields.Str()
    director_id = fields.Int()
    director = fields.Str()


movie_schema = MovieSchema()
movies_schema = MovieSchema(many=True)


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


@movie_ns.route("/")
class BasedView(Resource):
    def get(self):
        all_movies = Movie.query.all()
        director_id = request.args.get('director_id')
        genre_id = request.args.get('genre_id')
        if director_id:
            result = Movie.query.filter_by(director_id=director_id).all()
            return movies_schema.dump(result), 200
        if genre_id:
            result = Movie.query.filter_by(genre_id=genre_id).all()
            return movies_schema.dump(result), 200
        return movies_schema.dump(all_movies), 200


@movie_ns.route("/<int:uid>")
class BasedView(Resource):
    def get(self, uid: int):
        try:
            book = Movie.query.get(uid)
            return movie_schema.dump(book), 200
        except Exception:
            return "", 404


if __name__ == '__main__':
    app.run(debug=True)
