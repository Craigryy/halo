FROM alpine:latest

RUN adduser -D admin
USER admin


WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "flask", "run", "--host=0.0.0.0", "--port=5000"]