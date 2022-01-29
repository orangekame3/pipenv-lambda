import pytest
from model import Handler
import pandas as pd


@pytest.fixture
def handler():
    return Handler(
        event={},
        context={},
        s3="",
    )


@pytest.mark.parametrize(
    "input_dict,want_dict",
    [
        (
            [
                {
                    "会員番号": "000",
                    "名前": "椎名 米子",
                    "会員ランク": 1,
                    "ポイント": 45,
                    "タイムスタンプ": "2021-07-14",
                },
                {
                    "会員番号": "001",
                    "名前": "広島 たくみ",
                    "会員ランク": 4,
                    "ポイント": 39,
                    "タイムスタンプ": "2021-12-17",
                },
                {
                    "会員番号": "002",
                    "名前": "大嶺 順子",
                    "会員ランク": 2,
                    "ポイント": 27,
                    "タイムスタンプ": "2021-09-23",
                },
            ],
            [
                {
                    "会員番号": "000",
                    "名前": "椎名 米子",
                    "会員ランク": 1,
                    "ポイント": 45,
                    "タイムスタンプ": "2021-07-14",
                    "ボーナスポイント": 45,
                },
                {
                    "会員番号": "001",
                    "名前": "広島 たくみ",
                    "会員ランク": 4,
                    "ポイント": 39,
                    "タイムスタンプ": "2021-12-17",
                    "ボーナスポイント": 48.75,
                },
                {
                    "会員番号": "002",
                    "名前": "大嶺 順子",
                    "会員ランク": 2,
                    "ポイント": 27,
                    "タイムスタンプ": "2021-09-23",
                    "ボーナスポイント": 27,
                },
            ],
        ),
    ],
)
def test_process(handler, input_dict, want_dict):
    json_dict = pd.DataFrame.from_dict(input_dict)
    got = handler.process(json_dict).sort_index(axis=1, ascending=False)
    want = pd.DataFrame.from_dict(want_dict).sort_index(axis=1, ascending=False)
    pd.testing.assert_frame_equal(got, want)
