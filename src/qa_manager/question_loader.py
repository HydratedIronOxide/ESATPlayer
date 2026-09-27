import json
import uuid

from src.datastruct.test_data import TestQuestion
from src.paths import BANK_DIR


def populate_id(bank_id: str):
    with open(BANK_DIR / bank_id, "r") as f:
        bank_j = json.load(f)

    changed = False
    for question in bank_j["questions"]:
        if question['id'] is None:
            question['id'] = str(uuid.uuid4())
            changed = True

    if changed:
        with open(BANK_DIR / bank_id, "w") as f:
            json.dump(bank_j, f, indent=4)



def load_questions(bank_id: str):
    populate_id(bank_id)
    with open(BANK_DIR / bank_id, "r") as f:
        bank_j = json.load(f)

    bank = []
    for question in bank_j["questions"]:
        bank.append(TestQuestion(
            question["question"],
            tuple(question["choices"]),
            uuid.UUID(question['id']),
            question["correct_answer"]
        ))

    return {
        "name": bank_j["title"],
        "questions": tuple(bank)
    }





