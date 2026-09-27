import datetime
import json
import uuid

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










