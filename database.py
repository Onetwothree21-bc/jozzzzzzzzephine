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
"""
id INTEGER PRIMARY KEY AUTOINCREMENT, #person id assigned by database
face_embedding TEXT, #face recognition from webcam
first_name TEXT, #information from text to speech
last_name TEXT, #information from text to speech
course_or_job TEXT, #information from text to speech
location TEXT, #information from text to speech
event TEXT, #information from text to speech
date TEXT #from raspberry pi
"""
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

#example data*********888
people_data = [
    ([0.12, 0.98, 0.33], "BOB", "MR BOB", "physics", "SU", "freshers ball", "2024-10,22"),
    ([0.20, 0.85, 0.40], "BOB2", "MR BOB", "physics", "SU", "freshers ball", "2024-10,22")
]
for person in people_data:
    cursor.execute("""
    INSERT INTO people (
        face_embedding, first_name, last_name,
        course_or_job, location, event, date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
        json.dumps(person[0]),  # embedding → JSON string
        person[1],
        person[2],
        person[3],
        person[4],
        person[5],
        person[6]
    ))

conn.commit()

#read data back
cursor.execute("SELECT * FROM people")
rows = cursor.fetchall()

print("raw datbase rows")
for row in rows:
    print(row)

#convert back to usable data
for row in rows:
    name = row[1]
    face_embedding = json.loads(row["face_embedding"])
    print(name, face_embedding)

#similarity search
import numpy as np

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

##example query embedding************8
query = [0.1, 0.9, 0.3]

best_match = None
best_score = -1

for row in rows:
    stored_embedding = json.loads(row["face_embedding"])

    score = cosine_similarity(query, stored_embedding)

    if score > best_score:
        best_score = score
        best_match = (row["first_name"], row["last_name"])
#add threshold so it doesnt find a match everytime
if best_score < 0.8:
    print("Unknown person")
else:
    print(f"Match: {best_match} (confidence: {best_score:.2f})")

print("Best match:", best_match)
print("Score:", best_score)

#using it with pandas

df = pd.read_sql_query("SELECT * FROM people", conn)
print(df)
df["face_embedding"] = df["face_embedding"].apply(json.loads)
print(df)
#close database
conn.close()