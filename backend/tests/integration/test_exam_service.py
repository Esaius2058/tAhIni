import pytest, sys, os, json
from datetime import datetime, timedelta
from sqlalchemy.orm import sessionmaker
from ..conftest import test_db_session
from src.db.models import Exam, Course, Semester, Question, QuestionType
from src.services.exam import ExamService
from src.utils.exceptions import NotFoundError, ServiceError

@pytest.fixture
def exam_service(test_db_session):
    return ExamService(test_db_session)

def instantiate_course_semester(test_db_session):
    course = Course(id="MATH110", name="Introduction to Vectors")
    test_db_session.add(course)
    test_db_session.commit()
    semester = Semester(name="Year 1 Semester 1",
                        end_date=datetime.now() + timedelta(days=79)
                        )
    test_db_session.add(semester)
    test_db_session.commit()
    return {"course": course,"semester": semester}

def test_create_exam(exam_service, test_db_session):
    course_semester = instantiate_course_semester(test_db_session)
    course = course_semester["course"]
    semester = course_semester["semester"]
    exam_service.create_exam("Math", "End of Semester Exam", course.id, semester.id)
    exam = test_db_session.query(Exam).filter_by(subject="Math").first()
    assert exam is not None
    assert exam.duration == "2h"

def test_get_exam_by_id(exam_service, test_db_session):
    course_semester = instantiate_course_semester(test_db_session)
    course = course_semester["course"]
    semester = course_semester["semester"]
    exam_service.create_exam("Biology", "End of Semester Exam", course.id, semester.id)
    exam = test_db_session.query(Exam).filter_by(subject="Biology").first()
    exam_service.get_exam_by_id(exam.id)

    assert exam.title == "End of Semester Exam"

def test_get_exams_by_course(exam_service, test_db_session):
    course_semester = instantiate_course_semester(test_db_session)
    course = course_semester["course"]
    semester = course_semester["semester"]
    exam_service.create_exam("Sociology", "End of Semester Exam", course.id, semester.id)
    exam_service.create_exam("Biology", "End of Semester Exam", course.id, semester.id)
    exam_service.create_exam("Math", "End of Semester Exam", course.id, semester.id)
    exam = test_db_session.query(Exam).filter_by(subject="Sociology").first()

    fetched = exam_service.get_exams_by_course(exam.course_id, exam.semester_id)
    assert fetched is not None
    assert len(fetched) == 3
    assert fetched[0].id == exam.id

def test_list_exam_questions(exam_service, test_db_session):
    course_semester = instantiate_course_semester(test_db_session)
    course = course_semester["course"]
    semester = course_semester["semester"]
    exam_service.create_exam("Religion", "End of Semester Exam", course.id, semester.id)
    exam_service.create_exam("Physics", "End of Semester Exam", course.id, semester.id)
    exam_service.create_exam("Computer", "End of Semester Exam", course.id, semester.id)
    exam1 = test_db_session.query(Exam).filter_by(subject="Religion").first()
    question1 = Question(
        type=QuestionType.SHORT_ANSWER,
        difficulty="medium",
        tags=[
            "biology",
            "anatomy",
            "pharmacology"
        ],
        exam_id=exam1.id
    )
    question2 = Question(
        type=QuestionType.CODE,
        difficulty="medium",
        tags=[
            "java",
            "programming",
            "object-oriented-programming"
        ],
        exam_id=exam1.id
    )
    question3 = Question(
        type=QuestionType.SHORT_ANSWER,
        difficulty="medium",
        tags=[
            "force",
            "newton's laws",
            "physics"
        ],
        exam_id=exam1.id
    )
    question4 = Question(
        type=QuestionType.ESSAY,
        difficulty="medium",
        tags=[
            "christian ethics",
            "religion",
            "bible"
        ],
        exam_id=exam1.id
    )
    test_db_session.add_all([question1, question2, question3, question4])
    test_db_session.commit()
    questions = exam_service.list_exam_questions(exam1.id)

    assert questions is not None
    assert len(questions) == 4
    assert "force" in questions[2].tags

def test_list_exams(exam_service, test_db_session):
    course_semester = instantiate_course_semester(test_db_session)
    course = course_semester["course"]
    semester = course_semester["semester"]
    exam_service.create_exam("Sociology", "End of Semester Exam", course.id, semester.id)
    exam_service.create_exam("Biology", "End of Semester Exam", course.id, semester.id)
    exam_service.create_exam("Math", "End of Semester Exam", course.id, semester.id)
    exam_service.create_exam("Math", "End of Semester Exam", course.id, semester.id)
    exam_service.create_exam("Math", "End of Semester Exam", course.id, semester.id)

    math_exams = exam_service.list_exams(subject="Math")
    end_of_sem_exams = exam_service.list_exams(title="End of Semester Exam")
    assert math_exams is not None
    assert len(math_exams) == 3
    assert len(end_of_sem_exams) == 5

def test_update_exam(exam_service, test_db_session):
    course_semester = instantiate_course_semester(test_db_session)
    course = course_semester["course"]
    semester = course_semester["semester"]
    exam_service.create_exam("Sociology", "End of Semester Exam", course.id, semester.id)
    exam = test_db_session.query(Exam).filter_by(subject="Sociology").first()
    updated = exam_service.update_exam(exam_id=exam.id, subject="Christian Ethics")

    assert updated is not None
    assert updated.id == exam.id

def test_delete_exam(exam_service, test_db_session):
    course_semester = instantiate_course_semester(test_db_session)
    course = course_semester["course"]
    semester = course_semester["semester"]
    exam_service.create_exam("Christian Ethics", "End of Semester Exam", course.id, semester.id)
    exam = test_db_session.query(Exam).filter_by(subject="Christian Ethics").first()

    deleted = exam_service.delete_exam(exam.id)
    assert deleted == True

