FROM ubuntu:latest
WORKDIR /opt

ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install build-essential wget qtbase5-dev qtdeclarative5-dev nodejs npm git tree ninja-build gcc-multilib g++-multilib lib32stdc++-9-dev flex bison xz-utils ruby ruby-dev python3-requests binutils python3-setuptools python3-dev python3-pip libc6-dev libc6-dev-i386 bat -y
RUN gem install fpm -v 1.11.0 --no-document
RUN wget -q https://dl.google.com/android/repository/android-ndk-r25b-linux.zip && unzip android-ndk-r25b-linux.zip
ENV ANDROID_NDK_ROOT=/opt/android-ndk-r25b
RUN python3 -m pip install lief git+https://github.com/micahjmartin/Shipyard.git
RUN git clone --recurse-submodules https://github.com/frida/frida
WORKDIR /opt/frida
RUN git checkout tags/16.1.5
# Install newest node bc ubuntu node is old AF
RUN npm install -g n && n stable

#RUN make -f Makefile.toolchain.mk
#RUN make -f Makefile.sdk.mk
# Apply the patches to the source
COPY shipfile.py anti-anti-frida.py ./
RUN shipyard apply_code_patches
# Build
RUN make core-linux-x86_64
#RUN make core-android-x86_64
#RUN make core-android-arm64
#RUN make core-android-arm