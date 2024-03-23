FROM python:3.10

## Install system dependencies for TA-Lib
#RUN apt-get update && \
#    apt-get install -y build-essential libz-dev libfreetype6-dev libopenjp2-7-dev
#
## Install TA-Lib
#WORKDIR /tmp
#RUN wget https://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
#    tar -xzf ta-lib-0.4.0-src.tar.gz && \
#    cd ta-lib/ && \
#    ./configure --build=x86_64-linux-gnu && \
#    make && \
#    make install && \
#    cd / && \
#    rm -rf /tmp/ta-lib*

WORKDIR /app
COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY .. .

CMD ["python", "trade_consumer.py"]
