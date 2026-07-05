import mysql.connector


def login(misid: str, password: str):
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "select StudentID from students where StudentID = %s and Password = %s",
        (misid, password)
    )
    result = cursor.fetchone()
    db.close()
    if result is None:
        return False
    return result[0]   # plain StudentID, e.g. 10001


def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",    
        database="school"
    )   


def info(id: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)   # <-- key change
    cursor.execute(
        "select Picpath, StudentID, Name, ParentName, ClassID, DOB, Gender, StudentPhone, ParentPhone, IsActive from students where StudentID = %s",
        (id,)
    )
    result = cursor.fetchone()
    db.close()
    if result is None:
        return None
    return result
    
def changeinfo(dob:str, gender:str, StudentPhone:str, Parentphone:str,Address:str, ParentEmail:str, id:int):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("update students set DOB = %s, Gender = %s, StudentPhone = %s, ParentPhone = %s, Address = %s, ParentEmail = %s where StudentID = %s", (dob, gender, StudentPhone, Parentphone, Address, ParentEmail, id))   
    db.commit()
    db.close()

