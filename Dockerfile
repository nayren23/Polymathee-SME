FROM python:3.10

WORKDIR /usr/src/app

#Set arguments
ARG DB_HOST
ARG DB_NAME
ARG DB_PORT
ARG DB_PWD
ARG DB_USER
ARG FRONT_END_URL
ARG FLASK_DEBUG
ARG FLASK_HOST
ARG FLASK_PORT
ARG CERTIFICATE_CRT_FOLDER
ARG CERTIFICATE_KEY_FOLDER

# Set environment variables, maybe for specific variables we can move them to the docker-compose file
ENV FRONT_END_URL='http://localhost:4200'
ENV FLASK_DEBUG='http://localhost:4200'
ENV FLASK_DEBUG='http://localhost:4200'
ENV FLASK_HOST='http://localhost:4200'
ENV FLASK_PORT='http://localhost:4200'

ENV DB_HOST=$DB_HOST \
    DB_NAME=$DB_NAME \
    DB_PORT=$DB_PORT \
    DB_PWD=$DB_PWD \
    DB_USER=$DB_USER \
    CERTIFICATE_CRT_FOLDER=$CERTIFICATE_CRT_FOLDER \
    CERTIFICATE_KEY_FOLDER=$CERTIFICATE_KEY_FOLDER 

# Copy pyproject.toml first to avoid reinstalling dependencies when code changes
COPY pyproject.toml . 

COPY . .

RUN pip install -e .

EXPOSE 5050

ENTRYPOINT [ "python3" ]

CMD ["polymathee_sme/rest_api.py"]