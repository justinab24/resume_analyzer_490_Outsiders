import pytest
from unittest.mock import MagicMock

# Mock Classes
class MockChatCompletion:
    def __init__(self, choices, id, created, model, usage):
        self.choices = choices
        self.id = id
        self.created = created
        self.model = model
        self.usage = usage

class MockChoice:
    def __init__(self, finish_reason, index, message):
        self.finish_reason = finish_reason
        self.index = index
        self.message = message

class MockChatCompletionMessage:
    def __init__(self, content):
        self.content = content
