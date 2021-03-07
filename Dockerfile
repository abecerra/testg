FROM python:3.9.2-alpine

LABEL APP="genesuggester"
LABEL APP_REPOSITORY="https://github.com/abecerra/genesuggester"

RUN adduser -D flaskuser
WORKDIR /home/flaskuser

#ENV TIMEZONE Europe/Paris

# Installing packages 
RUN apk add --no-cache mysql
RUN addgroup mysql mysql

# Work path
#WORKDIR /scripts

# Copy
COPY app.py app.py
COPY dbhandler.py dbhandler.py 
COPY test-dbhandler.py test-dbhandler.py 
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

#RUN su - flaskuser -c "python3 test-dbhandler.py"


# Creating the persistent volume
#VOLUME [ "/var/lib/mysql" ]

EXPOSE 5000
#ENTRYPOINT [ "python3 /home/flaskuser/app.py" ]
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]
