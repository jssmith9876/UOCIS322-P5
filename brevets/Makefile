IMG = jordan-smith-cis322-4
CNT = jordan-smith-proj4
PORT = 5678

all: build run

build:
	docker build -t $(IMG) .

run:
	docker run --name $(CNT) -d -p $(PORT):5000 $(IMG)

start:
	docker start $(CNT)

stop:
	docker stop $(CNT)

clean:
	docker rm $(CNT)
	docker rmi -f $(IMG):latest
