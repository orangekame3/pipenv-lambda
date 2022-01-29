# pipenv-lambda

Pipenvを利用してLambdaの開発環境をセットアップするデモスクリプトです。

前提としているツール

* docker-compose
* pyenv(もしくはPython環境) 
* zipコマンドとmake コマンド
* aws-cli2


使用ツール
 * pipenv
 * pytest
 * mypy
 * localstack


## ディレクトリ構成

```bash
❯❯❯ tree
.
├── Makefile
├── Pipfile
├── Pipfile.lock
├── README.md
├── bin
│   └── lambda.zip
├── deploy-packages
├── docker-compose.yml
├── lambda.py
├── model.py
├── requirements.txt
├── result
│   └── test.xlsx
├── result.log
├── setup.cfg
├── src
├── tests
│   ├── __init__.py
│   └── test_model.py
└── utils
    ├── data
    │   └── sample_data.json
    └── utils.py

7 directories, 16 files
```