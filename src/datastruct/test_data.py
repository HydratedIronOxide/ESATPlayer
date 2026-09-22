from uuid import UUID

# class for containing test questions data
class TestQuestion:
    __slots__ = ("__id", "__question", "__choices")
    def __init__(self, question: str, choices: tuple[str, ...], uid: UUID):
        self.__id = uid
        self.__question = question
        self.__choices = choices

    @property
    def id(self): return self.__id

    @property
    def question(self): return self.__question

    @property
    def choices(self): return self.__choices

