import os
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# 配置
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path,'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # 关闭对模型修改的监控

db = SQLAlchemy(app)

@app.route('/')
def index():
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
    return render_template('index.html',name=name,movies=movies)