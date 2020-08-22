PYTHON_PATH := $(shell which python3)
ACTUAL_PATH := $(shell echo ${PWD})

setup:
	crontab -l | { cat; echo "*/5 * * * * $(PYTHON_PATH) $(ACTUAL_PATH)/dht_collector.py >> ~/cron.log 2>&1"; } | crontab -
	pip install -r requirements.txt
