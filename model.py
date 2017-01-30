from flask_sqlalchemy import SQLAlchemy
from werkzeug.exceptions import HTTPException
from flask import Response, request
from flask_admin.contrib.sqla import ModelView
from datetime import datetime


db = SQLAlchemy ()


class AuthException(HTTPException):
    def __init__(self, message):
        super().__init__(message, Response(
            'Need authentication to get access to the page', 401,
            {'WWW-Authenticate': 'Basic realm="Login Required"'}
        ))


class AuthView(ModelView):
    form_excluded_columns = ('date_datetime', )
    form_args = dict(
        date_str=dict(default=datetime.now().strftime('%d.%m.%Y'))
    )

    def check_auth(self, username, password):
        return username == 'admin' and password == 'admin'

    def is_accessible(self):
        auth = request.authorization
        if not auth or not self.check_auth(auth.username, auth.password):
            raise AuthException('Not authenticated')
        return True


class Post(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(160))
    post_text = db.Column(db.Text)
    image_url = db.Column(db.String(140))
    date_str = db.Column(db.String(140))

    """

    def set_date_datetime(self):
        print(datetime.now().strftime('%d.%m.%Y'), self.date_str)
        if datetime.now().strftime('%d.%m.%Y') != self.date_str and self.date_str and self.date_str is not None:
            day, month, year = findall(r'\d', self.date_str)
            self.date_datetime = datetime(year=year, month=month, day=day)
        else:
            self.date_datetime = datetime.now()
        print(self.date_datetime)


    def __repr__(self):
        return '{} {} {} {}'.format(self.id, self.title, self.post_text, self.date)"""
