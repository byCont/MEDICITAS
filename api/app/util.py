import os
import uuid
import smtplib
from datetime import date, time, datetime
from dateutil.relativedelta import relativedelta
from email.message import EmailMessage
from typing import Any, Type, List, Optional
from fastapi import Form, UploadFile
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import ColumnCollection
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from pydantic import BaseModel, root_validator
from app.config import config

format = {
    "date": "%m/%d/%Y",
    "time": "%H:%M:%S",
    "datetime": "%m/%d/%Y %H:%M:%S"
}

operators = {
    "c": lambda col, val: col.like(f"%{val}%"),
    "e": lambda col, val: col == val,
    "g": lambda col, val: col > val,
    "ge": lambda col, val: col >= val,
    "l": lambda col, val: col < val,
    "le": lambda col, val: col <= val,
}

def get_operator(oper: str) -> Any:
    return operators.get(oper, operators["e"])

def get_column_attr(selected_columns: ColumnCollection, column: str) -> Any:
    for col in selected_columns:
        model = col["entity"].__name__
        field = col["name"]
        if col["aliased"]:
            model = col["entity"]._aliased_insp.name
        if col["expr"].__class__.__name__ == "Label":
            field = list(col["expr"].base_columns)[0].name
        if f"{model}.{field}" == column:
            return getattr(col["entity"], column.split(".")[1])
    return None

async def get_error(exc: Exception) -> JSONResponse:
    if isinstance(exc, RequestValidationError):
        errors = {}
        for error in exc.errors():
            field_name = error["loc"][-1]
            errors[field_name] = error["msg"]
        return JSONResponse({ "errors": errors }, 400)
    elif isinstance(exc, IntegrityError):
        return JSONResponse({ "message": str(exc.orig) }, 400)
    else:
        return JSONResponse({ "message": str(exc) }, 400)
    
async def get_file(folder: str, file: UploadFile) -> str:
    os.makedirs(os.path.join("uploads", folder), exist_ok=True)
    _, ext = os.path.splitext(file.filename)
    while True:
        file_name = f"{str(uuid.uuid4())[24:]}{ext}"
        file_path = os.path.join("uploads", folder, file_name)
        if not os.path.exists(file_path):
            break
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return file_name

def send_mail(type: str, email: str, token: str, user: str = None):
    body = config["mail"][type]
    body = body.replace("{app_url}", config["app"]["url"])
    body = body.replace("{app_name}", config["app"]["name"])
    body = body.replace("{token}", token)
    if user:
        body = body.replace("{user}", user)
    subject = "Login Information" if type == "welcome" else ("Reset Password" if type == "reset" else f'{config["app"]["name"]} message')
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = config["mail"]["sender"]
    msg["To"] = email
    # You need to complete the SMTP Server configuration before you can sent mail
    '''
    with smtplib.SMTP(config["smtp"]["host"], config["smtp"]["port"]) as smtp:
        smtp.starttls()
        smtp.login(config["smtp"]["user"], config["smtp"]["password"])
        smtp.send_message(msg)
    '''

def get_item(db: Session, query: Any) -> Any:
    return format_data(db.execute(query).fetchone()._mapping)

def get_list(db: Session, query: Any) -> Any:
    return format_data(db.execute(query).mappings().all())

def get_datetime(value) -> datetime:
    return datetime.strptime(value, format["datetime"])

def get_date(value) -> date:
    return datetime.strptime(value, format["date"]).date()

def get_time(value) -> time:
    return datetime.strptime(value, format["time"]).time()

def get_date_query(value) -> Any:
    if len(value) > 11:
        return get_datetime(value)
    elif len(value) == 10:
        return get_date(value)
    else:
        return get_time(value)

def format_data(data: Any) -> Any:
    if isinstance(data, List):
        rows = []
        for row in data:
            rows.append(format_data(row))
        return rows
    else:
        data = dict(data)
        for key in data:
            if isinstance(data[key], datetime):
                data[key] = data[key].strftime(format["datetime"])
            elif isinstance(data[key], date):
                data[key] = data[key].strftime(format["date"])
            elif isinstance(data[key], time):
                data[key] = data[key].strftime(format["time"])
            elif isinstance(data[key], bytes):
                data[key] = data[key].replace(b"\x00", b"")
        return data

def form_body(cls: Type) -> Type:
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(None) if arg.default is None else Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls

class Model(BaseModel):

    @root_validator(pre=True)
    def parse_date(cls, values):
        for field, value in values.items():
            if value == "":
                values[field] = None
            if value:
                type = cls.__annotations__.get(field)
                if type == datetime or type == Optional[datetime]:
                    values[field] = get_datetime(value)
                elif type == date or type == Optional[date]:
                    values[field] = get_date(value)
                elif type == time or type == Optional[time]:
                    values[field] = get_time(value)
        return values