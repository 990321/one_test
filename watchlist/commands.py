import click
from watchlist import app,db
from watchlist.models import User,Movie


# 自定义initdb
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
    name = "Warm"
    movies = [
        {'title':'三生三世十里桃花','year':'2020'},
        {'title':'超时空同居','year':'2018'},
        {'title':'枕上书','year':'2016'},
        {'title':'叶问4','year':'2020'},
        {'title':'无双','year':'2016'},
        {'title':'反贪风暴4','year':'2020'},
        {'title':'追龙','year':'2020'},
        {'title':'敢死队4','year':'2017'},
        {'title':'极限特工','year':'2018'},
        {'title':'生化危机：终章','year':'2019'}
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'],year=m['year'])
        db.session.add(movie)
    db.session.commit()
    click.echo('数据导入完成')

# 生成admin账号的函数
@app.cli.command()
@click.option('--username',prompt=True,help="用来登录的用户名")
@click.option('--password',prompt=True,hide_input=True,confirmation_prompt=True,help="用来登录的密码")
def admin(username,password):
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('更新用户')
        user.username = username
        user.set_password(password)
    else:
        click.echo('创建用户')
        user = User(username=username,name="Warm")
        user.set_password(password)
        db.session.add(user)
    
    db.session.commit()
    click.echo('创建管理员账号完成')
