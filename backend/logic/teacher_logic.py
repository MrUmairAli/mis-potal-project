from mis.backend.logic import std_logic


def teacherlogin(teacherid:int,password:str):
    db=std_logic.get_db()
    cursor=db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM teachers WHERE TeacherID = %s AND passwords = %s",
        (teacherid, password)
    )
    result = cursor.fetchone()
    db.close ()
    if result is None:
        return False
    else :
        return result["TeacherID"]


def getteacherdata(teacherid:int):

    db=std_logic.get_db()
    cursor=db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM teachers WHERE TeacherID = %s",
        (teacherid,)
    )

    result = cursor.fetchone()
    db.close()
    return result
    


def changeinfo(teachersid:int ,email:str, dob:str, gender:str, teacherPhone:str):
    db = std_logic.get_db()
    cursor = db.cursor()
    cursor.execute(
        "update teachers set DOB = %s, Gender = %s, Phone = %s, Email = %s where TeacherID = %s",
        (dob, gender, teacherPhone, email, teachersid ))
    db.commit()
    db.close()
    return True


def showStudentsOfaClass(classid:int):
    db=std_logic.get_db()
    cursor=db.cursor(dictionary=True)
    cursor.execute(
        "SELECT * FROM students WHERE ClassID = %s",
        (classid,)
    )
    result = cursor.fetchall()
    db.close()
    if result is None:
        return "No students found  "
    return result

    

def takeattandecne (studentid :int, date:str , status:str , classid:int, remarks:str=None):
    db=std_logic.get_db()
    cursor=db.cursor(dictionary=True)  
    cursor.execute(
        "SELECT * FROM attendance WHERE StudentID = %s AND Date = %s",
        (studentid, date)
    ) 
    x=cursor.fetchone()
    if x is not None:   
        return False
    cursor.execute(
        "INSERT INTO attendance (StudentID, Date, Status, ClassID, Remarks) VALUES (%s, %s, %s, %s, %s)",
        (studentid, date, status, classid, remarks)
    )
    db.commit()
    db.close()
    return True


def checkattandece(studentid:int ,date:str ):
    db=std_logic.get_db(    )
    cursor=db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM attendance WHERE StudentID = %s AND Date = %s", (studentid, date))
    result = cursor.fetchone()
    db.close()
    return result


def changeattandence(studentid:int, date:str, status:str, classid:int, remarks:str=None):
    db=std_logic.get_db()
    cursor=db.cursor(dictionary=True)  
    cursor.execute(
        "UPDATE Attendance SET Status = %s, Remarks = %s WHERE StudentID = %s AND Date = %s AND ClassID = %s",
        (status, remarks, studentid, date, classid)
    )
    db.commit()
    db.close()
    return True


def givediary(teacherId: int, classid: int, subjectid: int, content: str, date: str):
    db = std_logic.get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "insert into Diary (TeacherID, ClassID, SubjectID, Date, Diarycontent) values (%s, %s, %s, %s, %s)",
        (teacherId, classid, subjectid, date, content,)
    )
    db.commit()
    db.close()
    return True


def showmydiaries(teacherid: int, classid: int):
    db = std_logic.get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "select DiaryID, ClassID, SubjectID, Date, Diarycontent from Diary where TeacherID=%s and ClassID=%s order by Date desc",
        (teacherid, classid)
    )
    result = cursor.fetchall()   # <-- was missing; function never fetched or returned real data before
    db.close()
    return result


def changediary(diaryid: int, content: str):
    db = std_logic.get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "update Diary set Diarycontent = %s where DiaryID = %s",   # <-- was "content", column is "Diarycontent"
        (content, diaryid)
    )
    db.commit()
    db.close()
    return True


def deletediaries(diaryid: int):
    db = std_logic.get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
        "delete from Diary where DiaryID = %s",   # <-- "delete * from" is invalid SQL, DELETE doesn't take columns
        (diaryid,)
    )
    db.commit()
    db.close()
    return True

def getsubject( ):
    db =std_logic.get_db()
    cursor=db.cursor(dictionary=True)
    cursor.execute("select * from subjects")
    result =cursor.fetchall()
    db.close()
    return result

def getsalary ( teacherid:int):
    db = std_logic.get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
       " select * from TeacherSalary where TeacherID =%s",(teacherid,)
    )
    result =cursor.fetchall()
    db.close()
    return result


def getmonthlysalary ( teacherid:int , month : int ):
    db = std_logic.get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
       " select * from TeacherSalary where TeacherID =%s and Month =%s",(teacherid,month,)
    )
    result =cursor.fetchall()
    db.close()
    return result


def getyearlysalary ( teacherid : int , year : int):
    db = std_logic.get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
       " select * from TeacherSalary where TeacherID =%s Year =%s",(teacherid,year,)
    )
    result =cursor.fetchall()
    db.close()
    return result













