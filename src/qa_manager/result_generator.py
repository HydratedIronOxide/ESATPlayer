import datetime
import json
import uuid

from datastruct.test_data import TestQuestion
from src.paths import SESSIONS_DIR


"""{
    'sid': string uuid4,
    'datetime': int timestamp,
    'result': [
        {
            'qid': string uuid4,
            'selected': string,
            'time': int
        },
        {...},
        ...
    ]
}"""


def generate_result(test_data: list[dict]):
    sid = uuid.uuid4()
    date = datetime.datetime.now()
    result = test_data

    j = json.dumps({
        'sid': str(sid),
        'datetime': int(date.timestamp()),
        'result': result
    }, indent=4)

    with open(SESSIONS_DIR / f"{date.strftime("%Y-%m-%d %H-%M-%S")}.json", 'w') as f:
        f.write(j)



def mark_set(test_data: list[dict], question_data: list[TestQuestion]):
    """Marks the test data against the question data and returns a list of results"""
    results = []
    for i, q in enumerate(question_data):
        qid = str(q.id)
        selected = test_data[i]['selected']
        correct = q.correct
        time = test_data[i]['time']
        is_correct = selected == correct
        results.append({
            'qid': qid,
            'selected': selected,
            'correct': correct,
            'time': time,
            'is_correct': is_correct
        })
    return results







