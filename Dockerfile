FROM alpine

MAINTAINER shivanand@gramophone.co.in

RUN apt-get install -y git
RUN git clone https://github.com/cdqa-suite/cdQA-annotator
RUN sudo apt-get install curl
RUN curl -sL https://deb.nodesource.com/setup_12.x | sudo -E bash -
RUN sudo apt-get install nodejs
RUN cd cdQA-annotator
RUN sudo npm install -g @vue/cli
RUN sudo npm install -g @vue/cli-service-global
RUN sudo npm install --save bootstrap-vue
RUN sudo npm install --save bootstrap-vue/dist/bootstrap-vue.css
RUN npm install --save svg-progress-bar
RUN sudo npm audit fix --force

WORKDIR ./cdQA-annotator/src
 
EXPOSE 8080

CMD ["vue", " serve"]
