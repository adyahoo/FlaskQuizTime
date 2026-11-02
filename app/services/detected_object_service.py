from app.models.detected_object import DetectedObject
from app import db

def get_detection_by_id(id):
   return db.session.execute(db.select(DetectedObject).filter_by(id=id)).scalar() 

def save_detection(detection):
    new_detection = DetectedObject(
        filename=detection['filename'],
        label=detection['label'],
        score=detection['score']
    )

    db.session.add(new_detection)
    db.session.commit()

    return new_detection

