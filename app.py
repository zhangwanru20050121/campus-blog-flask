from flask import Flask, render_template, request, redirect, flash, abort, url_for, jsonify
from forms import LoginForm, RegisterForm, ArticleEditForm
import json
from pathlib import Path
from datetime import datetime
from uuid import uuid4

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret'

from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)
bootstrap_cdns = app.extensions['bootstrap']['cdns']
bootstrap_cdns['bootstrap'] = bootstrap_cdns['local']
bootstrap_cdns['jquery'] = bootstrap_cdns['local']

base_dir = Path(__file__).resolve().parent
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(base_dir / 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['AVATAR_UPLOAD_FOLDER'] = base_dir / 'static' / 'uploads' / 'avatars'
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
app.config['AVATAR_UPLOAD_FOLDER'].mkdir(parents=True, exist_ok=True)
ALLOWED_AVATAR_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
login_manager = LoginManager(app)
login_manager.login_view = 'login_view'
login_manager.login_message = '请先登录后再进行操作'
login_manager.login_message_category = 'warning'

from flask_ckeditor import CKEditor
ckeditor = CKEditor(app)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    age = db.Column(db.Integer)
    phone = db.Column(db.String(11), unique=True)
    intro = db.Column(db.Text)
    avatar = db.Column(db.String(255), default='default-avatar.svg')
    articles = db.relationship('Article', backref='author', foreign_keys='Article.author_id', uselist=True, cascade='all, delete-orphan')

class Article(db.Model):
    __tablename__ = 'articles'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

class ArticleLike(db.Model):
    __tablename__ = 'article_likes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_id = db.Column(db.Integer, db.ForeignKey('articles.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    __table_args__ = (db.UniqueConstraint('article_id', 'user_id', name='unique_article_user'),)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Article': Article, 'ArticleLike': ArticleLike}

@app.cli.command('init-db')
def init_db():
    db.drop_all()
    db.create_all()

@app.before_request
def ensure_new_columns():
    """兼容旧 data.db：首次运行时自动补充头像和文章时间字段，不清空原有数据。"""
    if getattr(app, '_columns_checked', False):
        return
    try:
        with db.engine.connect() as conn:
            user_cols = [row[1] for row in conn.exec_driver_sql('PRAGMA table_info(users)').fetchall()]
            article_cols = [row[1] for row in conn.exec_driver_sql('PRAGMA table_info(articles)').fetchall()]
            if user_cols and 'avatar' not in user_cols:
                conn.exec_driver_sql("ALTER TABLE users ADD COLUMN avatar VARCHAR(255) DEFAULT 'default-avatar.svg'")
            if article_cols and 'created_at' not in article_cols:
                conn.exec_driver_sql('ALTER TABLE articles ADD COLUMN created_at DATETIME')
                conn.exec_driver_sql("UPDATE articles SET created_at = datetime('now') WHERE created_at IS NULL")
            if article_cols and 'updated_at' not in article_cols:
                conn.exec_driver_sql('ALTER TABLE articles ADD COLUMN updated_at DATETIME')
                conn.exec_driver_sql("UPDATE articles SET updated_at = created_at WHERE updated_at IS NULL")
            conn.commit()
    except Exception:
        pass
    app._columns_checked = True

def avatar_url(user):
    filename = user.avatar or 'default-avatar.svg'
    return url_for('static', filename='uploads/avatars/' + filename)

@app.context_processor
def inject_helpers():
    return {'avatar_url': avatar_url}

def get_like_count(article_id):
    return ArticleLike.query.filter_by(article_id=article_id).count()

def is_liked_by_user(article_id, user_id):
    if not user_id:
        return False
    return ArticleLike.query.filter_by(article_id=article_id, user_id=user_id).first() is not None

def allowed_avatar(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_AVATAR_EXTENSIONS

def save_avatar(file_storage):
    if not file_storage or not file_storage.filename:
        return None
    if not allowed_avatar(file_storage.filename):
        flash('头像仅支持 png、jpg、jpeg、gif、webp 格式', 'warning')
        return None
    ext = file_storage.filename.rsplit('.', 1)[1].lower()
    filename = f'{uuid4().hex}.{ext}'
    file_storage.save(app.config['AVATAR_UPLOAD_FOLDER'] / filename)
    return filename

@app.route('/')
def index_view():
    articles = Article.query.order_by(Article.created_at.desc(), Article.id.desc()).paginate(per_page=6)
    user_id = current_user.id if current_user.is_authenticated else None
    return render_template('index.html', username=current_user.username if current_user.is_authenticated else None, article_pagination=articles, get_like_count=get_like_count, is_liked_by_user=is_liked_by_user, current_user_id=user_id)

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username, password = form.username.data, form.password.data
            user = User.query.filter_by(username=username).first()
            if user and user.password == password:
                login_user(user)
                flash('登录成功，欢迎回来！', 'success')
                return redirect('/')
            flash('错误的用户名或密码', 'danger')
        else:
            flash('验证不通过: ' + json.dumps(form.errors, ensure_ascii=False), 'warning')
    return render_template('login.html', form=form, username=current_user.username if current_user.is_authenticated else None)

@app.route('/logout')
@login_required
def logout_view():
    logout_user()
    flash('已退出登录', 'info')
    return redirect('/')

@app.route('/register', methods=['GET', 'POST'])
def register_view():
    form = RegisterForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            user = User.query.filter_by(username=username).first()
            if user:
                flash('用户名已存在', 'danger')
            else:
                new_user = User(username=username, password=form.password.data, age=form.age.data, phone=form.phone.data, intro=form.intro.data)
                avatar = save_avatar(request.files.get('avatar'))
                if avatar:
                    new_user.avatar = avatar
                db.session.add(new_user)
                db.session.commit()
                flash('成功注册，请登录', 'success')
                return redirect('/login')
        else:
            flash('验证不通过: ' + json.dumps(form.errors, ensure_ascii=False), 'warning')
    return render_template('register.html', form=form, username=current_user.username if current_user.is_authenticated else None)

@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile_view():
    if request.method == 'POST':
        avatar = save_avatar(request.files.get('avatar'))
        if avatar:
            current_user.avatar = avatar
            db.session.commit()
            flash('头像更新成功', 'success')
        return redirect('/profile')
    return render_template('profile.html', username=current_user.username, user=current_user)

@app.route('/article/list')
@login_required
def article_list_view():
    article_pagination = Article.query.filter_by(author_id=current_user.id).order_by(Article.created_at.desc(), Article.id.desc()).paginate(per_page=10)
    return render_template('article_list.html', username=current_user.username, article_pagination=article_pagination)

@app.route('/article/add', methods=['GET', 'POST'])
@login_required
def article_add_view():
    form = ArticleEditForm()
    if request.method == 'POST' and form.validate_on_submit():
        new_article = Article(title=form.title.data or '', content=form.content.data or '', author_id=current_user.id, created_at=datetime.now(), updated_at=datetime.now())
        db.session.add(new_article)
        db.session.commit()
        flash('文章创建成功', 'success')
        return redirect('/article/list')
    return render_template('article_edit.html', username=current_user.username, form=form, page_title='发布文章')

@app.route('/article/edit', methods=['GET', 'POST'])
@login_required
def article_edit_view():
    article_id = request.args.get('id') or -1
    article = Article.query.get(article_id)
    if not article or article.author_id != current_user.id:
        flash('文章不存在或无权编辑', 'danger')
        return redirect('/article/list')
    form = ArticleEditForm()
    if request.method == 'POST' and form.validate_on_submit():
        article.title = form.title.data or ''
        article.content = form.content.data or ''
        article.updated_at = datetime.now()
        db.session.commit()
        flash('文章保存成功', 'success')
        return redirect('/article/list')
    form.title.data = article.title
    form.content.data = article.content
    return render_template('article_edit.html', username=current_user.username, form=form, page_title='编辑文章')

@app.route('/article/delete')
@login_required
def article_delete_view():
    article_id = request.args.get('id') or -1
    article = Article.query.get(article_id)
    if not article or article.author_id != current_user.id:
        flash('文章不存在或无权删除', 'danger')
        return redirect('/article/list')
    db.session.delete(article)
    db.session.commit()
    flash('文章删除成功', 'success')
    return redirect('/article/list')

@app.route('/article/view', methods=['GET', 'POST'])
def article_view_view():
    article_id = request.args.get('id') or -1
    article = Article.query.get(article_id)
    if not article:
        flash('文章不存在或无权查看', 'danger')
        abort(404)
    user_id = current_user.id if current_user.is_authenticated else None
    return render_template('article_view.html', username=current_user.username if current_user.is_authenticated else None, article=article, like_count=get_like_count(article_id), is_liked=is_liked_by_user(article_id, user_id), current_user_id=user_id)

@app.route('/article/like/ajax', methods=['POST'])
@login_required
def article_like_ajax_view():
    data = request.get_json()
    if not data:
        return jsonify({'success': False, 'message': '无效的请求'}), 400
    article_id = data.get('article_id') or -1
    article = Article.query.get(article_id)
    if not article:
        return jsonify({'success': False, 'message': '文章不存在'}), 404
    existing_like = ArticleLike.query.filter_by(article_id=article_id, user_id=current_user.id).first()
    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        return jsonify({'success': True, 'liked': False, 'count': get_like_count(article_id)})
    new_like = ArticleLike(article_id=article_id, user_id=current_user.id)
    db.session.add(new_like)
    db.session.commit()
    return jsonify({'success': True, 'liked': True, 'count': get_like_count(article_id)})

if __name__ == '__main__':
    app.run(debug=True)
