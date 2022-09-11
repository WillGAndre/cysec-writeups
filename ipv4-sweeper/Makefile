.PHONY : deps run
all: deps run

# apt-get install -y libgirepository1.0-dev && apt-get install -y iputils-ping && apt-get install -y net-tools
deps:
	python3 -m pip install -r requirements.txt

run:
	python3 subnet_scan.py