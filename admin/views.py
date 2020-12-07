from app import app
from app import db
from app.models import Icon, About, Project, Area, Servis
from flask import render_template,redirect,request,url_for, flash
import os
from werkzeug.utils import secure_filename


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/adminpanel')
def adminIndex():
    return render_template('/admin/index.html',title='Dashboard')


#the start of users
@app.route('/users')
def users():
    return render_template('/admin/users.html')
#the end of users

#The start of functionality of Icon 

@app.route('/icons')
def icons():
    alldata=Icon.query.all()
    return render_template('/admin/icons.html', allicon=alldata)


@app.route('/icons/add', methods=['POST'])
def addicons():
    if request.method == 'POST':
        title=request.form['icontitle']
        text=request.form['icontext']
        mydata=Icon(title, text)
        db.session.add(mydata)
        db.session.commit()
        return redirect(url_for('icons'))


@app.route('/icons/update', methods=['GET', 'POST'])
def updateicons():
    if request.method == 'POST':
        mydata=Icon.query.get(request.form.get('id'))
        mydata.title=request.form['icontitle']
        mydata.text=request.form['icontext']
        db.session.commit()
        return redirect(url_for('icons'))

@app.route('/icon/delete/<id>/', methods=['GET', 'POST'])
def deleteicons(id):
    mydata=Icon.query.get(id)
    db.session.delete(mydata)
    db.session.commit()
    return redirect(url_for('icons'))

#The end of functionality of Icon 


#The start of functionality of about

@app.route('/about')
def about():
    alldata= About.query.all()
    return render_template('admin/about.html', allabout=alldata)

@app.route('/about/add', methods=['GET', 'POST'])
def addabout():
    if request.method == 'POST':
        title=request.form['abouttitle']
        text=request.form['abouttext']
        myabout=About(title, text)
        db.session.add(myabout)
        db.session.commit()
        return redirect(url_for('about'))

@app.route('/about/update', methods=['GET', 'POST'])
def updatedabout():
    if request.method == 'POST':
        myabout=About.query.get(request.form.get('id'))
        myabout.title=request.form['abouttitle']
        myabout.text=request.form['abouttext']
        db.session.commit()
        return redirect(url_for('about'))


@app.route('/about/delete/<id>/', methods=['GET', 'POST'])
def deleteabout(id):
    mydata=About.query.get(id)
    db.session.delete(mydata)
    db.session.commit()
    return redirect(url_for('about'))

# The end of functionality  of about

# The start of functionality of project

@app.route('/projects')
def project():
    prodata=Project.query.all()
    return render_template('/admin/projects.html', alldata=prodata)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/projects/add', methods=['POST'])
def addproject():
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
            file.save(os.path.join('static/admin', app.config['UPLOAD_FOLDER'], filename))
            photo= os.path.join(app.config['UPLOAD_FOLDER'], filename)
        else:
            flash('Fayl secilmedi')
            return redirect(url_for('projectsingle'))

        mydata=Project(title, category, text, photo)
        db.session.add(mydata)
        db.session.commit()
        return redirect(url_for('project'))

@app.route('/projects/update', methods=['POST'])
def updateproject():
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


@app.route('/projects/delete/<id>', methods=['GET', 'POST'])
def deleteproject(id):
    myproject=Project.query.get(id)
    db.session.delete(myproject)
    db.session.commit()
    return redirect(url_for('project'))

# The end of functionailty of project

#the start of functionality of area

@app.route('/area')
def area():
    alldata=Area.query.all()
    return render_template('admin/area.html', allarea=alldata)

@app.route('/area/add', methods=['POST'])
def addarea():
    if request.method == 'POST':
        title=request.form['title']
        text=request.form['text']
        mydata=Area(title, text)
        db.session.add(mydata)
        db.session.commit()
        return redirect(url_for('area'))

@app.route('/area/update', methods=['GET', 'POST'])
def updatearea():
    if request.method == 'POST':
        mydata=Area.query.get(request.form.get('id'))
        mydata.title=request.form['title']
        mydata.text=request.form['text']
        db.session.commit()
        return redirect(url_for('area'))

@app.route('/areas/delete/<int:id>', methods=['GET', 'POST'])
def deletearea(id):
    mydata=Area.query.get(id)
    db.session.delete(mydata)
    db.session.commit()
    return redirect(url_for('area'))
#the end of functionality of area

#the start of functionality of servis

@app.route('/servis')
def servis():
    alldata=Servis.query.all()
    return render_template('admin/servis.html', myservis=alldata)



#the end of functionality of servis

#the start of functionality of servis

@app.route('/contact')
def contact():
    return render_template('admin/contact.html')

#the end of functionality of servis







        
