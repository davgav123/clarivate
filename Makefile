ENV=task_env

.PHONY: setup build install clean

setup:
	pyenv install --patch 3.6.8 < alignment.patch

build:
	pyenv virtualenv ${ENV}

install:
	source ~/.pyenv/versions/${ENV}/bin/activate && \
	pip install -r requirements.txt

clean:
	pyenv virtualenv-delete -f ${ENV}
