from fastapi import FastAPI, HTTPException
from mongoengine import (
    connect,
    disconnect,
    Document,
    StringField,
    ReferenceField,
    ListField,
    IntField
)
import json
from bson import ObjectId  # Import ObjectId for validating MongoDB IDs
from pydantic import BaseModel
from typing import Optional

app = FastAPI()


@app.on_event("startup")
def startup_db_client():
    # Set the correct parameters to connect to the database
    connect("fast-api-database", host="mongodb://mongo:27017", port=27017)


@app.on_event("shutdown")
def shutdown_db_client():
    # Set the correct parameters to disconnect from the database
    disconnect("fast-api-database")


# Helper functions to convert MongeEngine documents to json
def course_to_json(course):
    course = json.loads(course.to_json())
    course["students"] = list(map(lambda dbref: str(dbref["$oid"]), course["students"]))
    course["id"] = str(course["_id"]["$oid"])
    course.pop("_id")
    return course


def student_to_json(student):
    student = json.loads(student.to_json())
    student["id"] = str(student["_id"]["$oid"])
    student.pop("_id")
    return student


# Schema
class Student(Document):
    # Implement the Student schema according to the instructions
    name = StringField(required=True)
    student_number = IntField()


class Course(Document):
    # Implement the Course schema according to the instructions
    name = StringField(required=True)
    description = StringField()
    tags = ListField(StringField())
    students = ListField(ReferenceField(Student))


# Input Validators
class CourseData(BaseModel):
    name: str
    description: str | None  # Optional attribute
    tags: list[str] | None
    students: list[str] | None


class StudentData(BaseModel):
    name: str
    student_number: int | None


# Course CRUD routes
# Complete the Course routes similarly as per the instructions provided in A+

@app.post("/courses", status_code=201)
def create_course(course_data: CourseData):
    try:
        course = Course(**course_data.dict()).save()
        return {"message": "Course successfully created", "id": str(course.id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/courses")
def get_courses(tag: str | None = None, studentName: str | None = None):
    """
    :param tag: filter courses by tag
    :param studentName: filter courses by student name
    :return: Multiple database objects [Course]
    """
    query = {}
    if tag:
        query["tags__icontains"] = tag
    elif studentName:
        query["students__name__icontains"] = studentName
    try:
        courses = Course.objects(**query)  # Query the database
        return [course_to_json(course) for course in courses]
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/courses/{course_id}")
def get_course(course_id: str):
    """
    :param course_id: string
    :return: Single database object [Course]
    """
    # Validate course_id format
    if not ObjectId.is_valid(course_id):
        raise HTTPException(status_code=400, detail="Invalid course ID format")
    # Query the database
    course = Course.objects.get(id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course_to_json(course)


@app.put("/courses/{course_id}")
def update_course(course_id: str, course_data: CourseData):
    course = Course.objects.get(id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    course.update(**course_data.dict())
    return {"message": "Course successfully updated"}


@app.delete("/courses/{course_id}")
def delete_course(course_id: str):
    course = Course.objects(id=course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    course.delete()
    return {"message": "Course successfully deleted"}


# Routes for Students

@app.post("/students", status_code=201)
def create_student(student_data: StudentData):
    try:
        student = Student(**student_data.dict()).save()
        return {"message": "Student successfully created", "id": str(student.id)}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/students/{student_id}")
def get_student(student_id: str):
    """
    :param student_id: str
    :return: Single database object [Student]
    """
    student = Student.objects.get(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student_to_json(student)


@app.put("/students/{student_id}")
def update_student(student_id: str, student_data: StudentData):
    student = Student.objects.get(id=student_id)
    student.update(**student_data.dict())
    return {"message": "Student successfully updated"}


@app.delete("/students/{student_id}")
def delete_student(student_id: str):
    student = Student.objects(id=student_id)
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    student.delete()
    return {"message": "Student successfully deleted"}
