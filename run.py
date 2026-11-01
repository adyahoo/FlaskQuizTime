from app import app, db
from app.models import User, Question, QuizAttempt
from app.utils.utils import *

if __name__ == "__main__":
    with app.app_context():
        # create database instance if not exist
        db.create_all()

        # import pre-built user, question, attempts
        dir = 'app/instance/mysql_schema/'
        import_csv_to_sqlite(dir + 'users.csv', user_mapper)
        import_csv_to_sqlite(dir + 'questions.csv', question_mapper)
        import_csv_to_sqlite(dir + 'quiz_attempts.csv', quiz_attempt_mapper)

    app.run(debug=True)