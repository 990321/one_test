import click
from watchlist import app,db
from watchlist.models import User,Ariticles


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
    ariticles = [
        {'title':'离婚了','content':'为什么呢？','author':'Warm'},
        {'title':'孙杨禁赛','content':'8年？','author':'Warm1'},
        {'title':'枕上书','content':'真好看？','author':'Warm2'},
        {'title':'疫情持续多久？','content':'待定','author':'Warm3'},
        {'title':'什么时候开学？','content':'另行通知','author':'Warm4'},
    ]
    user = User(name=name)
    db.session.add(user)
    for a in ariticles:
        ariticles = Ariticles(title=a['title'],content=a['content'],author=a['author'])
        db.session.add(ariticles)
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
