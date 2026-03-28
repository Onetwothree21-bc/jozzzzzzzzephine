#sqllite in python
#1. connect to a database file
#2. create tables
#3. insert data
#4. query data


import sqlite3
import json
import numpy as np
import pandas as pd
import os

DB_NAME = "face_voice.db"

def init_db(reset=False):
#reset database
    if os.path.exists("face_voice.db"):
        os.remove("face_voice.db")
#create a database
#creates a file called face_voice.db
#connet: if file exists it opens it, if not it creates it
    conn = sqlite3.connect("face_voice.db")
    conn.row_factory = sqlite3.Row # allows names instead of indexes
#cursor lets run sql commands
    cursor = conn.cursor()

#create table

#person id assigned by database
#face recognition from webcam
#information from text to speech
#information from text to speech
#information from text to speech
#information from text to speech
#information from text to speech
#from raspberry pi

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS people(
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        face_embedding TEXT, 
        first_name TEXT, 
        last_name TEXT, 
        course_or_job TEXT,
        location TEXT, 
        event TEXT, 
        date TEXT 
    )              
    """)
    conn.commit()
    return conn, cursor

def insert_person(conn, cursor, embedding, first, last, job, location, event, date):
    cursor.execute("""
        INSERT INTO people (
            face_embedding, first_name, last_name,
            course_or_job, location, event, date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        json.dumps(embedding),
        first,
        last,
        job,
        location,
        event,
        date
    ))
    conn.comit()

def get_all_people(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM people")             
    return cursor.fetchall()

def get_face_dataset(conn):
    rows = get_all_people(conn)

    encodings = []
    names = []

    for row in rows:
        encodings.append(json.loads(row["face_embedding"]))
        names.append((row["first_name"], row["last_name"]))
    
    return encodings, names