import mysql.connector
from datetime import date   
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from mis.backend.logic import std_logic


from starlette.middleware.sessions import SessionMiddleware
#          python3.13 -m uvicorn mis.backend.routes.std_api:app --reload
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="replace-with-a-real-secret")
templates = Jinja2Templates(directory="mis/backend/templates")

@app.get("/loginCheck")
def loginCheck(request: Request, misid: str, password: str):
    student_id = std_logic.login(misid, password)
    if student_id:
        request.session["student_id"] = student_id
        return {"status": "ok", "message": "Login successful"}
    return {"status": "error", "message": "Invalid MIS ID or password"}

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="mis_portal.html",
        context={}
    )


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="dashboard.html",
        context={}
    )
@app.get("/stdinfo")
def info(request: Request):
    student_id = request.session.get("student_id")
    if not student_id:
        return {"status": "error", "message": "Not logged in"}
    result = std_logic.info(student_id)
    if result == "Student not found" or result is None:
        return {"status": "error", "message": "Student not found"}
    return {"status": "ok", "student": result}

@app.post("/changeinfo")
def changeinfo(request: Request, dob: str = Form(...), gender: str = Form(...), StudentPhone: str = Form(...), Parentphone: str = Form(...), Address: str = Form(...), ParentEmail: str = Form(...)):
    student_id = request.session.get("student_id")
    if not student_id:
        return {"status": "error", "message": "Not logged in"}
    std_logic.changeinfo(dob, gender, StudentPhone, Parentphone, Address, ParentEmail, student_id)
    return {"status": "ok", "message": "Information updated successfully"}




@app.get("/attendance")
def attendance(request: Request, month: int, year: int):
    student_id = request.session.get("student_id")
    if not student_id:
        return {"status": "error", "message": "Not logged in"}
    attendance_records = std_logic.checkAttendance(student_id, month, year)
    return {"status": "ok", "attendance": attendance_records}

@app.get("/attendance/summary")
def attendance_summary(request: Request, month: int, year: int):
    student_id = request.session.get("student_id")
    if not student_id:
        return {"status": "error", "message": "Not logged in"}
    summary = std_logic.getAttendanceSummary(student_id, month, year)
    return {"status": "ok", "summary": summary}

@app.get("/attendance/daysofclass")
def days_of_class(request: Request, month: int, year: int):
    student_id = request.session.get("student_id")
    if not student_id:
        return {"status": "error", "message": "Not logged in"}
    days = std_logic.getdaysofclass(student_id, month, year)
    return {"status": "ok", "days": days}

@app.get("/attendance/daysofclass")
def days_of_class(request: Request, month: int, year: int):
    student_id = request.session.get("student_id")
    if not student_id:
        return {"status": "error", "message": "Not logged in"}
    days = std_logic.getdaysofclass(student_id, month, year)
    return {"status": "ok", "days": days}


@app.get("/fees")
def fees(request: Request):
    student_id = request.session.get("student_id")
    if not student_id:
        return {"status": "error", "message": "Not logged in"}
    fees = std_logic.getfee(student_id)
    return {"status": "ok", "fees": fees}



@app.get("/finalresults")
def results(request: Request, classid: int):
    student_id = request.session.get("student_id")
    if not student_id:
        return {"status": "error", "message": "Not logged in"}
    results = std_logic.getfinalresults(student_id, classid)
    return {"status": "ok", "results": results}


@app.get("/midsresults")
def mids_results(request: Request, classid: int):
    student_id = request.session.get("student_id")
    if not student_id:
        return {"status": "error", "message": "Not logged in"}
    results = std_logic.getmidtermresults(student_id, classid)
    return {"status": "ok", "results": results}


@app.get("/firstresults")
def first_results(request: Request, classid: int):
    student_id = request.session.get("student_id")
    if not student_id:
        return {"status": "error", "message": "Not logged in"}
    results = std_logic.getfirsttermresults(student_id, classid)
    return {"status": "ok", "results": results}

@app.get("/subjectresults")
def subject_results(request: Request, subject: str, classid: int):
    student_id = request.session.get("student_id")
    if not student_id:
        return {"status": "error", "message": "Not logged in"}
    results = std_logic.getresultofsubject(student_id, subject, classid)
    return {"status": "ok", "results": results}



@app.get("/diary")
def getdiary(request:Request , classId:int):
    student_id = request.session.get("student_id")
    if not student_id:
        return {"status": "error", "message": "Not logged in"}
    result=std_logic.getdiary(classId)
    return {"status":"ok","result":result}

@app.get("/diaryofsubject")
def diaryofsubject(request:Request , classID:int ,subjectID:int):
    student_id = request.session.get("student_id")
    if not student_id:
        return {"status": "error", "message": "Not logged in"}
    result=std_logic.getsubjectdiary(classID,subjectID)
    return {"status":"ok","result":result}

@app.get("/diaryoftime")
def diaryoftime(request:Request,classid:int,date1:str,date2:str):
    student_id = request.session.get("student_id")
    if not student_id:
        return {"status": "error", "message": "Not logged in"}
    result=std_logic.getdiaryoftime(classid,date1,date2)
    return {"status":"ok","result":result}

@app.get("/subjects")
def getsubjects(request:Request):
    student_id = request.session.get("student_id")
    if not student_id:
        return {"status": "error", "message": "Not logged in"}
    result=std_logic.getsubject()
    return {"status":"ok","result":result}

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return {"status": "ok"}