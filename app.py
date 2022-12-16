# app.py

from flask import Flask, request
from flask_restx import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


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

class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))


class MovieSchema(Schema):
    id = fields.Int()
    title = fields.Str()
    description = fields.Str()
    trailer = fields.Str()
    year = fields.Str()
    rating = fields.Float()
    genre = fields.Str()
    director = fields.Str()


class DirectorSchema(Schema):
    id = fields.Int()
    name = fields.Str()


class GenreSchema(Schema):
    id = fields.Int()
    name = fields.Str()


# единичная сериализация
movie_schema = MovieSchema()
director_schema = DirectorSchema()
genre_schema = GenreSchema()

# множественная сериализация
movie_schema = MovieSchema(many=True)
director_schema = DirectorSchema(many=True)
genre_schema = GenreSchema(many=True)

# эндпоинт мувис
api = Api(app)
movies_ns = api.namespace('movies')


# функция сериализатор
def serializ(model, object):
    dct = model.dump(object)
    return dct


# функция десериализатор
def deserializ(model, object):
    dct = model.load(object)
    return dct


# вьюшки
@movies_ns.route('/')
class MoviePage(Resource):
    def get(self):
        res = serializ(movie_schema, Movie.query.all())

        # запрос по режиссеру
        director_id = int(request.args.get('director_id'))
        if director_id != None:
            director = serializ(director_schema, Director.query.get(director_id))
            movie = serializ(movie_schema, Movie.query.all())

            res = []
            for i in movie:
                if i['id'] == director['id']:
                    res.append(i)


        # запрос по жанру
        genre_id = int(request.args.get('genre_id'))
        if genre_id != None:
            genre = serializ(genre_schema, Genre.query.get(genre_id))
            movie = serializ(movie_schema, Movie.query.all())
            res = []
            for i in movie:
                if i['id'] == genre['id']:
                    res.append(i)
        return res, 200


#tlbybxyfz cthbfkbpfwbz
@movies_ns.route('/<int:mid>')
class MoviePage(Resource):
    def get(self, mid):
        red = serializ(movie_schema, Movie.query.get(mid))
        return res, 200


if __name__ == '__main__':
    app.run(debug=True)
