REDIS_IP:=$(shell docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' redis-test)

buildenv:
	docker build -t flaskapp -f webservice/Dockerfile . 
	docker build -t worker -f worker/Dockerfile .  

runflask:
	docker run -v "/home/thomas/Documents/kubernetes/k8s-youtube-dl/test":/root/test -p 5000:5000 -e REDIS_PATH=redis://$(REDIS_IP):6379 -e YOUTUBE_QUEUE_NAME=youtube_queue -e YOUTUBE_STORAGE_MOUNT_PATH=/root/test/ -e TZ=Europe/Copenhagen flaskapp

runworker:
	docker run -v "/home/thomas/Documents/kubernetes/k8s-youtube-dl/test":/root/test -e REDIS_PATH=redis://$(REDIS_IP):6379 -e YOUTUBE_QUEUE_NAME=youtube_queue -e ENABLE_DEBUG_LOG=1 -e YOUTUBE_STORAGE_MOUNT_PATH=/root/test/ -e TZ=Europe/Copenhagen worker

startredis:
	docker run --name "redis-test" -d -p 6379:6379 -e TZ=Europe/Copenhagen redis:alpine3.13
