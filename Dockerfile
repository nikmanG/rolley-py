# base image
FROM python:3.7.2-stretch

# copy all required stuff into container
COPY . /rolex
# May not to explicitly copy a .env here
WORKDIR /rolex

ENV TOKEN=NTI0OTQ5OTUyODkyMjM5ODc0.DwrD9A.ttRw8MvmPuhoWmv2xdXDsbOQAm8
# setup commands
RUN pip3 install -r requirements.txt
RUN python3 main.py
# CMD vim .env