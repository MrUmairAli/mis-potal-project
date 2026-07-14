from httpcore import request
import mysql.connector      
from datetime import date   
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from mis.backend.logic  import  std_logic, teacher_logic ,employee


from starlette.middleware.sessions import SessionMiddleware
#          python3.13 -m uvicorn mis.backend.routes.teacher_api:app --reload
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="replace-with-a-real-secret")
templates = Jinja2Templates(directory="mis/backend/templates")

@app.get("/", response_class=HTMLResponse)
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="employee_login.html",
        context={}
    )
 
@app.get("/employee/loginCheck")
def loginCheck(request: Request, teacherid: str, password: str):
    employee_id = employee.login(teacherid, password)
    if employee_id:
        request.session["Employee_id"] = employee_id
        return {"status": "ok", "message": "Login successful"}
    return {"status": "error", "message": "Invalid Employee ID or password"}

@app.get("/employee/dashboard",response_class=HTMLResponse)
def setDAshboard(request :Request):
    
    return templates.TemplateResponse(
        request=request,
        name="employee_dashboard.html",
        context={}
    )

@app.get("/teacher/info")
def getteacherdata(request: Request):
    employee_id = request.session.get("Employee_id")
    if not employee_id:
        return {"status": "error", "message": "Not logged in"}
    result = employee.get_info(employee_id)
    if result == "Employee not found" or result is None:
        return {"status": "error", "message": "employee not found"}
    return {"status": "ok", "employee": result}


@app.post("/changeinfo")
def getteacherdata(request: Request , email:str ,phone:str ,dob:str ,address:str):
    employee_id = request.session.get("Employee_id")
    if not employee_id:
        return {"status": "error", "message": "Not logged in"}
    employee.changeinfo(employee_id,email,phone,dob,address)
    return {"status": "ok", "message": "Information updated successfully"}


@app.get("/employee/salary")
def get_salary(request: Request):
    Employee_id = request.session.get("Employee_id")
    if not Employee_id:
        return {"status": "error", "message": "Not logged in"}
    result=employeemployee.salary(Employee_id)
    if not result:
        return {"status": "error", "message": "No salary found"}
    return {"status": "ok", "salary": result}


@app.get("/employee/monthlysalary")
def get_monthlysalary(request: Request, month :int):
    Employee_id = request.session.get("Employee_id")
    if not Employee_id:
        return {"status": "error", "message": "Not logged in"}
    result=employee.getmonthlysalary(Employee_id,month)
    if not result:
        return {"status": "error", "message": "No salary found"}
    return {"status": "ok", "salary": result}


@app.get("/employee/yearlysalary")
def get_yearlysalary(request: Request, month :int , year :int ):
    Employee_id = request.session.get("Employee_id")
    if not Employee_id:
        return {"status": "error", "message": "Not logged in"}
    result=employee.getyearlysalary(Employee_id,month ,year)
    if not result:
        return {"status": "error", "message": "No salary found"}
    return {"status": "ok", "salary": result}


