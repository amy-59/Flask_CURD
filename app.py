from flask import Flask,flash,redirect,url_for,request,render_template 
from models import db, StudentModel
app=Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#Creating table
@app.before_request
def create_table():
    db.create_all()

#Adding data
@app.route('/create', methods=["GET", "POST"])
def create():
    if request.method =="GET":
        return render_template('create.html')
    if request.method == "POST":
        hobby= request.form.getlist('hobbies')
        hobbies = ",".join(map(str,hobby))
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        gender = request.form['gender']
        hobbies = hobbies
        country =request.form['country']

        students = StudentModel(
            first_name=first_name,
            last_name=last_name,
            email= email,
            password=password,
            gender=gender,
            hobbies= hobbies,
            country=country)
        
        db.session.add(students)
        db.session.commit()
        return  redirect('/')
    
 # Edit Data   
@app.route('/<int:id>/edit', methods=["GET","POST"])
def update(id):
    student= StudentModel.query.filter_by(id=id).first()

    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()

            hobby= request.form.getlist('hobbies')
            hobbies = ",".join(map(str,hobby))
            first_name = request.form['first_name']
            last_name = request.form['last_name']
            email = request.form['email']
            password = request.form['password']
            gender = request.form['gender']
            hobbies = hobbies
            country =request.form['country']

            students = StudentModel(
            first_name=first_name,
            last_name=last_name,
            email= email,
            password=password,
            gender=gender,
            hobbies= hobbies,
            country=country)
        
        db.session.add(students)
        db.session.commit()
        return redirect('/')
        return f"Student with id ={id} does not exixt"
        
    return render_template("update.html",student=student)

#Delete Data
@app.route('/<int:id>/delete', methods=["GET","POST"])
def delete(id):
    students=StudentModel.query.filter_by(id=id).first()
    if request.method == "POST":
        if students:
            db.session.delete(students)
            db.session.commit()
            return redirect("/")
        abort(404)
    return render_template('delete.html')

#View All Data
@app.route('/', methods=["GET"])
def retrieve_list():
    students = StudentModel.query.all()
    return render_template('datalist.html', students = students)

#Run The App
app.run(debug=True)
