# base image
FROM python:3.7.2-stretch

# copy all required stuff into container
COPY . /rolex
# May not to explicitly copy a .env here
WORKDIR /rolex

# setup commands
RUN pip3 install -r requirements.txt
CMD vim .env