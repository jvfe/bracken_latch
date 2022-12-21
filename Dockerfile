FROM 812206152185.dkr.ecr.us-west-2.amazonaws.com/latch-base:6839-main

RUN apt-get update &&\
    apt-get install -y curl

# Get Bracken
RUN curl -L \
    https://github.com/jenniferlu717/Bracken/archive/refs/tags/v2.8.tar.gz \
    -o bracken.tar.gz &&\
    tar -xvf bracken.tar.gz &&\
    cd Bracken-2.8 &&\
    sh install_bracken.sh

# STOP HERE:
# The following lines are needed to ensure your build environement works
# correctly with latch.
RUN python3 -m pip install --upgrade latch
COPY wf /root/wf
ARG tag
ENV FLYTE_INTERNAL_IMAGE $tag
WORKDIR /root
