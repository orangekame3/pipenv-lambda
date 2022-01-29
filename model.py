import logging
import pandas as pd
import tempfile
import json
from typing import List


logger = logging.getLogger()
logger.setLevel(logging.INFO)


class Handler(object):
    def __init__(self, event, context, s3):
        self.event = event
        self.context = context
        self.s3 = s3

    def main(self) -> str:
        try:
            bucket = "test-bucket"
            send = "test.xlsx"
            data_path = self.event["input_obj"]
            dict_data: List[dict] = self.get_s3_data(bucket, data_path)
            df = self.make_df(dict_data)
            df_processed = self.process(df)
            send = self.send_excel(df_processed, bucket, send)
            return "completed : {0}".format(send)

        except Exception as e:
            logger.exception(e)
            raise e

    def get_s3_data(self, bucket: str, key: str) -> List[dict]:
        resp = self.s3.get_object(Bucket=bucket, Key=key)
        body = resp["Body"].read().decode("utf-8")
        json_dict: List[dict] = json.loads(body)
        return json_dict

    def make_df(self, data: list) -> pd.DataFrame:
        df = pd.DataFrame.from_dict(data)
        return df

    def calc(self, row):
        if row["会員ランク"] > 3:
            return row["ポイント"] * 1.25
        else:
            return row["ポイント"]

    def process(self, data: pd.DataFrame) -> pd.DataFrame:
        data["ボーナスポイント"] = data.apply(self.calc, axis=1)
        return data

    def send_excel(self, df: pd.DataFrame, bucket: str, send: str) -> str:
        with tempfile.TemporaryFile() as fp:
            writer = pd.ExcelWriter(fp, engine="xlsxwriter")
            df.to_excel(writer, sheet_name="Sheet1", index=False)
            writer.save()
            fp.seek(0)
            self.s3.put_object(
                Body=fp.read(),
                Bucket=bucket,
                Key=send,
            )
        return send
