# base image
FROM python:3.11.7-alpine3.18


# environment variable
ENV APP /Optima_Yuli
ENV LOGNAME Neo


# working directory 
WORKDIR $APP


# copy our project from directory where dockerfile is to the actual working directory
COPY . .

# building dependencies
RUN pip install -r requirements.txt
RUN pip install .


ENTRYPOINT ["optima"]