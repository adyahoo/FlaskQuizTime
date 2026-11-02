import os
import numpy as np
import tensorflow as tf
from flask import render_template, request, redirect, url_for, flash
from app import app, detector
from app.services import quiz_attempt_service, user_service, question_service, option_service, detected_object_service
from app.utils.utils import allowed_file, COCO_CLASSES
from werkzeug.utils import secure_filename
from PIL import Image, ImageDraw

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    user = user_service.get_user_by_username(username=request.form['username'])

    if not user:
        user = user_service.create_user(username=request.form['username'])

    return redirect(url_for('quiz', user=user.id))

@app.route('/quiz')
def quiz():
    user_id = request.args.get('user')

    questions = question_service.get_all_questions_with_options()
    high_scores = quiz_attempt_service.get_high_score(user_id=user_id)

    return render_template('quiz.html', questions=questions, high_scores=high_scores, user_id=user_id)

@app.route('/submit_quiz/<int:user_id>', methods=['POST'])
def submit_quiz(user_id):
    score = 0
    form = request.form

    for name, value in form.items():
        question_id = int(name.split('_')[1])
        option_id = int(value)

        question = question_service.get_question_by_id(question_id=question_id)
        is_correct = option_service.check_answer(option_id=option_id)
        score += question.point if is_correct else 0

    quiz_attempt_service.add_quiz_attempt(user_id=user_id, score=score)

    return redirect(url_for('result', user_id=user_id))

@app.route('/result')
def result():
    user_id = request.args.get('user_id')

    high_scores = quiz_attempt_service.get_high_score(user_id=user_id)
    latest_score = quiz_attempt_service.get_latest_attempt(user_id=user_id).score

    return render_template('result.html', user_id=user_id, high_scores=high_scores, latest_score=latest_score)

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        file = request.files['image']

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            input_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(input_filepath)
            
            # Define output filename for the processed image
            output_filename = f"detected_{filename}"
            output_filepath = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)

            # 2. Open image with Pillow and convert to numpy array
            img = Image.open(input_filepath).convert("RGB")
            img_np = np.array(img)
            
            # 3. Convert array to TensorFlow tensor and add batch dimension
            input_tensor = tf.convert_to_tensor(img_np)[tf.newaxis, ...]
            
            # 4. Run the model inference
            result = detector(input_tensor)

            boxes = result["detection_boxes"][0].numpy()
            classes = result["detection_classes"][0].numpy()
            scores = result["detection_scores"][0].numpy()
            
            # 5. Draw bounding boxes on the image
            draw = ImageDraw.Draw(img)
            im_width, im_height = img.size
            detected = {}

            if len(scores) > 0:
                best_idx = np.argmax(scores)
                best_score = scores[best_idx]

                if best_score > 0.5:
                    ymin, xmin, ymax, xmax = boxes[best_idx]
                    left, right = xmin * im_width, xmax * im_width
                    top, bottom = ymin * im_height, ymax * im_height
                    
                    # Draw a red rectangle
                    draw.rectangle([(left, top), (right, bottom)], outline="red", width=3)

                    class_id = int(classes[best_idx])
                    class_name = COCO_CLASSES.get(class_id, f"Unknown Object ({class_id})")

                    detected = {
                        "name": class_name,
                        "percentage_probability": float(scores[best_idx] * 100),
                        "box_points": [int(left), int(top), int(right), int(bottom)]
                    }
            
            # Save the modified image
            img.save(output_filepath)

            detected_obj = {
                "filename": filename,
                "label": detected['name'],
                "score": detected['percentage_probability']
            }

            saved_detection = detected_object_service.save_detection(detected_obj)

            return redirect(url_for(
                'predict_result', 
                file_id=saved_detection.id
            ))
    
    return render_template('predict.html')

@app.route('/predict_result')
def predict_result():
    id = request.args.get('file_id')

    res = detected_object_service.get_detection_by_id(id)

    return render_template('predict_result.html', result=res)