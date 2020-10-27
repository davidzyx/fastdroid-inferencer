FROM python:3.7-alpine

RUN apk update && \
    apk upgrade && \
    apk add bash openjdk8 git && \
    rm -rf /var/cache/apk/*

WORKDIR /root
RUN wget https://raw.githubusercontent.com/iBotPeaches/Apktool/master/scripts/linux/apktool && \
    chmod +x apktool && \
    mv apktool /usr/local/bin/

RUN git clone git://github.com/iBotPeaches/Apktool.git --progress --verbose && \
    cd Apktool && \
    ./gradlew build shadowJar && \
    mv ./brut.apktool/apktool-cli/build/libs/apktool-cli-all.jar /usr/local/bin/apktool.jar && \
    chmod +x /usr/local/bin/apktool && \
    rm -rf /root/Apktool && \
    rm -rf /root/.gradle
