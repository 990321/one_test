import os,sys,click
from flask import Flask,render_template,request,url_for,redirect,flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = 'Warm'

WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///' # 如果是windows系统，三个斜杠
else:
    prefix = 'sqlite:////' #Mac，Linux，四个斜杠

# 配置
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控
app.config['SECRET_KEY'] = 'develop'

db = SQLAlchemy(app)

# 创建数据库模型类
class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)  # 主键
    name = db.Column(db.String(20))
class Movie(db.Model):
    id = db.Column(db.Integer,primary_key=True)  # 主键
    title = db.Column(db.String(30))
    year = db.Column(db.String(4))

# 自定义initdb命令
@app.cli.command()
@click.option('--drop',is_flag=True,help='删除之后再创建')
def initdb(drop):
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('初始化数据库')

# 自定义命令forge，把数据写入数据库
@app.cli.command()
def forge():
    db.create_all()
    name = 'Warm'
    movies = [
        {'title':'三生三世十里桃花','year':'2018'},
        {'title':'反贪风暴4','year':'2019'},
        {'title':'无双','year':'2019'},
        {'title':'枕上书','year':'2020'},
        {'title':'釜山行','year':'2017'},
        {'title':'神话','year':'2016'},
        {'title':'叶问','year':'2015'},
        {'title':'少林寺','year':'2014'},
        {'title':'前任3','year':'2013'},
        {'title':'超时空同居','year':'2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('导入完成')

# 首页
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        # 获取表单的数据
        title = request.form.get('title')
        year = request.form.get('year')

        # 验证title，year不为空，并且title不大于60，year不大于4
        if not title or not year or len(title)>60 or len(year)>4:
            flash('输入错误')
            return redirect(url_for('index')) # 重定向回主页
    
        movie = Movie(title=title,year=year) # 创建记录
        db.session.add(movie) # 添加数据库会话
        db.session.commit()    # 提交数据库会话
        flash('数据创建成功')
        return redirect(url_for('index'))

    movies = Movie.query.all()
    return render_template('index.html',movies=movies)

# 编辑电影信息页面
@app.route('/movie/edit/<int:movie_id>',methods=['GET','POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if request.method == 'POST':
        # 获取表单的数据
        title = request.form['title']
        year = request.form['year']

        # 验证title，year不为空，并且title不大于60，year不大于4
        if not title or not year or len(title)>60 or len(year)>4:
            flash('输入错误')
            return redirect(url_for('edit'),movie_id=movie_id)

        movie.title = title
        movie.year = year
        db.session.commit()
        flash('电影信息已经更新')
        return redirect(url_for('index'))
    return render_template('edit.html',movie=movie)


# 删除信息
@app.route('/movie/delete/<int:movie_id>',methods=['GET','POST'])
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('删除数据成功')
    return redirect(url_for('index'))



@app.errorhandler(404) # 传入要处理的错误代码
def page_not_found(e):
    return render_template('404.html'),404


@app.context_processor # 模板上下文处理函数，可以全局使用，不需要重复操作类似代码
def inject_user():
    user = User.query.first()
    return dict(user=user)



