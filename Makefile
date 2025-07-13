.PHONY: protos clean

CONTAINER_NAME := vehicle_telematics

all: edge.tar.gz

protos:
	python3 -m grpc_tools.protoc -I=../hub-sdk/protos --python_out=. --pyi_out=. --grpc_python_out=. ../hub-sdk/protos/edgehub/v3/*.proto

docker.tar: Dockerfile protos
	docker build --platform=linux/arm64 -f Dockerfile . -t ${CONTAINER_NAME}
	docker save -o docker.tar ${CONTAINER_NAME}

edge.tar.gz: docker.tar edge.json
	tar -czvf edge.tar.gz docker.tar edge.json

clean:
	rm -rf docker.tar edge.tar.gz edgehub
