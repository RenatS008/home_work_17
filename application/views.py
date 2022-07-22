from flask import current_app as app, request
from flask_restx import Api, Resource, Namespace
from application.models import db
from application import models, schema

api: Api = app.config['api']

movie_ns: Namespace = api.namespace('movies')
director_ns: Namespace = api.namespace('directors')
genre_ns: Namespace = api.namespace('genres')

movie_schema = schema.MovieSchema()
movies_schema = schema.MovieSchema(many=True)

genre_schema = schema.GenreSchema()
genres_schema = schema.GenreSchema(many=True)

director_schema = schema.DirectorSchema()
directors_schema = schema.DirectorSchema(many=True)

'''====================================== MOVIE ======================================'''


@movie_ns.route('/')
class MoviesView(Resource):
    """возвращает список всех фильмов,
    разделенный по страницам"""

    def get(self):
        movies_data = db.session.query(models.Movie)

        args = request.args
        director_id = args.get('director_id')

        if director_id is not None:
            movies_data = movies_data.filter(models.Movie.director_id == director_id)

        genre_id = args.get('genre_id')
        if genre_id is not None:
            movies_data = movies_data.filter(models.Movie.genre_id == genre_id)

        movies = movies_data.all()

        return movies_schema.dump(movies), 200

    @movie_ns.response(201, description="Фильм добавлен")
    def post(self):
        """добавление фильма в бд"""

        movie = movie_schema.load(request.json)
        db.session.add(models.Movie(**movie))
        db.session.commit()
        return {"OK"}, 201


@movie_ns.route('/<int:movie_id>/')
class MovieView(Resource):

    @movie_ns.response(200, description="Возвращает фильм по его ID")
    @movie_ns.response(404, description="Фильм не найден")
    def get(self, movie_id):
        """возвращает подробную информацию о фильме."""
        movie = db.session.query(models.Movie).filter(models.Movie.id == movie_id).first()

        if movie is None:
            return {"ERROR"}, 404

        return movie_schema.dump(movie), 200

    @movie_ns.response(200, description="Фильм обновлен")
    @movie_ns.response(400, description="Неверный ID фильма")
    def put(self, movie_id):
        """обновление данных фильма"""

        update_data = db.session.query(models.Movie).filter(models.Movie.id == movie_id).update(request.json)

        if update_data != 1:
            return {"ERROR"}, 400
        db.session.commit()

        return {"OK"}, 200

    @movie_ns.response(200, description="Фильм удален")
    @movie_ns.response(400, description="Неверный ID фильма")
    def delete(self, movie_id):
        delete_data = db.session.query(models.Movie).filter(models.Movie.id == movie_id).delete()

        if delete_data != 1:
            return {"ERROR"}, 400

        db.session.commit()

        return {"OK"}, 200


'''====================================== DIRECTORS ======================================'''


@director_ns.route('/')
class DirectorsView(Resource):
    """возвращаем всех режиссеров"""

    def get(self):
        directors = db.session.query(models.Director).all()

        return directors_schema.dump(directors), 200

    @movie_ns.response(201, description="Режиссер добавлен")
    def post(self):
        """добавляем режиссера в бд"""

        director = director_schema.load(request.json)
        db.session.add(models.Director(**director))
        db.session.commit()

        return {"OK"}, 201


@director_ns.route('/<int:director_id>/')
class DirectorView(Resource):
    @director_ns.response(200, description="Возвращает режиссера по его ID")
    @director_ns.response(404, description="Режиссер не найден")
    def get(self, director_id):
        """возвращаем информацию о режиссере"""

        director = db.session.query(models.Director).filter(models.Director.id == director_id).first()

        if director_id is None:
            return {"ERROR"}, 404

        return director_schema.dump(director), 200

    @director_ns.response(200, description="Режиссер обновлен")
    @director_ns.response(400, description="Неверный ID режиссера")
    def put(self, director_id):
        """обноление данных режиссера"""

        update_data = db.session.query(models.Director).filter(models.Director.id == director_id).update(request.json)

        if update_data != 1:
            return {"ERROR"}, 400

        db.session.commit()

        return {"OK"}, 200

    @director_ns.response(200, description="Режиcсер удален")
    @director_ns.response(400, description="Неверный ID режиcсера")
    def delete(self, director_id):
        """удаление режиссера"""

        delete_data = db.session.query(models.Director).filter(models.Director.id == director_id).delete()

        if delete_data != 1:
            return {"ERROR"}, 400

        db.session.commit()

        return {"OK"}, 200


'''====================================== GENRES ======================================'''


@genre_ns.route('/')
class GenresView(Resource):
    """возвращает все жанры"""

    def get(self):
        genres = db.session.query(models.Genre).all()

        return genres_schema.dump(genres), 200

    @genre_ns.response(201, description="Жанр добавлен")
    def post(self):
        """добавляем жанр в бд"""

        genre = genre_schema.load(request.json)
        db.session.add(models.Genre(**genre))
        db.session.commit()

        return {"OK"}, 201


@genre_ns.route('/<int:genre_id>/')
class GenreView(Resource):
    @genre_ns.response(200, description="Возвращает фильм по жанру")
    @genre_ns.response(404, description="Жанр не найден")
    def get(self, genre_id):
        """возвращает информацию о жанре с перечислением списка фильмов по жанру"""

        genre = db.session.query(models.Genre).filter(models.Genre.id == genre_id).first()

        if genre_id is None:
            return {"ERROR"}, 404

        return genre_schema.dump(genre), 200

    @genre_ns.response(200, description="Жанр обновлен")
    @genre_ns.response(400, description="Неверный ID жанра")
    def put(self, genre_id):
        update_data = db.session.query(models.Genre).filter(models.Genre.id == genre_id).update(request.json)
        if update_data != 1:
            return {"ERROR"}, 400
        db.session.commit()
        return {"OK"}, 200

    @genre_ns.response(200, description="Жанр удален")
    @genre_ns.response(400, description="Неверный ID жанра")
    def delete(self, genre_id):
        """удаляем жанр"""

        delete_data = db.session.query(models.Genre).filter(models.Genre.id == genre_id).delete()

        if delete_data != 1:
            return {"ERROR"}, 400

        db.session.commit()

        return {"OK"}, 200
