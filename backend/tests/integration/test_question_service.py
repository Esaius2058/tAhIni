import os, pytest
from src.db.models import Question, QuestionType
from src.services.questions import QuestionService
from tests.conftest import test_db_session

@pytest.fixture
def question_service(test_db_session):
    return QuestionService(test_db_session)

def test_store_question(question_service, test_db_session):
    question = question_service.store_question(
        text="Who is your favorite rapper?",
        tags=["music", "contemporary", "poetry"],
        type=QuestionType.SHORT_ANSWER
    )
    question_query = test_db_session.query(Question).filter(Question.id == question.id).first()

    assert question_query is not None
    assert "poetry" in question_query.tags

def test_store_question_bulk(question_service, test_db_session):
    question1 = question_service.store_question(
        text="Who is the most influential rapper right now?",
        tags=["music", "contemporary", "poetry"],
        type=QuestionType.SHORT_ANSWER,
        bulk=True
    )
    question2 = question_service.store_question(
        text="In three sentences or more describe love",
        tags=["romance", "contemporary", "life"],
        type=QuestionType.ESSAY,
        bulk=True
    )
    question3 = question_service.store_question(
        text="Is politics a dirty game? Discuss",
        tags=["political", "contemporary", "history", "global"],
        type=QuestionType.ESSAY,
        bulk=True
    )
    questions = [question1, question2, question3]

    test_db_session.add_all(questions)
    test_db_session.commit()

    question_query1 = test_db_session.query(Question).filter(Question.id == question1.id).first()
    question_query2 = test_db_session.query(Question).filter(Question.id == question2.id).first()
    question_query3 = test_db_session.query(Question).filter(Question.id == question3.id).first()

    assert question_query1.type == QuestionType.SHORT_ANSWER
    assert "romance" in question_query2.tags
    assert question_query3.text == "Is politics a dirty game? Discuss"

def get_stored_questions(question_service):
    question1 = question_service.store_question(
        text="Who is the most influential rapper right now?",
        tags=["music", "contemporary", "poetry"],
        type=QuestionType.SHORT_ANSWER,
        bulk=True
    )
    question2 = question_service.store_question(
        text="Do you agree that politics is a dirty game? Explain your view.",
        tags=["political", "ethics", "governance", "society"],
        type=QuestionType.ESSAY,
        bulk=True
    )

    question3 = question_service.store_question(
        text="To what extent can politics be considered a corrupt enterprise?",
        tags=["political", "ethics", "governance", "history"],
        type=QuestionType.ESSAY,
        bulk=True
    )

    question4 = question_service.store_question(
        text="Is the phrase 'politics is a dirty game' justified in today’s world?",
        tags=["political", "philosophy", "global", "media"],
        type=QuestionType.ESSAY,
        bulk=True
    )

    question5 = question_service.store_question(
        text="Critically examine whether politics must always involve manipulation and corruption.",
        tags=["political", "ethics", "critical-thinking", "leadership"],
        type=QuestionType.ESSAY,
        bulk=True
    )

    question6 = question_service.store_question(
        text="Discuss the moral implications of calling politics a dirty game.",
        tags=["political", "ethics", "philosophy", "society"],
        type=QuestionType.ESSAY,
        bulk=True
    )

    question7 = question_service.store_question(
        text="Is it fair to say that politics and morality cannot coexist?",
        tags=["political", "ethics", "philosophy", "leadership"],
        type=QuestionType.ESSAY,
        bulk=True
    )

    questions = [question1, question2, question3, question7, question5, question6, question4]
    return questions

def test_semantic_search(question_service, test_db_session):
    questions = get_stored_questions(question_service)

    test_db_session.add_all(questions)
    test_db_session.commit()

    query_text = "Does engaging in politics always require compromising one’s morals?"
    result = question_service.semantic_search(query_text)

    assert result is not None
    assert len(result) > 3

def test_keyword_search(question_service, test_db_session):
    questions = get_stored_questions(question_service)

    test_db_session.add_all(questions)
    test_db_session.commit()

    keyword = "corrupt"
    result = question_service.keyword_search(keyword)

    assert result is not None
    assert len(result) > 1

def test_hybrid_search(question_service, test_db_session):
    questions = get_stored_questions(question_service)

    test_db_session.add_all(questions)
    test_db_session.commit()

    query = "Discuss whether corruption is inevitable in politics and governance."
    ranked = question_service.hybrid_search(query=query)

    assert len(ranked) > 5

