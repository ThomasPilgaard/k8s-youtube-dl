REDIS_IP:=$(shell docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' redis-test)

buildenv:
	docker build -t flaskapp -f webservice/Dockerfile . 
	docker build -t worker -f worker/Dockerfile .  

runflask:
	docker run -p 5000:5000 -e REDIS_PATH=redis://$(REDIS_IP):6379 -e YOUTUBE_QUEUE_NAME=youtube_queue flaskapp

runworker:
	docker run -e REDIS_PATH=redis://$(REDIS_IP):6379 -e YOUTUBE_QUEUE_NAME=youtube_queue worker

startredis:
	docker run --name "redis-test" -d -p 6379:6379 redis:alpine3.13
