import os, pytest
from src.utils.exceptions import NotFoundError
from src.utils.embeddings import generate_embedding
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

def test_semantic_search(question_service, test_db_session, stored_questions):
    query_text = "Does engaging in politics always require compromising one’s morals?"
    result = question_service.semantic_search(query_text)

    assert len(stored_questions) == 7
    assert len(stored_questions[0].embedding) == 1536
    assert result is not None
    assert len(result) > 3

def test_keyword_search(question_service, test_db_session, stored_questions):
    keyword = "corrupt"
    result = question_service.keyword_search(keyword)

    assert result is not None
    assert len(result) > 1

def test_hybrid_search(question_service, stored_questions):
    query = "Discuss whether corruption is inevitable in politics and governance."
    ranked = question_service.hybrid_search(query=query)

    assert len(ranked) > 5

def test_get_question_by_id(question_service, sample_question):
    result = question_service.get_question_by_id(sample_question.id)
    assert result.id == sample_question.id
    assert result.text == "What is the capital of France?"


def test_get_question_by_id_not_found(question_service):
    question = non_existent_question()
    with pytest.raises(NotFoundError):
        question_service.get_question_by_id(question.id)


def test_get_questions_by_tags(question_service, test_db_session, sample_question):
    results = question_service.get_questions_by_tags(["geography"])
    assert any("geography" in q.tags for q in results)


def test_list_questions_with_filters(question_service, sample_question):
    results = question_service.list_questions(tags=["geography"], difficulty="easy")
    assert len(results) >= 1
    assert results[0].difficulty == "easy"


def test_update_question(question_service, test_db_session, sample_question):
    question_service.update_question(
        sample_question.id,
        new_difficulty="medium",
        tags=["updated"],
        question_type=QuestionType.TRUE_FALSE
    )

    updated = test_db_session.query(Question).filter_by(id=sample_question.id).first()
    assert updated.difficulty == "medium"
    assert "updated" in updated.tags
    assert updated.type == QuestionType.TRUE_FALSE


def test_delete_question(question_service, test_db_session, sample_question):
    deleted = question_service.delete_question(sample_question.id)
    assert deleted is True
    assert test_db_session.query(Question).filter_by(id=sample_question.id).first() is None


def test_delete_nonexistent_question(question_service):
    question = non_existent_question()
    deleted = question_service.delete_question(question.id)
    assert deleted is False
