'''项目初始化'''
import os,sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager



# 创建flask类的实例，flask的当前实例对象就是app，后面各个方法都调用这个实例，可以规定模板，路径等
app = Flask(__name__)


WIN = sys.platform.startswith('win')
if WIN:
    prefix = 'sqlite:///'  # 如果是windows系统，三个斜杠
else:
    prefix = 'sqlite:////'  # Mac，Linux，四个斜杠

# 配置
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path),os.getenv('DATABASE_FILE','data.db'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY','dev')


db = SQLAlchemy(app) # 通过SQLAlchemy链接数据库，对数据库进行操作

# Flask-login 初始化操作
login_manager = LoginManager(app)   # 实例化扩展类,让app和flask_login协同工作
# 登录视图的名称
login_manager.login_view = 'login'
# 自定义登录信息
login_manager.login_message = '没有登录'


@login_manager.user_loader
def load_user(user_id):   # 创建用户   从会话中存储的ID加载用户对象，加载回调函数，接受用户ID作为参数
    from watchlist.models import User
    user = User.query.get(int(user_id))
    return user


@app.context_processor # 模板上下文处理函数
def inject_user():
    from watchlist.models import User
    user = User.query.first()
    return dict(user=user)


from watchlist import views,error,commands






