import face_recognition
import cv2
import sounddevice as sd
from scipy.io.wavfile import write
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
    


def imageCheck(known_face_ids, known_face_encodings):

    # Get a reference to webcam #0 (the default one)
    video_capture = cv2.VideoCapture(0)

    # Create arrays of known face encodings and their names
    
    known_faces = (known_face_encodings,known_face_ids)
    
    # Initialize some variables
    face_locations = []
    current_face_encodings = []
    process_this_frame = True
    
    checkPeople = initilize(video_capture, known_faces)
    peoples = [x for (x,y,z) in checkPeople]
    new_face_encodings = [z for (x,y,z) in checkPeople if x == "Unknown"]

    if "Unknown" in peoples:
        # Start microphone recording
        fs = 44100  # sample rate
        recording = True
        audio_buffer = []

        def audio_callback(indata, frames, time, status):
            if recording:
                audio_buffer.append(indata.copy())

        stream = sd.InputStream(samplerate=fs, channels=1, callback=audio_callback)
        stream.start()

        startTime = datetime.datetime.now()
        idnum = len([x for (x,y,z) in checkPeople if x == "Unknown"])
        talkingCounter = 0
        currentTalker = 0
        timestamps = []
        timestamps.append((0,0))
        while talkingCounter < 2400:
            # Grab a single frame of video
            ret, frame = video_capture.read()

            # Only process every other frame of video to save time
            if process_this_frame:
                rgb_small_frame = convertImage(frame)
                
                newImageProcess = checkImage(rgb_small_frame,known_faces)
                if len([x for x in newImageProcess if x[0] == "Unknown"]) != idnum:
                    pass
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

                
                personTalking = detectTalker(frame)
                
                if personTalking != currentTalker:
                    if personTalking == 0 and timestamps:
                        if talkingCounter > 10:
                            timestamps[-1] = (timestamps[-1][0],0)
                        else:
                            timestamps[-1] = (timestamps[-1][0],currentTalker)
                    
                    currentTalker  = personTalking
                    timestamps.append((int((datetime.datetime.now() - startTime).total_seconds() * 1000), currentTalker))
                
                if personTalking == 0:
                    talkingCounter += 1
                else:
                    talkingCounter = 0
            
            process_this_frame = not process_this_frame
        timestamps[-1] = (timestamps[-1][0],-1)
                    

        # Stop microphone recording
        recording = False
        stream.stop()
        stream.close()

        # Combine audio chunks
        if len(audio_buffer) == 0:
            audio_data = np.array([])
        else:
            audio_data = np.concatenate(audio_buffer, axis=0).flatten()

        ## Save to file
        #audio_filename = "audioFiles/testAudioFile.wav"
        #write(audio_filename, fs, audio_data)
#
        ## take audio file
        #audio = AudioSegment.from_mp3("audioFiles/testAudioFile.mp3")
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
        return (audio_data, timestamps),len(peoples),peoples

            # Display the results
        displayResultsOnWebCam(face_locations, face_names,frame)

        # Hit 'q' on the keyboard to quit!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            pass

        
        return list(zip(face_ids,))
    else:
        # get all needed data for each id    (checkPeople) is the list of id's 
        old_face_encodings = [z for (x,y,z) in checkPeople if x != "Unknown"]   
        return None,len(old_face_encodings),old_face_encodings

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
        if len(known_face_encodings) != 0:
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index] and face_distances[best_match_index] < 0.4:
                name = str(known_face_names[best_match_index])
   
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
    allFaceLandmarks = face_recognition.face_landmarks(frame)

    # No faces detected
    if not allFaceLandmarks:
        return 0

    mouths = []
    for faceLandmarks in allFaceLandmarks:
        top_lip = faceLandmarks.get("top_lip")
        bottom_lip = faceLandmarks.get("bottom_lip")
        
        # If lips are missing, mouth openness is 0
        if not top_lip or not bottom_lip:
            mouths.append(0)
        else:
            # Inner lip points (more accurate for openness)
            top_inner = top_lip[6:12]
            bottom_inner = bottom_lip[0:6]
            mouth_open = abs(avg_y(bottom_inner) - avg_y(top_inner))
            mouths.append(mouth_open)

    # If no mouths calculated, return 0
    if not mouths:
        return 0

    max_value = max(mouths)

    # Check if max mouth is noticeably more open than others
    if all(max_value - m > 1 for m in mouths if m != max_value):
        return mouths.index(max_value) + 1

    return 0  # no clear talker