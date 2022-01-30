import datetime
import json
from random import randint

import boto3
from fire import Fire
from mimesis import Person
from mimesis.locales import Locale

person = Person(Locale.JA)


def dummy_data(num: int) -> dict:
    id = str(num).zfill(3)
    date = datetime.date(2021, randint(1, 12), randint(1, 28)).strftime("%Y-%m-%d")
    dummy_dict = {
        "会員番号": id,
        "名前": person.full_name(reverse=True),
        "会員ランク": randint(1, 5),
        "ポイント": randint(50, 100),
        "タイムスタンプ": date,
    }
    return dummy_dict


def send_json(s3, sample_data: list, bucket: str, send: str) -> str:
    with open("utils/data/sample_data.json", mode="wt", encoding="utf-8") as f:
        json.dump(sample_data, f, ensure_ascii=False, indent=4)
    s3.put_object(
        Body=json.dumps(sample_data, ensure_ascii=False, indent=4),
        Bucket=bucket,
        Key=send,
    )
    return send


def make_dummy_data(k) -> list:
    sample_data = []
    for i in range(k):
        sample_data.append(dummy_data(i))
    return sample_data


def main(iterate_num: int) -> str:
    endpoint = f"http://localhost:4566"
    s3 = boto3.client(
        service_name="s3",
        endpoint_url=endpoint,
        aws_access_key_id="test",
        aws_secret_access_key="test",
    )
    bucket = "test-bucket"
    send = "test.json"
    sample_data = make_dummy_data(iterate_num)
    send = send_json(s3, sample_data, bucket, send)
    return send


if __name__ == "__main__":
    Fire(main)
