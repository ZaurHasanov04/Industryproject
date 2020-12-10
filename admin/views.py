from app import app
from app import db
from app.models import Icon, About, Project, Area, Servis, User, Contact, Logo
from flask import render_template,redirect,request,url_for, flash, abort
import os
from werkzeug.utils import secure_filename
from flask_login import login_user,  login_required, current_user


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['UPLOAD_PATH_POST'] = 'static/uploads'

@app.route('/adminpanel')
@login_required
def adminIndex():
    if User.query.get(1) == current_user:
        return render_template('/admin/index.html',title='Dashboard')
    else:abort(403)


#the start of users
@app.route('/users')
@login_required
def users():
    if User.query.get(1) == current_user:
        alldata=User.query.all()
        return render_template('/admin/users.html', allusers=alldata)
    else: abort(403)
#the end of users

#The start of functionality of Icon 

@app.route('/icons')
@login_required
def icons():
    if User.query.get(1) == current_user:
        alldata=Icon.query.all()
        return render_template('/admin/icons.html', allicon=alldata)
    else:
        abort(403)

@app.route('/icons/add', methods=['POST'])
@login_required
def addicons():
    if User.query.get(1) == current_user:
        if request.method == 'POST':
            title=request.form['icontitle']
            text=request.form['icontext']
            mydata=Icon(title, text)
            db.session.add(mydata)
            db.session.commit()
            return redirect(url_for('icons'))
    else:
        abort(403)


@app.route('/icons/update', methods=['GET', 'POST'])
@login_required
def updateicons():
    if User.query.get(1) == current_user:
        if request.method == 'POST':
            mydata=Icon.query.get(request.form.get('id'))
            mydata.title=request.form['icontitle']
            mydata.text=request.form['icontext']
            db.session.commit()
            return redirect(url_for('icons'))
    else:
        abort(403)

@app.route('/icon/delete/<id>/', methods=['GET', 'POST'])
@login_required
def deleteicons(id):
    if User.query.get(1) == current_user:
        mydata=Icon.query.get(id)
        db.session.delete(mydata)
        db.session.commit()
        return redirect(url_for('icons'))
    else:
        abort(403)

#The end of functionality of Icon 


#The start of functionality of about

@app.route('/about')
@login_required
def about():
    if User.query.get(1) == current_user:
        alldata= About.query.all()
        return render_template('admin/about.html', allabout=alldata)
    else:
        abort(403)    

@app.route('/about/add', methods=['GET', 'POST'])
@login_required
def addabout():
    if User.query.get(1) == current_user:
        if request.method == 'POST':
            title=request.form['abouttitle']
            text=request.form['abouttext']
            myabout=About(title, text)
            db.session.add(myabout)
            db.session.commit()
            return redirect(url_for('about'))
    else:
        abort(403)

@app.route('/about/update', methods=['GET', 'POST'])
@login_required
def updatedabout():
    if User.query.get(1) == current_user:
        if request.method == 'POST':
            myabout=About.query.get(request.form.get('id'))
            myabout.title=request.form['abouttitle']
            myabout.text=request.form['abouttext']
            db.session.commit()
            return redirect(url_for('about'))
    else:
        abort(403)

@app.route('/about/delete/<id>/', methods=['GET', 'POST'])
@login_required
def deleteabout(id):
    if User.query.get(1) == current_user:
        mydata=About.query.get(id)
        db.session.delete(mydata)
        db.session.commit()
        return redirect(url_for('about'))
    else:
        abort(403)

# The end of functionality  of about

# The start of functionality of project

@app.route('/projects')
@login_required
def project():
    if User.query.get(1) == current_user:
        prodata=Project.query.all()
        return render_template('/admin/projects.html', alldata=prodata)
    else:
        abort(403)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/projects/add', methods=['POST'])
@login_required
def addproject():
    if User.query.get(1) == current_user:
        if request.method == 'POST':
            title=request.form['title']
            category=request.form['category']
            text=request.form['text']
            file=request.files['file']

            if 'file' not in request.files:
                flash('No file part')
                return redirect(url_for('projectsingle'))
            if file.filename == '':
                flash('No selected file')
                return redirect(url_for('project_single'))
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join('static', app.config['UPLOAD_FOLDER'], filename))
                photo= os.path.join(app.config['UPLOAD_FOLDER'], filename)
            else:
                flash('Fayl secilmedi')
                return redirect(url_for('projectsingle'))

            mydata=Project(title, category, text, photo)
            db.session.add(mydata)
            db.session.commit()
            return redirect(url_for('project'))
    else: 
        abort(403)        

@app.route('/projects/update', methods=['POST'])
@login_required
def updateproject():
    if User.query.get(1) == current_user:
        myproject=Project.query.get(request.form.get('id'))
        myproject.title=request.form['title']
        myproject.category=request.form['category']
        myproject.text=request.form['text']

        file=request.files['file']

        if file.filename != '':
            if allowed_file(file.filename):
                os.remove(os.path.join('static', myproject.photoURL))
                filename=secure_filename(file.filename)
                file.save(os.path.join('static', app.config['UPLOAD_FOLDER'], filename))
                myproject.photoURL=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            else:
                flash('Bu fayl formatini desteklemir')
                return redirect(url_for('updateproject'))
        
        db.session.commit()
        return redirect(url_for('project'))
    else:
        abort(403)    


@app.route('/projects/delete/<id>', methods=['GET', 'POST'])
@login_required
def deleteproject(id):
    if User.query.get(1) == current_user:
        myproject=Project.query.get(id)
        db.session.delete(myproject)
        db.session.commit()
        return redirect(url_for('project'))
    else:
        abort(403)

# The end of functionailty of project

#the start of functionality of area

@app.route('/area')
@login_required
def area():
    if User.query.get(1) == current_user:
        alldata=Area.query.all()
        return render_template('admin/area.html', allarea=alldata)
    else:
        abort(403)

@app.route('/area/add', methods=['POST'])
@login_required
def addarea():
    if User.query.get(1) == current_user:
        if request.method == 'POST':
            title=request.form['title']
            text=request.form['text']
            mydata=Area(title, text)
            db.session.add(mydata)
            db.session.commit()
            return redirect(url_for('area'))
    else:
        abort(403)

@app.route('/area/update', methods=['GET', 'POST'])
@login_required
def updatearea():
    if User.query.get(1) == current_user:
        if request.method == 'POST':
            mydata=Area.query.get(request.form.get('id'))
            mydata.title=request.form['title']
            mydata.text=request.form['text']
            db.session.commit()
            return redirect(url_for('area'))
    else:
        abort(403)

@app.route('/areas/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def deletearea(id):
    if User.query.get(1) == current_user:
        mydata=Area.query.get(id)
        db.session.delete(mydata)
        db.session.commit()
        return redirect(url_for('area'))
    else: abort(403)
#the end of functionality of area

#the start of functionality of servis

@app.route('/servis')
@login_required
def servis():
    if User.query.get(1) == current_user:
        alldata=Servis.query.all()
        return render_template('admin/servis.html', myservis=alldata)
    else:
        abort(403)



#the end of functionality of servis

#the start of functionality of servis

@app.route('/contact')
@login_required
def contact():
    if User.query.get(1) == current_user:
        alldata=Contact.query.all()
        return render_template('admin/contact.html', contact=alldata)
    else: abort(403)



#the end of functionality of servis

@app.route('/logo')
@login_required
def logo():
    if User.query.get(1) == current_user:
        alldata=Logo.query.all()
        return render_template('/admin/logo.html', alllogo=alldata)
    else:
        abort(403)

@app.route('/logo/add', methods=['POST'])
@login_required
def addlogo():
    if User.query.get(1) == current_user:
        if request.method == 'POST':
            
            file=request.files['file']

            if 'file' not in request.files:
                flash('No file part')
                return redirect(url_for('addlogo'))
            if file.filename == '':
                flash('No selected file')
                return redirect(url_for('addlogo'))
            if allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_PATH_POST'] , filename))
                photo= os.path.join(app.config['UPLOAD_PATH_POST'], filename)
            else:
                flash('Fayl secilmedi')
                return redirect(url_for('logo'))

            mydata=Logo(photo)
            db.session.add(mydata)
            db.session.commit()
            return redirect(url_for('logo'))
    else: 
        abort(403)        


@app.route('/logo/update', methods=['GET', 'POST'])
@login_required
def updatelogo():
    if User.query.get(1) == current_user:
        if request.method == 'POST':
            myproject=Logo.query.get(request.form.get('id'))

            file=request.files['file']

            if file.filename != '':
                if allowed_file(file.filename):
                    os.remove(os.path.join('static', myproject.photoURL))
                    filename=secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_PATH_POST'], filename))
                    myproject.photoURL=os.path.join(app.config['UPLOAD_PATH_POST'], filename)
                else:
                    flash('Bu fayl formatini desteklemir')
                    return redirect(url_for('updatelogo'))
            
            db.session.commit()
            return redirect(url_for('logo'))
    else:
        abort(403)   

@app.route('/logo/delete/<id>/', methods=['GET', 'POST'])
@login_required
def deletelogo(id):
    if User.query.get(1) == current_user:
        mydata=Logo.query.get(id)
        db.session.delete(mydata)
        db.session.commit()
        return redirect(url_for('logo'))
    else:
        abort(403)






        
