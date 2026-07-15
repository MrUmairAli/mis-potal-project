from mis.backend.logic import std_logic
def login ( employeeId:int , employeepass:str):
    db=std_logic.get_db ()
    cursor=db.cursor(dictionary=True)
    cursor.execute("select * from employees where EmployeeID =%s and password =%s ",
                   (employeeId,employeepass))
    result = cursor.fetchone()
    db.close()
    if result is not None:
         return result["EmployeeID"]
    return result

def get_info(id:int):
    db=std_logic.get_db ()
    cursor=db.cursor(dictionary=True)
    cursor.execute("select * from employees where EmployeeID =%s  ",
                   (id))
    result = cursor.fetchone()
    db.close()
    return result

def changeinfo(id:int , email:str ,phone:str ,dob:str ,address:str):
    db=std_logic.get_db ()
    cursor=db.cursor(dictionary=True)
    cursor.execute("update employees set DOB = %s, Email = %s, Phone = %s,  Address = %s, where EmployeeID = %s", 
                   (dob, email, phone,  address, id))   
    db.commit()
    db.close()

def salary(id:int):
    
    db = std_logic.get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
       " select * from EmployeeSalary where EmployeeID =%s",(id,)
    )
    result =cursor.fetchall()
    db.close()
    return result


def getmonthlysalary ( id:int , month : int ):
    db = std_logic.get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
       " select * from EmployeeSalary where EmployeeID =%s and Month =%s",(id,month,)
    )
    result =cursor.fetchall()
    db.close()
    return result


def getyearlysalary ( id : int , year : int):
    db = std_logic.get_db()
    cursor = db.cursor(dictionary=True)
    cursor.execute(
       " select * from EmployeeSalary where EmployeeID =%s and Year =%s",(id,year,)
    )
    result =cursor.fetchall()
    db.close()
    return result

