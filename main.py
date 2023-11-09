 
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///visual_tutoring.db'
db = SQLAlchemy(app)

class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), unique=True, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return '<Lesson %r>' % self.title

class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.id'), nullable=False)
    question = db.Column(db.String(80), nullable=False)
    answer = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return '<Quiz %r>' % self.question

@app.route('/')
def index():
    lessons = Lesson.query.all()
    return render_template('index.html', lessons=lessons)

@app.route('/lesson/<int:lesson_id>')
def lesson(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    return render_template('lesson.html', lesson=lesson)

@app.route('/quiz/<int:lesson_id>')
def quiz(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    quizzes = Quiz.query.filter_by(lesson_id=lesson_id).all()
    return render_template('quiz.html', lesson=lesson, quizzes=quizzes)

@app.route('/results/<int:lesson_id>', methods=['POST'])
def results(lesson_id):
    lesson = Lesson.query.get_or_404(lesson_id)
    quizzes = Quiz.query.filter_by(lesson_id=lesson_id).all()
    correct_answers = 0
    for quiz in quizzes:
        if request.form.get(quiz.id) == quiz.answer:
            correct_answers += 1
    return render_template('results.html', lesson=lesson, quizzes=quizzes, correct_answers=correct_answers)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
