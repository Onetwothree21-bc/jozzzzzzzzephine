import face_recognition
import cv2
import numpy as np
import datetime
# import mic shit

def imageCheck():

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    # Create arrays of known face encodings and their names
    known_face_ids = [
        # pull from database
    ]
    known_face_encodings = [
        #pull from database
    ]
    known_faces = list(zip(known_face_encodings,known_face_ids))
    
    # Initialize some variables
    face_locations = []
    face_encodings = []
    process_this_frame = True

    if checkImage(video_capture.read()).any() == "Unknown":
        # TODO:
        # Start microphone recording 
        startTime = datetime.datetime.now()
        while True:
            face_names = []
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Only process every other frame of video to save time
            if process_this_frame:
                rgb_small_frame = convertImage(frame)
                face_names.append(checkImage(rgb_small_frame,known_faces))
                

            process_this_frame = not process_this_frame
            talkingCounter = 0
            currentTalker = None
            timestamps = []
            while talkingCounter < 6000000:
                personTalking = detectTalker()
                if personTalking == None:
                    talkingCounter += 1
                else:
                    talkingCounter = 0
                if personTalking != currentTalker:
                    currentTalker  = personTalking
                    timestamps += (startTime - datetime.datetime.now(),currentTalker)

            #TODO:
            # close mic
            # take audio file
            # cut it at time stamps 
            # stich together for all id's
            # return                

            # Display the results
            displayResultsOnWebCam()

            # Hit 'q' on the keyboard to quit!
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()
        return list(zip(face_names,))
    else:
        return

def displayResultsOnWebCam(face_locations, face_names,frame):
    for (top, right, bottom, left), name in zip(face_locations, face_names):
            # Scale back up face locations since the frame we detected in was scaled to 1/4 size
            top *= 4
            right *= 4
            bottom *= 4
            left *= 4

            # Draw a box around the face
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Draw a label with a name below the face
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    # Display the resulting image
    cv2.imshow('Video', frame)

def checkImage(frame,known_faces):
    known_face_encodings = known_faces(0)
    known_face_names = known_faces(1)
    potential_face_names = []

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for face_encoding in face_encodings:
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index] and best_match_index < 0.4:
            name = known_face_names[best_match_index]

        potential_face_names.append(name)
    return potential_face_names

def convertImage(frame):
     # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    return rgb_small_frame