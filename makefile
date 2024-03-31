download_model:
	poetry run python3 scripts/download_model.py

lab_url:
	firefox $(shell docker logs parser_lab 2>&1 | grep 'http://127.0.0.1:8081/lab?token=' | tail -n 1)


mongourl:
	docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' mongodb

detectorurl:
	docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' detector

dc_dev:
	docker compose -f docker-compose-dev.yml up -d
