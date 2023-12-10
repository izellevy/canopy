import pytest

from canopy.chat_engine.query_generator import LastMessageQueryGenerator
from canopy.models.data_models import UserMessage, Query, AssistantMessage, Role


@pytest.fixture
def sample_user_messages():
    return [
        UserMessage(content="What is photosynthesis?")
    ]


@pytest.fixture
def sample_messages():
    return [
        UserMessage(content="What is photosynthesis?"),
        AssistantMessage(content="Oh! I don't know.")
    ]


@pytest.fixture
def query_generator():
    return LastMessageQueryGenerator()


def test_generate(query_generator, sample_user_messages):
    expected = [Query(text=sample_user_messages[-1].content)]
    actual = query_generator.generate(sample_user_messages, 0)
    assert actual == expected


@pytest.mark.asyncio
async def test_agenerate(query_generator, sample_user_messages):
    expected = [Query(text=sample_user_messages[-1].content)]
    actual = await query_generator.agenerate(sample_user_messages, 0)
    assert actual == expected


def test_generate_with_user_and_assistant(query_generator, sample_messages):
    last_user_message = next(message for message in sample_messages if message.role == Role.USER)
    expected = [Query(text=last_user_message.content)]
    actual = query_generator.generate(sample_messages, 0)
    assert actual == expected


def test_generate_fails_with_empty_history(query_generator):
    with pytest.raises(ValueError):
        query_generator.generate([], 0)


def test_generate_fails_with_no_user_message(query_generator):
    with pytest.raises(ValueError):
        query_generator.generate([AssistantMessage(content="Hi! How can I help you?")], 0)