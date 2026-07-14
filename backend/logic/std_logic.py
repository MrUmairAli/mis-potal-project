import mysql.connector
import time

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

    
def checkAttendance(student_id: int, month: int, year: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT Status, Date FROM Attendance WHERE StudentID = %s AND MONTH(Date) = %s AND YEAR(Date) = %s",
        (student_id, month, year)
    )
    result = cursor.fetchall()
    db.close()
    return result


def getAttendanceSummary(student_id: int, month: int, year: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT Status, COUNT(*) as Count FROM Attendance WHERE StudentID = %s AND MONTH(Date) = %s AND YEAR(Date) = %s GROUP BY Status",
        (student_id, month, year)
    )
    result = cursor.fetchall()
    db.close()
    return result


def getdaysofclass(student_id: int, month: int, year: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT Date FROM Attendance WHERE StudentID = %s AND MONTH(Date) = %s AND YEAR(Date) = %s",
        (student_id, month, year)
    )
    result = cursor.fetchall()
    db.close()
    return result


def getattandenceforaday(student_id: int, date: str):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT Status FROM Attendance WHERE StudentID = %s AND Date = %s",
        (student_id, date)
    )
    result = cursor.fetchone()
    db.close()
    if result is None:
        return None
    return result["Status"]   # dict now, not a tuple — index by key, not [0]





def getfee(student_id: int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM Fees WHERE StudentID = %s",
        (student_id,)
    )
    result = cursor.fetchall()
    db.close()
    return result

def getfirsttermresults(student_id: int,classid:int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM Results WHERE StudentID = %s and ExamCategory = 'FirstTerm' and ClassID = %s",
        (student_id, classid)
    )
    result = cursor.fetchall()
    total_marks = sum(row['totalMarks'] for row in result)  
    total_obtain_marks=sum(row['Marks'] for row in result)
    average= total_obtain_marks / len(result) if result else 0 
    sub=getsubjectsid()
    for r in result:
        for s in sub:
            if r['SubjectID'] == s['SubjectID']:
                r['SubjectID'] = s['SubjectName']
                break
        
    
    db.close()
    return {"result": result, "total_marks": total_marks, "total_obtainmarks": total_obtain_marks, "average": average}


def getmidtermresults(student_id: int,classid:int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM Results WHERE StudentID = %s and ExamCategory = 'MidTerm' and ClassID = %s",
        (student_id, classid)
    )
    result = cursor.fetchall()
    total_marks = sum(row['totalMarks'] for row in result)
    total_obtain_marks=sum(row['Marks'] for row in result)
    average= total_obtain_marks / len(result) if result else 0
    db.close()
    sub=getsubjectsid()
    for r in result:
        for s in sub:
            if r['SubjectID'] == s['SubjectID']:
                r['SubjectID'] = s['SubjectName']
                break
    return {"result": result, "total_marks": total_marks, "total_obtainmarks": total_obtain_marks ,"average": average}

def getfinalresults(student_id: int,classid:int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM Results WHERE StudentID = %s and ExamCategory = 'FinalTerm' and ClassID = %s",
        (student_id, classid)
    )
    result = cursor.fetchall()
    total_obtainmarks = sum(row['Marks'] for row in result)
    total_marks=sum(row['totalMarks']for row in result)
    average= total_obtainmarks / len(result) if result else 0
    db.close()
    sub=getsubjectsid()
    for r in result:    
        for s in sub:
            if r['SubjectID'] == s['SubjectID']:
                r['SubjectID'] = s['SubjectName']
                break
    return {"result": result, "total_obtainmarks": total_obtainmarks,"total_marks": total_marks, "average": average}


def getsubjectsid():
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT SubjectID, SubjectName FROM Subjects"
    )
    result = cursor.fetchall()
    db.close()
    return result

def getresultofsubject(student_id: int, subject: str, classid:int):
    db = get_db()
    cursor = db.cursor(dictionary=True)
    sub=getsubjectsid()
    subject_id =None
    for s in sub:
        if subject == s['SubjectName']:
            subject_id = s['SubjectID']
            break
    
    cursor.execute(
        "SELECT * FROM Results WHERE StudentID = %s and SubjectID = %s and ClassID = %s",
        (student_id, subject_id, classid)
    )
    result = cursor.fetchall()
    db.close()
    return  result 




def getdiary(classID: int):
    """Get all diary entries for a class"""
    db = get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM Diary WHERE ClassID = %s ORDER BY Date ASC",
        (classID,)
    )
    result = cursor.fetchall()
    te=getteacher()
    se=getsubject()

    for record in result :
        for  t in te :
            if record ["TeacherID"]==t["TeacherID"]:
                record["TeacherID"]=t["TeacherName"]
    for record in result:
        for s in se:
            if record ["SubjectID"]==s["SubjectID"]:
                record["SubjectID"]=s["SubjectName"]
    db.close()
    return result

def getdiaryoftime(classId:int,startingdate:str ,endingdate:str):
    db =get_db()
    cursor=db.cursor(dictionary=True)
    cursor.execute("select * from Diary where ClassId =%s and Date between %s and %s order by date asc",(classId,startingdate,endingdate,))
    result =cursor.fetchall()

    te=getteacher()
    se=getsubject()

    for record in result :
        for  t in te :
            if record ["TeacherID"]==t["TeacherID"]:
                record["TeacherID"]=t["TeacherName"]
    for record in result:
        for s in se:
            if record ["SubjectID"]==s["SubjectID"]:
                record["SubjectID"]=s["SubjectName"]
    db.close()
    return result

def getsubject( ):
    db =get_db()
    cursor=db.cursor(dictionary=True)
    cursor.execute("select SubjectID ,SubjectName  from subjects")
    result =cursor.fetchall()

    te=getteacher()
    se=getsubject()

    for record in result :
        for  t in te :
            if record ["TeacherID"]==t["TeacherID"]:
                record["TeacherID"]=t["TeacherName"]
    for record in result:
        for s in se:
            if record ["SubjectID"]==s["SubjectID"]:
                record["SubjectID"]=s["SubjectName"]
    db.close()
    return result

def getteacher():
    
    db =get_db()
    cursor=db.cursor(dictionary=True)
    cursor.execute("select TeacherID, TeacherName  from teachers")
    result =cursor.fetchall()
    db.close()
    return result


def getsubjectdiary(subjectID:int,classId:int):
    db =get_db()
    cursor=db.cursor(dictionary=True)
    cursor.execute("select * from Diary where ClassID =%s and SubjectID = %s order by date asc",(classId,subjectID,))
    result =cursor.fetchall()
    db.close()
    return result






