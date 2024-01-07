import os
import cv2
import face_recognition
import numpy as np
import config

camera = cv2.VideoCapture(1)
face_cascade = cv2.CascadeClassifier('static/resources/haarcascade_frontalface_default.xml')

def detect_faces(image_path, id_employees):
    if not os.path.exists('static/detected_faces'):
        os.makedirs('static/detected_faces')
        
    sql_person_name = "SELECT name FROM employees WHERE id_employees = %s"
    val_person_name = (id_employees,)
    
    config.db_cursor.execute(sql_person_name, val_person_name)
    person_name_result = config.db_cursor.fetchone()
    
    if person_name_result:
        person_name = person_name_result['name']
        person_dir = os.path.join('static', 'detected_faces', person_name)
        if not os.path.exists(person_dir):
            os.makedirs(person_dir)

        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)

        for i, (top, right, bottom, left) in enumerate(face_locations):
            face_image = image[top:bottom, left:right]
            face_path = os.path.join(person_dir, f"face_{i}.jpg")
            face_image = cv2.cvtColor(face_image, cv2.COLOR_RGB2BGR)
            cv2.imwrite(face_path, face_image)

            # Simpan path file ke dalam database
            sql = "INSERT INTO faces (id_employees, image_path) VALUES (%s, %s)"
            val = (id_employees, face_path)  # Menggunakan path file yang disimpan di server
            config.db_cursor.execute(sql, val)

        # Commit perubahan ke database
        config.db_connection.commit()

        return len(face_locations)
    else:
        return 0  # Return 0 if person name not found
    

def train_recognizer():
    face_encodings = []
    labels = []

    for root, dirs, files in os.walk('static/detected_faces'):
        for label, folder_name in enumerate(dirs):
            for filename in os.listdir(os.path.join(root, folder_name)):
                img_path = os.path.join(root, folder_name, filename)
                image = face_recognition.load_image_file(img_path)
                face_encoding = face_recognition.face_encodings(image)
                
                # Check if any face is detected in the image
                if len(face_encoding) > 0:
                    encoding = face_encoding[0]  # Take the first face encoding
                    face_encodings.append(encoding)
                    labels.append(label)
                else:
                    print(f"No face found in {img_path}")

    return face_encodings, labels



def detect_and_recognize_faces(image_path):
    unknown_image = face_recognition.load_image_file(image_path)
    unknown_encoding = face_recognition.face_encodings(unknown_image)

    if len(unknown_encoding) > 0:
        face_encodings, labels = train_recognizer()
        face_distances = face_recognition.face_distance(face_encodings, unknown_encoding[0])
        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)
            if face_distances[best_match_index] < 0.6:  # Menentukan threshold
                person_name = os.listdir('static/detected_faces')[labels[best_match_index]]
                return person_name
            else:
                return "Unknown"
        else:
            return "Unknown"
    else:
        return "Face not detected"
    

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            # Mendeteksi wajah dalam frame
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            # Gambar kotak di sekitar setiap wajah yang terdeteksi
            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')