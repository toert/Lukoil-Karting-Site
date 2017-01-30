from flask import Flask, render_template, request
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from flask_admin import Admin
from model import db, Post, AuthView
from config import SQLALCHEMY_DATABASE_URI

app = Flask(__name__)
app.config.from_object('config')
app.config['SECRET_KEY'] = '1703'
db.init_app(app)
admin = Admin(app, name='PDB-Admin', template_mode='bootstrap3')

POSTS_IN_ONE_PAGE = 15


@app.route('/', methods=['GET'])
def index_page():
    return render_template('index.html')


@app.route('/news', methods=['GET'])
def ads_list():
    page = request.args.get('page')
    if not page or page is None:
        page = 1
    all_news = Post.query.order_by(desc(Post.id)).paginate(int(page), POSTS_IN_ONE_PAGE, False)
    return render_template('news.html', news=all_news)


@app.route('/partners', methods=['GET'])
def partners_page():
    return render_template('partners.html')


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    engine = create_engine(SQLALCHEMY_DATABASE_URI)
    # meta = MetaData(bind=engine, reflect=True)
    # base.metadata.create_all(engine)
    session_maker = sessionmaker(bind=engine)
    session = session_maker()
    admin.add_view(AuthView(Post, session))
    app.run()
