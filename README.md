# Flask API Quickstart with JSON Web Tokens, SQLAlchemy and Pytest

This is a quick-start application that demonstrates how to create secured API applications using Flask and JWT. It is built with:

- [Python 3](https://www.python.org/)
- [Flask](http://flask.pocoo.org/)
- [PyJWT](https://pyjwt.readthedocs.io/en/latest/)
- [Flask-SQLAlchemy](http://flask-sqlalchemy.pocoo.org/2.1/)
- [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
- [Pytest](https://docs.pytest.org/)

I wrote an article about creating the quickstart: [Flask API Quickstart Application with JSON Web Tokens, SQLAlchemy and Pytest](https://stribny.name/blog/2018/10/flask-api-quickstart-application-with-json-web-tokens-sqlalchemy-and-pytest).

## Requirements

You will need Python 3 installed, together with [Pipenv](https://pipenv.readthedocs.io/en/latest/) to install dependencies.

The app uses a SQL database via SQLAlchemy. It was tested with PostgreSQL, but should work with other supported databases as well.

## Installation

1. Clone the repository
2. Install dependencies using `pipenv install`

## Configuration

All configuration can be found in `app/config.py` file.

Change at least:

- `SQLALCHEMY_DATABASE_URI` for the db connection
- `SECRET_KEY` to be unique to your application

## Run the application

1. Enter virtual environment using `pipenv shell`
2. Run database migrations using `flask db upgrade`
3. Run `python run.py`
4. Check to see if the application is running with `curl -XGET http://localhost:5000/ping`

### Create account

```
curl -i -H "Content-Type: application/json" -X POST -d '{"username":"user1", "password":"Password1", "email": "t@example.com"}' http://localhost:5000/api/v1/auth/signup
```

### Log in to get JWT token

```
curl -i -H "Content-Type: application/json" -X POST -d '{"username":"user1", "password":"Password1"}' http://localhost:5000/api/v1/auth/login
```

You should get a `token` that can be used for the following two endpoints:

### Access protected endpoint

Replace `XXXXX` with your token:

```
curl -i -H "Authorization: Bearer XXXXX" -H "Content-Type: application/json" -XGET http://localhost:5000/protected
```

### Logout to invalidate the token

Replace `XXXXX` with your token:

```
curl -i -H "Authorization: Bearer XXXXX" -H "Content-Type: application/json" -XPOST http://localhost:5000/api/v1/auth/logout
```

## Run the tests

1. Enter virtual environment using `pipenv shell`
2. Run the test suite with `pytest`

## Documentation

There is API specification written in OpenAPI Specification in `docs/api.yaml`

## License

Various parts of the quickstart were inspired by [Bucket List API](https://github.com/jokamjohn/bucket_api).

Author: [Petr Stříbný](http://stribny.name)

License: The MIT License (MIT)
