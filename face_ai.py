#prediction

import cv2
import numpy as np
import os


def get_names(folder='dataset'):
    return os.listdir(folder)

#function to detect face using OpenCV
def detect_face(img,cascade = 'cascades/lbpcascade_frontalface.xml'):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cascade)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5);
    if (len(faces) == 0):
        return None, None
    
    (x, y, w, h) = faces[0]
    return gray[y:y+w, x:x+h], faces[0]


#this function will read all persons' training images, detect face from each image
#and will return two lists of exactly same size, one list 
# of faces and another list of labels for each face
def prepare_training_data(data_folder_path='dataset'):
    dirs = os.listdir(data_folder_path)
    faces = []
    labels = []
    for label,dir_name in enumerate(dirs):
        subject_dir_path = data_folder_path + "/" + dir_name
        if os.path.isdir(subject_dir_path):
            subject_images_names = os.listdir(subject_dir_path)
            for image_name in subject_images_names:
                if image_name.startswith("."):
                    continue
                image_path = subject_dir_path + "/" + image_name
                image = cv2.imread(image_path)
                # cv2.imshow("Training on image...", image)
                cv2.waitKey(100)
                try:
                    face, rect = detect_face(image)
                    if face is not None:
                        faces.append(face)
                        labels.append(label)
                except Exception as e:
                    print(e)
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    return faces, labels

def train_face_ai(faces,labels):
    #create our LBPH face recognizer 
    face_recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_recognizer.train(faces, np.array(labels))
    return face_recognizer

def draw_rectangle(img, rect):
    (x, y, w, h) = rect
    cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    
def draw_text(img, text, x, y):
    cv2.putText(img, text, (x, y), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 255, 0), 2)

def predict(test_img,face_recognizer):
    img = test_img.copy()
    face, rect = detect_face(img)
    label= face_recognizer.predict(face)[0]
    print(label)
    label_text = subjects[label]
    draw_rectangle(img, rect)
    draw_text(img, label_text, rect[0], rect[1]-5)
    return img


if __name__ == "__main__":
    subjects = get_names()
    print("Preparing data...")
    faces, labels = prepare_training_data()
    print("Data prepared")
    #print total faces and labels
    print("Total faces: ", len(faces))
    print("Total labels: ", len(labels))
    face_recognizer = train_face_ai(faces, labels)
    print("Predicting images...")

    # #load test images
    # test_img1 = cv2.imread("dataset\\meraz_1700\\meraz_8.jpg")
    # test_img2 = cv2.imread("dataset\\shahbaz_548\\shahbaz_20.jpg")

    # #perform a prediction
    # predicted_img1 = predict(test_img1,face_recognizer)
    # predicted_img2 = predict(test_img2,face_recognizer)
    # print("Prediction complete")

    # #display both images
    # cv2.imshow(subjects[0], predicted_img1)
    # cv2.imshow(subjects[1], predicted_img2)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
