import videoSurvelance as vs
import database as db
import numpy as np
import speech_to_text as st
import extract_info as ei
import datetime
import pyttsx3 

def runSystem():

    conn, cursor = db.init_db(reset=True)
    encodings, ids = db.get_face_dataset(conn)

    audioShit, newNum, embeddings = vs.imageCheck(ids, encodings)
    
    if audioShit != None:
        audioText = st.main(audioShit[0], audioShit[1])
        dataInfo = ei.main(audioText)
        
        for i in range(0, newNum):
            embedding = embeddings[i]
            first_name = dataInfo[i][1]
            job = dataInfo[i][2]
            last_name = ""
            location = ""
            event = ""
            dateCurrent = datetime.datetime.now()

            db.insert_person(
                conn, cursor,
                embedding, first_name, last_name,
                job, location, event, dateCurrent
            )
    
    else:
        # Get info from database
        people = []
        for i in range(0, newNum):
            people.append(get_person_by_id(conn, embeddings[i]))
        
        # Print into Console logs
        for person in people:
            print_person_row(person)
        
        # Build message
        message = ""

        for person in people:
            if person is not None:
                message += f"{person['first_name']} {person['last_name']} - {person['course_or_job']}. "

        if message == "":
            message = "No known people detected"

        # send message
        send_audio_message(message)

    return "data given"


def send_audio_message(message):
    print("Speaking:", message)

    engine = pyttsx3.init()

    # presets
    engine.setProperty('rate', 170)   # speed
    engine.setProperty('volume', 1.0) # max volume

    try:
        engine.say(message)
        engine.runAndWait()
    except Exception as e:
        print("Audio error:", e)

def get_person_by_id(conn, person_id):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people WHERE id = ?", (person_id,))
    row = cursor.fetchone()  # fetch one record
    return row  # returns a sqlite3.Row or None if not found

def print_person_row(row):
    if row is None:
        print("No record found.")
        return
    
    print("===== Person Record =====")
    print("ID: " + str(row['id']))
    print("First Name: " + str(row['first_name']))
    print("Last Name: " + str(row['last_name']))
    print("Course / Job: " + str(row['course_or_job']))
    print("Location: " + str(row['location']))
    print("Event: " + str(row['event']))
    print("Date: "+ str(row['date']))
    print("=========================")

