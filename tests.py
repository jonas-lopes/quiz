import pytest
from model import Question

def test_create_question():
    question = Question(title='q1')
    assert question.id != None

def test_create_multiple_questions():
    question1 = Question(title='q1')
    question2 = Question(title='q2')
    assert question1.id != question2.id

def test_create_question_with_invalid_title():
    with pytest.raises(Exception):
        Question(title='')
    with pytest.raises(Exception):
        Question(title='a'*201)
    with pytest.raises(Exception):
        Question(title='a'*500)

def test_create_question_with_valid_points():
    question = Question(title='q1', points=1)
    assert question.points == 1
    question = Question(title='q1', points=100)
    assert question.points == 100

def test_create_choice():
    question = Question(title='q1')
    
    question.add_choice('a', False)

    choice = question.choices[0]
    assert len(question.choices) == 1
    assert choice.text == 'a'
    assert not choice.is_correct

def test_question_rejects_invalid_points():
    with pytest.raises(Exception):
        Question(title='title', points=0)
    with pytest.raises(Exception):
        Question(title='title', points=101)

def test_question_stores_max_selections():
    q = Question(title='q', max_selections=3)
    assert q.max_selections == 3

def test_add_multiple_choices_to_question():
    q = Question(title='q')
    q.add_choice('a', True)
    q.add_choice('b', False)
    assert len(q.choices) == 2

def test_add_choice_marks_correctness():
    q = Question(title='q')
    correct = q.add_choice('correct', True)
    wrong = q.add_choice('wrong', False)
    assert correct.is_correct
    assert not wrong.is_correct

def test_add_choice_validates_text_length():
    q = Question('q')
    with pytest.raises(Exception):
        q.add_choice('a'*101)

def test_add_choice_rejects_empty_text():
    q = Question('q')
    with pytest.raises(Exception):
        q.add_choice('')

def test_choice_has_unique_id():
    q = Question('q')
    a = q.add_choice('a')
    b = q.add_choice('b')
    assert a.id != b.id

def test_question_id_is_hex_string():
    q = Question('q')
    assert isinstance(q.id, str)
    assert all(c in '0123456789abcdef' for c in q.id.lower())

def test_question_title_preserved():
    title = 'Example Question'
    q = Question(title=title)
    assert q.title == title

def test_choice_text_preserved():
    q = Question('q')
    c = q.add_choice('Option A')
    assert c.text == 'Option A'

@pytest.fixture
def empty_question():
    return Question(title="Empty Question", points=2)

def test_empty_question_has_no_choices(empty_question):
    assert empty_question.choices == []

@pytest.fixture
def question_with_choices():
    q = Question(title="Sample question", points=5, max_selections=2)
    q.add_choice("Option A", is_correct=True)
    q.add_choice("Option B", is_correct=False)
    q.add_choice("Option C", is_correct=True)
    return q

def test_question_has_correct_number_of_choices(question_with_choices):
    assert len(question_with_choices.choices) == 3
