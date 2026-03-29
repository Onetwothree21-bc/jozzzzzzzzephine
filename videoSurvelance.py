import face_recognition
import cv2
import numpy as np
import datetime
# import mic shit
from pydub import AudioSegment
from PIL import Image
import math
import os 
os.makedirs("temporaryPictures", exist_ok=True)

def initilize(video_capture,known_faces):
    ret, frame = video_capture.read()
    rgb_small_frame = convertImage(frame)
    newImageProcess = checkImage(rgb_small_frame,known_faces,'y')

    tempid = 0
    face_locations = face_recognition.face_locations(frame)
    for face_location in face_locations:
        tempid += 1
        # Print the location of each face in this image
        top, right, bottom, left = face_location

        # You can access the actual face itself like this:
        face_image = frame[top:bottom, left:right]
        pil_image = Image.fromarray(face_image)
        pil_image.save("temporaryPictures/"+str(tempid)+".jpg")
    
    return newImageProcess
    


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
    known_faces = (known_face_encodings,known_face_ids)
    
    # Initialize some variables
    face_locations = []
    current_face_encodings = []
    process_this_frame = True
    
    initialRet, initialFrame = video_capture.read()
    checkPeople = initilize(initialFrame, known_faces)
    peoples = [x for (x,y,z) in checkPeople]
    new_face_encodings = [z for (x,y,z) in checkPeople]

    if "Unknown" in peoples:
        # TODO:
        # Start microphone recording 
        startTime = datetime.datetime.now()
        idnum = len(checkPeople)
        talkingCounter = 0
        while talkingCounter < 2400:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Only process every other frame of video to save time
            if process_this_frame:
                rgb_small_frame = convertImage(frame)
                
                newImageProcess = checkImage(rgb_small_frame,known_faces)
                if len([unknown for unknown in newImageProcess[0]if unknown == None]) != idnum:
                    continue
                    #TODO:
                    #implement this
                

                #for face_location in face_locations:
                #    # Print the location of each face in this image
                #    top, right, bottom, left = face_location
#
                #    # You can access the actual face itself like this:
                #    face_image = frame[top:bottom, left:right]
                #    pil_image = Image.fromarray(face_image)
                #    pil_image.show()

                currentTalker = None
                timestamps = []
                
                personTalking = detectTalker(frame)
                
                if personTalking != currentTalker:
                    if personTalking == None:
                        if talkingCounter > 10:
                            timestamps[-1] = (timestamps[-1][0],0)
                        else:
                            timestamps[-1] = (timestamps[-1][0],currentTalker)
                    timestamps[-1] = (timestamps[-1][0],personTalking)
                    currentTalker  = personTalking
                    timestamps.append(startTime - datetime.datetime.now(),currentTalker)
                
                if personTalking == None:
                    talkingCounter += 1
                else:
                    talkingCounter = 0
            
            process_this_frame = not process_this_frame
                    

        #TODO:
        # close mic

        # take audio file
        audio = AudioSegment.from_mp3("audioFiles/testAudioFile.mp3")
        # cut it at time stamps
        #previousTime = 0 
        #audioSlices = []
        #for time,tempid in timestamps:
        #    audioSlices.append((audio[previousTime,time],tempid))
        #    previousTime = time
        #
        ## stich together for all id's
        #final_slices = []
        #for id in new_ids:
        #    final_slices.append(sum([x for (x,y) in audioSlices if y == id]))
        
        # Release handle to the webcam
        video_capture.release()
        cv2.destroyAllWindows()
        # return                
        return (audio, timestamps),len(new_face_encodings)

            # Display the results
        displayResultsOnWebCam()

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass

        
        return list(zip(face_ids,))
    else:
        # get all needed data for each id    (checkPeople) is the list of id's    
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

def checkImage(frame,known_faces, new = 'n'):
    known_face_encodings = known_faces[0]
    known_face_names = known_faces[1]
    potential_face_names = []

    # Find all the faces and face encodings in the current frame of video
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)
    
    tempid = 0
    mouths = []
    for face_encoding in face_encodings:
        tempid += 1
        # See if the face is a match for the known face(s)
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index] and face_distances[best_match_index] < 0.4:
            name = known_face_names[best_match_index]
   
        potential_face_names.append((name,tempid,face_encoding))
    return potential_face_names

def convertImage(frame):
     # Resize frame of video to 1/4 size for faster face recognition processing
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    # Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
    rgb_small_frame = small_frame[:, :, ::-1]
    return rgb_small_frame

def avg_y(points):
    return sum(p[1] for p in points) / len(points)

def detectTalker(frame):
    mouths = []
    allFaceLandmarks = face_recognition.face_landmarks(frame)
    for faceLandmarks in allFaceLandmarks:
        if not faceLandmarks["top_lip"] or not faceLandmarks["bottom_lip"]:
            mouths.append(0)
        else:
            top_lip = faceLandmarks["top_lip"]
            bottom_lip = faceLandmarks["bottom_lip"]

            # Inner lip points (these are more accurate for openness)
            top_inner = top_lip[6:12]
            bottom_inner = bottom_lip[0:6]
            mouth_open = abs(avg_y(bottom_inner) - avg_y(top_inner))
            mouths.append(mouth_open)

    max_value = max(mouths)
    talkerID = None

    if all(max_value - m > 1 for m in mouths if m != max_value):
        talkerID = mouths.index(max_value)+1
    return talkerID