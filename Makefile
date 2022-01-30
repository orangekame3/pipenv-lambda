.PHONY: clean zip  delete cretae update invoke log test bucket download json
PROJECT_DIR=$(shell pwd)
DEPLOY_PACKAGES_DIR=deploy-packages

clean:
	rm -rf ./bin/*

zip:clean
	pipenv run mypy
	pipenv run pytest
	pipenv lock -r >requirements.txt
	pipenv run pip install -r requirements.txt --target $(DEPLOY_PACKAGES_DIR)
	@echo "Project Location: $(PROJECT_DIR)"
	@echo "Library Location: $(DEPLOY_PACKAGES_DIR)"
	cd $(DEPLOY_PACKAGES_DIR) && rm -rf __pycache__ && zip -r $(PROJECT_DIR)/bin/lambda.zip *
	cd $(PROJECT_DIR) && zip -g ./bin/lambda.zip lambda.py model.py
	find ./bin/lambda.zip
	cd $(DEPLOY_PACKAGES_DIR) && rm -r *

delete:
	aws --endpoint-url=http://localhost:4566 \
    --region ap-northeast-1 --profile local lambda delete-function \
    --function-name=pipenv-lambda
	
create:
	aws lambda create-function \
    --function-name=pipenv-lambda \
    --runtime=python3.9 \
    --role=DummyRole \
    --handler=lambda.lambda_handler \
    --zip-file fileb://./bin/lambda.zip \
	--region ap-northeast-1 \
    --endpoint-url=http://localhost:4566


update:
	aws lambda update-function-code \
    --function-name=pipenv-lambda \
    --zip-file fileb://./bin/lambda.zip \
	--region ap-northeast-1 \
    --endpoint-url=http://localhost:4566

invoke:
	aws lambda --endpoint-url=http://localhost:4566 invoke \
	--function-name pipenv-lambda \
	--region ap-northeast-1 \
	--payload '{ "input_obj": "test.json" }' \
	--cli-binary-format raw-in-base64-out \
	--profile local  result.log

log:
	cat result.log

test:
	pipenv shell "pytest -vv && exit"


bucket:
	aws s3 mb s3://test-bucket \
	--endpoint-url=http://localhost:4566 \
	--profile local

download:
	aws s3 --endpoint-url=http://localhost:4566 \
	cp s3://test-bucket/ ./result --exclude "*" \
	--include "*.xlsx" --recursive

json:
	python utils/utils.py 100