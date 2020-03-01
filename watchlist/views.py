'''视图，显示内容和实现功能'''
from watchlist import db,app
from flask import request,redirect,url_for,flash,render_template
from flask_login import login_user,logout_user,login_required,current_user
from watchlist.models import User,Ariticles

# current_user.is_authenticated：当登录以后可以满足login_required的条件
# 首页
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            return redirect(url_for('index'))
        # 获取表单的数据
        title = request.form.get('title')
        content = request.form.get('content')
        author = request.form.get('author')

        # 验证title，year不为空，并且title长度不大于60，year的长度不大于4
        if not title or not content or not author or len(title)>60:
            flash('输入错误')  # 错误提示
            return redirect(url_for('index'))  # 重定向回主页
        
        ariticles = Ariticles(title=title,content=content,author=author)  # 创建记录
        db.session.add(ariticles)  # 添加到数据库会话
        db.session.commit()   # 提交数据库会话
        flash('数据创建成功')
        return redirect(url_for('index'))

    ariticles = Ariticles.query.all()
    return render_template('index.html',ariticles=ariticles)
# 编辑电影信息页面
@app.route('/movie/edit/<int:ari_id>',methods=['GET','POST'])
@login_required 
def edit(ari_id):
    ariticles = Ariticles.query.get_or_404(ari_id)

    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']

        if not title or not content or not author or len(title)>60:
            flash('输入错误')
            return redirect(url_for('edit'),ari_id=ari_id)
        
        ariticles.title = title
        ariticles.content = content
        ariticles.author = author
        db.session.commit()
        flash('电影信息已经更新')
        return redirect(url_for('index'))
    return render_template('edit.html',ariticles=ariticles)
# 博文详情
@app.route('/details/<int:ari_id>',methods=['GET','POST'])
@login_required # 判断是否登录，进行权限验证，未登录无权限，登录以后有权限
def details(ari_id):
    ariticles = Ariticles.query.get_or_404(ari_id)
    return render_template('detail.html',ariticles=ariticles)

# 设置
@app.route('/settings',methods=['GET','POST'])
@login_required # 判断是否登录，进行权限验证，未登录无权限，登录以后有权限
def settings():
    if request.method == 'POST':
        name = request.form['name']

        if not name or len(name)>20:
            flash('输入错误')
            return redirect(url_for('settings'))
        
        current_user.name = name
        db.session.commit()
        flash('设置name成功')
        return redirect(url_for('index'))

    return render_template('settings.html')

# 删除信息
@app.route('/movie/delete/<int:ari_id>',methods=['POST'])
@login_required    
def delete(ari_id):
    ariticles = Ariticles.query.get_or_404(ari_id)
    db.session.delete(ariticles)
    db.session.commit()
    flash('删除数据成功')
    return redirect(url_for('index'))

# 用户登录 flask提供的login_user()函数
@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if not username or not password:
            flash('输入错误')
            return redirect(url_for('login'))
        user = User.query.first()
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登录用户，把用户设置到session中
            flash('登录成功')
            return redirect(url_for('index'))  # 登录成功返回首页
        flash('用户名或密码输入错误')
        return redirect(url_for('login'))
    return render_template('login.html')

# 用户登出
@app.route('/logout')
def logout():
    logout_user()
    flash('退出登录')
    return redirect(url_for('index'))