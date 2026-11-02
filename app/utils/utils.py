import csv
from app import app, db
from app.models import User, QuizAttempt, Question, Option

def user_mapper(row):
    existing = db.session.execute(
        db.select(User).filter_by(username=row['username'])
    ).scalar()

    if not existing:
        new_record = User(username=row['username'])
        db.session.add(new_record)

def question_mapper(row):
    existing = db.session.execute(
        db.select(Question).filter_by(id=row['id'])
    ).scalar()

    if not existing:
        new_record = Question(
            id=row['id'],
            question=row['question'],
            point=row['point'],
            created_at=row['created_at']
        )
        db.session.add(new_record)

def option_mapper(row):
    existing = db.session.execute(
        db.select(Option).filter_by(id=row['id'])
    ).scalar()

    if not existing:
        new_record = Option(
            id=row['id'],
            question_id=row['question_id'],
            option=row['option'],
            is_correct=True if row['is_correct']=='1' else False
        )
        db.session.add(new_record)

def quiz_attempt_mapper(row):
    existing = db.session.execute(
        db.select(QuizAttempt).filter_by(id=row['id'])
    ).scalar()

    if not existing:
        new_record = QuizAttempt(
            id=row['id'],
            user_id=row['user_id'],
            score=row['score'],
            attempted_at=row['attempted_at']
        )
        db.session.add(new_record)

def import_csv_to_sqlite(filename, mapper):
    with app.app_context():
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)

            for row in reader:
                mapper(row)

            db.session.commit()
            print(f"Data from {filename} successfully imported into SQLite.")

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Standard COCO 2017 dataset class mapping used by TF Hub MobileNet
COCO_CLASSES = {
    1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane',
    6: 'bus', 7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light',
    11: 'fire hydrant', 13: 'stop sign', 14: 'parking meter', 15: 'bench',
    16: 'bird', 17: 'cat', 18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow',
    22: 'elephant', 23: 'bear', 24: 'zebra', 25: 'giraffe', 27: 'backpack',
    28: 'umbrella', 31: 'handbag', 32: 'tie', 33: 'suitcase', 34: 'frisbee',
    35: 'skis', 36: 'snowboard', 37: 'sports ball', 38: 'kite', 39: 'baseball bat',
    40: 'baseball glove', 41: 'skateboard', 42: 'surfboard', 43: 'tennis racket',
    44: 'bottle', 46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',
    51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',
    56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',
    61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',
    67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',
    75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',
    80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',
    86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'
}