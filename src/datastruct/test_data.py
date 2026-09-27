from uuid import UUID

# class for containing test questions data
class TestQuestion:
    __slots__ = ("__id", "__question", "__choices", "__correct")
    def __init__(self, question: str, choices: tuple[str, ...], uid: UUID, correct: str):
        self.__id = uid
        self.__question = question
        self.__choices = choices
        self.__correct = correct

    @property
    def id(self): return self.__id
    @property
    def question(self): return self.__question
    @property
    def choices(self): return self.__choices
    @property
    def correct(self): return self.__correct

