FROM python:3.7-alpine
COPY . /src
WORKDIR /src
RUN apk add --no-cache libcurl
ENV PYCURL_SSL_LIBRARY=openssl

RUN apk add --no-cache --virtual .build-deps build-base curl-dev \
    && pip install pycurl \
    && apk del --no-cache --purge .build-deps \
    && rm -rf /var/cache/apk/*

#Uncomment just the next 2  lines to run your application in Docker container
EXPOSE 8080
CMD python Assignment1.py 8080


#Uncomment just the next line when you want to deploy your container on Heroku
#CMD python Assignment1.py $PORT