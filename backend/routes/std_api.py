import mysql.connector
from datetime import date   
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from mis.backend.logic import std_logic


from starlette.middleware.sessions import SessionMiddleware

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

@app.get("/logout")
def logout(request: Request):
    request.session.clear()
    return {"status": "ok"}