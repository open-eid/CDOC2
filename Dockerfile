FROM python:3.8-buster

ENV NVM_DIR /usr/local/nvm
ENV NODE_VERSION 20.12.2
ENV PATH $NVM_DIR/versions/node/v$NODE_VERSION/bin:$PATH

COPY mkdocs_requirements.txt nvm-install.sh ./

RUN mkdir -p $NVM_DIR && \
    bash nvm-install.sh && . $NVM_DIR/nvm.sh && \
    nvm install $NODE_VERSION && npm install -g markdownlint-cli2 && \
    pip install -r mkdocs_requirements.txt
