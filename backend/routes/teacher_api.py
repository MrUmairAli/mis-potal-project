from httpcore import request
import mysql.connector      
from datetime import date   
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from mis.backend.logic  import  std_logic, teacher_logic


from starlette.middleware.sessions import SessionMiddleware
#          python3.13 -m uvicorn mis.backend.routes.teacher_api:app --reload
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="replace-with-a-real-secret")
templates = Jinja2Templates(directory="mis/backend/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="teacher_login.html",
        context={}
    )
@app.get("/teacher/dashboard", response_class=HTMLResponse)
def teacher_dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="teacher_dashboard.html",
        context={}
    )


@app.get("/teacher/loginCheck")
def loginCheck(request: Request, teacherid: str, password: str):
    teacher_id = teacher_logic.teacherlogin(teacherid, password)
    if teacher_id:
        request.session["teacher_id"] = teacher_id
        return {"status": "ok", "message": "Login successful"}
    return {"status": "error", "message": "Invalid Teacher ID or password"}


@app.get("/teacher/info")
def getteacherdata(request: Request):
    teacher_id = request.session.get("teacher_id")
    if not teacher_id:
        return {"status": "error", "message": "Not logged in"}
    result = teacher_logic.getteacherdata(teacher_id)
    if result == "Teacher not found" or result is None:
        return {"status": "error", "message": "Teacher not found"}
    return {"status": "ok", "teacher": result}


@app.post("/teacherchangeinfo")
def changeinfo(request: Request, dob: str, gender: str, teacherPhone: str, email: str):
    teacher_id = request.session.get("teacher_id")
    if not teacher_id:
        return {"status": "error", "message": "Not logged in"}
    teacher_logic.changeinfo(teacher_id, email, dob, gender, teacherPhone)
    return {"status": "ok", "message": "Information updated successfully"}


@app.get("/showStudentsOfaClass")
def showStudentsOfaClass(request: Request, classid: int):   
        
    teacher_id = request.session.get("teacher_id")
    if not teacher_id:
        return {"status": "error", "message": "Not logged in"}
    result = teacher_logic.showStudentsOfaClass(classid)
    if result == "No students found" or result is None:
        return {"status": "error", "message": "No students found"}
    return {"status": "ok", "students": result}


@app.post("/takeattendance")
def takeattendance(request: Request, studentid: int, date: str, status: str, classid: int, remarks: str = None):
    teacher_id = request.session.get("teacher_id")
    if not teacher_id:
        return {"status": "error", "message": "Not logged in"}
    result = teacher_logic.takeattandecne(studentid, date, status, classid, remarks)
    if result == False:
        return {"status": "error", "message": "Attendance already taken"}
    return {"status": "ok", "message": "Attendance recorded successfully"}


@app.get("/getattendance")
def getattendance(request: Request, studentid: int, date: str):
    teacher_id = request.session.get("teacher_id")
    if not teacher_id:
        return {"status": "error", "message": "Not logged in"}
    result = teacher_logic.checkattandece(studentid, date)
    if result == "No attendance records found" or result is None:
        return {"status": "error", "message": "No attendance records found"}
    return {"status": "ok", "attendance": result}

@app.post("/changeattendance")
def changeattendance(request: Request, studentid: int, date: str, status: str, classid: int, remarks: str = None):
    teacher_id = request.session.get("teacher_id")
    if not teacher_id:
        return {"status": "error", "message": "Not logged in"}
    result = teacher_logic.changeattandence(studentid, date, status, classid, remarks)
    if result == False:
        return {"status": "error", "message": "Attendance record not found"}
    return {"status": "ok", "message": "Attendance updated successfully"}

@app.get("/studentinfo")
def studentinfo(request: Request, studentid: int):
    teacher_id = request.session.get("teacher_id")
    if not teacher_id:
        return {"status": "error", "message": "Not logged in"}
    result = std_logic.info(studentid)
    if result == "Student not found" or result is None:
        return {"status": "error", "message": "Student not found"}
    return {"status": "ok", "student": result}



@app.get("/studentsmonthlyattandence")
def Monthlyattendance(request:Request ,studentid:int ,month:int ,year:int):
    teacher_id = request.session.get("teacher_id")
    if not teacher_id:
        return {"status": "error", "message": "Not logged in"}
    result =std_logic.getAttendanceSummary(studentid,month,year)
    return  {"status":"ok","result":result} 

@app.get("/teacher/studentattendance")
def teacher_student_attendance(request: Request, studentid: int, month: int, year: int):
    teacher_id = request.session.get("teacher_id")
    if not teacher_id:
        return {"status": "error", "message": "Not logged in"}
    attendance_records = std_logic.checkAttendance(studentid, month, year)
    return {"status": "ok", "attendance": attendance_records}

@app.post("/teacher/adddiary")
def add_diary(request: Request, classid: int, subjectid: int, content: str, date: str):
    teacher_id = request.session.get("teacher_id")
    if not teacher_id:
        return {"status": "error", "message": "Not logged in"}
    teacher_logic.givediary(teacher_id, classid, subjectid, content, date)
    return {"status": "ok", "message": "Diary entry added"}


@app.get("/teacher/mydiaries")
def get_my_diaries(request: Request, classid: int):
    teacher_id = request.session.get("teacher_id")
    if not teacher_id:
        return {"status": "error", "message": "Not logged in"}
    result = teacher_logic.showmydiaries(teacher_id, classid)
    if not result:
        return {"status": "error", "message": "No diary entries found"}
    return {"status": "ok", "diaries": result}


@app.post("/teacher/changediary")
def change_diary(request: Request, diaryid: int, content: str):
    teacher_id = request.session.get("teacher_id")
    if not teacher_id:
        return {"status": "error", "message": "Not logged in"}
    teacher_logic.changediary(diaryid, content)
    return {"status": "ok", "message": "Diary entry updated"}


@app.post("/teacher/deletediary")
def delete_diary(request: Request, diaryid: int):
    teacher_id = request.session.get("teacher_id")
    if not teacher_id:
        return {"status": "error", "message": "Not logged in"}
    teacher_logic.deletediaries(diaryid)
    return {"status": "ok", "message": "Diary entry deleted"}

@app.get("/teacher/subjects")
def get_subjects(request: Request):
    teacher_id = request.session.get("teacher_id")
    if not teacher_id:
        return {"status": "error", "message": "Not logged in"}
    result = teacher_logic.getsubject()
    if not result:
        return {"status": "error", "message": "No subjects found"}
    return {"status": "ok", "subjects": result}


@app.get("/teacher/salary")
def get_salary(request: Request):
    teacher_id = request.session.get("teacher_id")
    if not teacher_id:
        return {"status": "error", "message": "Not logged in"}
    result=teacher_logic.getsalary(teacher_id)
    if not result:
        return {"status": "error", "message": "No salary found"}
    return {"status": "ok", "salary": result}


@app.get("/teacher/monthlysalary")
def get_monthlysalary(request: Request, month :int):
    teacher_id = request.session.get("teacher_id")
    if not teacher_id:
        return {"status": "error", "message": "Not logged in"}
    result=teacher_logic.getmonthlysalary(teacher_id,month)
    if not result:
        return {"status": "error", "message": "No salary found"}
    return {"status": "ok", "salary": result}


@app.get("/teacher/yearlysalary")
def get_yearlysalary(request: Request, year:int ):
    teacher_id = request.session.get("teacher_id")
    if not teacher_id:
        return {"status": "error", "message": "Not logged in"}
    result=teacher_logic.getyearlysalary(teacher_id,year)
    if result is None:
        return {"status": "error", "message": "No salary found"}
    return {"status": "ok", "salary": result}


