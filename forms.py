from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional, Regexp
from flask_ckeditor import CKEditorField


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(message='请输入用户名'),
        Length(min=2, max=50, message='用户名长度应为2-50个字符')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='请输入密码'),
        Length(min=3, max=50, message='密码长度应为3-50个字符')
    ])
    submit = SubmitField('登录')


class RegisterForm(FlaskForm):
    username = StringField('用户名', validators=[
        DataRequired(message='请输入用户名'),
        Length(min=2, max=50, message='用户名长度应为2-50个字符')
    ])
    password = PasswordField('密码', validators=[
        DataRequired(message='请输入密码'),
        Length(min=3, max=50, message='密码长度应为3-50个字符')
    ])
    age = IntegerField('年龄', validators=[
        Optional(),
        NumberRange(min=1, max=120, message='年龄应在1-120之间')
    ])
    phone = StringField('手机号', validators=[
        Optional(),
        Regexp(r'^1\d{10}$', message='请输入11位手机号，例如：13800000000')
    ])
    intro = TextAreaField('个人简介', validators=[
        Optional(),
        Length(max=500, message='个人简介不能超过500个字符')
    ])
    submit = SubmitField('注册')


class ArticleEditForm(FlaskForm):
    title = StringField('文章标题', validators=[
        DataRequired(message='请输入文章标题'),
        Length(min=1, max=255, message='标题不能超过255个字符')
    ])
    content = CKEditorField('文章内容', validators=[
        DataRequired(message='请输入文章内容')
    ])
    submit = SubmitField('保存')
