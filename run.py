from flask import Flask, render_template, request, redirect, url_for
import flask_login

app = Flask(__name__)
app.secret_key = 'super secret string'

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

# Our mock database.
users = {'nick': {'password': 'test'}}


class User(flask_login.UserMixin): ...

@login_manager.user_loader
def user_loader(email):
    if email not in users:
        return
    
    user = User()
    user.id = email
    return user

# @login_manager.request_loader
# def request_loader(request):
#     email = request.form.get('email')
#     if email not in users:
#         return
    
#     user = User()
#     user.id = email
#     return user

@app.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        formDict = request.form.to_dict()
        email = formDict.get('email')

        if email in users:
            if users[email]['password'] == formDict.get('password'):
                user = User()
                user.id = email
                flask_login.login_user(user)
                # return redirect(url_for('protected_page_1'))
        
        if formDict.get('page'):
            return redirect(url_for('page'))
        elif formDict.get('protected_page_1'):
            return redirect(url_for('protected_page_1'))
        elif formDict.get('protected_page_2'):
            return redirect(url_for('protected_page_2'))
        elif formDict.get('logout'):
            return redirect(url_for('logout'))

    return render_template('login.html')

@app.route('/page', methods=['GET','POST'])
def page():
    if request.method == 'POST':
        formDict = request.form.to_dict()
        print('formDcit::', formDict)
        if formDict.get('page'):
            return redirect(url_for('page'))
        elif formDict.get('protected_page_1'):
            return redirect(url_for('protected_page_1'))
        elif formDict.get('protected_page_2'):
            return redirect(url_for('protected_page_2'))
        elif formDict.get('logout'):
            return redirect(url_for('logout'))
        elif formDict.get('login'):
            return redirect(url_for('login'))
    return render_template('page.html')
    


@app.route('/protected_page_1', methods = ['GET', 'POST'])
@flask_login.login_required
def protected_page_1():
    page_name = 'Protected page 1'
    other_protected_page = 'Protected page 2'
    if request.method == 'POST':
        formDict = request.form.to_dict()
        
        if formDict.get('page'):
            return redirect(url_for('page'))
        elif formDict.get('protected_page_1'):
            return redirect(url_for('protected_page_1'))
        elif formDict.get('protected_page_2'):
            return redirect(url_for('protected_page_2'))
        elif formDict.get('logout'):
            return redirect(url_for('logout'))

    return render_template('protected_page.html', flask_login = flask_login, 
        page_name = page_name, other_protected_page = other_protected_page)

@app.route('/protected_page_2', methods = ['GET', 'POST'])
@flask_login.login_required
def protected_page_2():
    page_name = 'Protected __page__ 2'
    other_protected_page = 'Protected page 1'
    if request.method == 'POST':
        formDict = request.form.to_dict()
        if formDict.get('page'):
            return redirect(url_for('page'))
        elif formDict.get('protected_page_1'):
            return redirect(url_for('protected_page_1'))
        elif formDict.get('protected_page_2'):
            return redirect(url_for('protected_page_2'))
        elif formDict.get('logout'):
            return redirect(url_for('logout'))


    return render_template('protected_page.html', flask_login = flask_login, 
        page_name = page_name, other_protected_page = other_protected_page)


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return redirect(url_for('login'))


if  __name__ == '__main__':
    app.run(debug = True)