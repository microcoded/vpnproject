FROM handsonsecurity/seed-ubuntu:large

RUN apt-get update && apt-get install -y python3-pip iperf3

COPY requirements.txt /requirements.txt
RUN pip3 install --no-cache-dir -r /requirements.txt
