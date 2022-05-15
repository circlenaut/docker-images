FROM ubuntu:20.04
MAINTAINER proneer <phillip@proneer.co>
LABEL \
    maintainer="proneer <phillip@proneer.co>" \
        org.label-schema.docker.dockerfile="/Dockerfile.focal.base" \
        org.label-schema.name="Base Ubuntu 20.04 Base Image" \
        org.label-schema.url="https://www.proneer.co"
ENV \
    USER_GID=0 \
    DEBIAN_FRONTEND=noninteractive
COPY scripts/clean-layer.sh  /usr/bin/clean-layer.sh
COPY scripts/fix-permissions.sh  /usr/bin/fix-permissions.sh
RUN \
    chmod a+rwx /usr/bin/clean-layer.sh && \
    chmod a+rwx /usr/bin/fix-permissions.sh
COPY sources-focal.list /etc/apt/sources.list
COPY apt.conf /etc/apt/apt.conf.d/proneer
RUN apt-get update && apt-get upgrade -y
RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        apt-utils \
        apt-transport-https \
        cmake \
        dialog \
        gcc \
        software-properties-common \
    # Cleanup
    && clean-layer.sh \
    && rm -rf /var/lib/apt/lists/* \
    # Fix permissions
    && fix-permissions.sh $HOME
RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        cron \
        dpkg-sig \
        gnupg-agent \
        gnupg2 \
        iproute2 \
		libffi7 \
        locales \
        openssl \
        sudo \
        time \
		tzdata \
        uuid-dev \
	# Set Ubuntu apt
	&& apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 6A755776 \
    # Cleanup
    && clean-layer.sh \
    && rm -rf /var/lib/apt/lists/* \
    # Fix permissions
    && fix-permissions.sh $HOME
ENV TZ="Etc/UTC"
RUN \
    ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
	&& dpkg-reconfigure locales tzdata
RUN locale-gen en_US.UTF-8
ENV \
    LANG=C.UTF-8 \
    LANGUAGE=C.UTF-8 \
    LC_ALL=C.UTF-8
RUN /usr/sbin/update-locale
ENV LANG="en_US.UTF-8" \
	LC_CTYPE="en_US.UTF-8" \
	LC_NUMERIC="en_US.UTF-8" \
	LC_TIME="en_US.UTF-8" \
	LC_COLLATE="en_US.UTF-8" \
	LC_MONETARY="en_US.UTF-8" \
	LC_MESSAGES="en_US.UTF-8" \
	LC_PAPER="en_US.UTF-8" \
	LC_NAME="en_US.UTF-8" \
	LC_ADDRESS="en_US.UTF-8" \
	LC_TELEPHONE="en_US.UTF-8" \
	LC_MEASUREMENT="en_US.UTF-8" \
	LC_IDENTIFICATION="en_US.UTF-8"
RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        wget \
        curl \
        git \
        libcurl4 \
        bzip2 \
        unzip \
        zip \
        g++ \
    # Cleanup
    && clean-layer.sh \
    && rm -rf /var/lib/apt/lists/* \
    # Fix permissions
    && fix-permissions.sh $HOME
RUN chmod a+x /usr/local/sbin/* && rm -fr /var/log/* /tmp/*
WORKDIR /root
FROM registry.dev.proneer.co/base:ubuntu20.04
MAINTAINER proneer <phillip@proneer.co>
LABEL \
    maintainer="proneer <phillip@proneer.co>" \
        org.label-schema.docker.dockerfile="/Dockerfile.cuda11-6-2" \
        org.label-schema.name="Base Ubuntu 20.04 CUDA 11.6 Update 2 Image" \
        org.label-schema.url="https://www.proneer.co"
ENV \
    USER_GID=0 \
    DEBIAN_FRONTEND=noninteractive
ENV \
    NVARCH="x86_64" \
    NVIDIA_REQUIRE_CUDA="cuda>=11.6 brand=tesla,driver>=418,driver<419 brand=tesla,driver>=440,driver<441 brand=tesla,driver>=450,driver<451 brand=tesla,driver>=460,driver<461 brand=tesla,driver>=470,driver<471 brand=unknown,driver>=470,driver<471 brand=nvidia,driver>=470,driver<471 brand=nvidiartx,driver>=470,driver<471 brand=quadrortx,driver>=470,driver<471"
RUN \
    apt-get update && apt-get install -y --no-install-recommends \
        gnupg2 curl ca-certificates \
    && apt-key adv --fetch-keys https://developer.download.nvidia.cn/compute/cuda/repos/ubuntu2004/${NVARCH}/3bf863cc.pub \
    && echo "deb https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/${NVARCH} /" > /etc/apt/sources.list.d/cuda.list \
    && rm -rf /var/lib/apt/lists/*
ENV \
    NV_CUDA_CUDART_VERSION="11.6.55-1" \
    NV_CUDA_COMPAT_PACKAGE="cuda-compat-11-6"
RUN \
    apt-get update && apt-get install -y --no-install-recommends \
        cuda-cudart-11-6=${NV_CUDA_CUDART_VERSION} \
        ${NV_CUDA_COMPAT_PACKAGE} \
    && ln -s cuda-11.6 /usr/local/cuda \
    # Cleanup - cannot use cleanup script here, otherwise too much is removed
    && apt-get clean \
    && rm -rf $HOME/.cache/* \
    && rm -rf /tmp/* \
    && rm -rf /var/lib/apt/lists/*
RUN \
    echo "/usr/local/nvidia/lib" >> /etc/ld.so.conf.d/nvidia.conf \
    && echo "/usr/local/nvidia/lib64" >> /etc/ld.so.conf.d/nvidia.conf
ENV \
    PATH=/usr/local/nvidia/bin:/usr/local/cuda/bin:${PATH} \
    LD_LIBRARY_PATH=/usr/local/nvidia/lib:/usr/local/nvidia/lib64
ENV \
    NVIDIA_VISIBLE_DEVICES=all \
    NVIDIA_DRIVER_CAPABILITIES=compute,utility
WORKDIR /root
FROM registry.dev.proneer.co/cuda:11.6.2-ubuntu20.04
MAINTAINER proneer <phillip@proneer.co>
LABEL \
    maintainer="proneer <phillip@proneer.co>" \
        org.label-schema.docker.dockerfile="/Dockerfile.cuda11-6-2.runtime" \
        org.label-schema.name="Base Ubuntu 20.04 Cuda 11.6 Update 2 Runtime Image" \
        org.label-schema.url="https://www.proneer.co"
ENV \
    USER_GID=0 \
    DEBIAN_FRONTEND=noninteractive
ENV \
    NV_CUDA_LIB_VERSION="11.6.2-1" \
    NV_NVTX_VERSION="11.6.124-1" \
    NV_LIBNPP_VERSION="11.6.3.124-1"
ENV \
    NV_LIBNPP_PACKAGE="libnpp-11-6=${NV_LIBNPP_VERSION}" \
    NV_LIBCUSPARSE_VERSION="11.7.2.124-1" \
    NV_LIBCUBLAS_PACKAGE_NAME="libcublas-11-6" \
    NV_LIBCUBLAS_VERSION="11.9.2.110-1"
ENV \
    NV_LIBCUBLAS_PACKAGE="${NV_LIBCUBLAS_PACKAGE_NAME}=${NV_LIBCUBLAS_VERSION}" \
    NV_LIBNCCL_PACKAGE_NAME="libnccl2" \
    NV_LIBNCCL_PACKAGE_VERSION="2.12.10-1" \
    NCCL_VERSION="2.12.10-1"
ENV \
    NV_LIBNCCL_PACKAGE="${NV_LIBNCCL_PACKAGE_NAME}=${NV_LIBNCCL_PACKAGE_VERSION}+cuda11.6"
RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        cuda-libraries-11-6=${NV_CUDA_LIB_VERSION} \
        ${NV_LIBNPP_PACKAGE} \
        cuda-nvtx-11-6=${NV_NVTX_VERSION} \
        libcusparse-11-6=${NV_LIBCUSPARSE_VERSION} \
        ${NV_LIBCUBLAS_PACKAGE} \
        ${NV_LIBNCCL_PACKAGE} \
    # apt from auto upgrading the cublas package. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
    && apt-mark hold \
        ${NV_LIBCUBLAS_PACKAGE_NAME} \
        ${NV_LIBNCCL_PACKAGE_NAME} \
    # Cleanup - cannot use cleanup script here, otherwise too much is removed
    && apt-get clean \
    && rm -rf $HOME/.cache/* \
    && rm -rf /tmp/* \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /root
FROM registry.dev.proneer.co/cuda:11.6.2-runtime-ubuntu20.04
MAINTAINER proneer <phillip@proneer.co>
LABEL \
    maintainer="proneer <phillip@proneer.co>" \
        org.label-schema.docker.dockerfile="/Dockerfile.cuda11-6-2.devel" \
        org.label-schema.name="Base Ubuntu 20.04 CUDA 11.6 Update 2 Development Image" \
        org.label-schema.url="https://www.proneer.co"
ENV \
    USER_GID=0 \
    DEBIAN_FRONTEND=noninteractive
ENV \
    NV_CUDA_LIB_VERSION="11.6.2-1" \
    NV_CUDA_CUDART_DEV_VERSION="11.6.55-1" \
    NV_NVML_DEV_VERSION="11.6.55-1" \
    NV_LIBCUSPARSE_DEV_VERSION="11.7.2.124-1" \
    NV_LIBNPP_DEV_VERSION="11.6.3.124-1"
ENV \
    NV_LIBNPP_DEV_PACKAGE="libnpp-dev-11-6=${NV_LIBNPP_DEV_VERSION}" \
    NV_LIBCUBLAS_DEV_PACKAGE_NAME="libcublas-dev-11-6" \
    NV_LIBCUBLAS_DEV_VERSION="11.9.2.110-1"
ENV \
    NV_LIBCUBLAS_DEV_PACKAGE="${NV_LIBCUBLAS_DEV_PACKAGE_NAME}=${NV_LIBCUBLAS_DEV_VERSION}" \
    NV_NVPROF_VERSION="11.6.124-1"
ENV \
    NV_LIBNCCL_DEV_PACKAGE_NAME="libnccl-dev" \
    NV_LIBNCCL_DEV_PACKAGE_VERSION="2.12.10-1" \
    NCCL_VERSION="2.12.10-1"
ENV \
    NV_LIBNCCL_DEV_PACKAGE="${NV_LIBNCCL_DEV_PACKAGE_NAME}=${NV_LIBNCCL_DEV_PACKAGE_VERSION}+cuda11.6"
RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        libtinfo5 libncursesw5 \
        cuda-cudart-dev-11-6=${NV_CUDA_CUDART_DEV_VERSION} \
        cuda-command-line-tools-11-6=${NV_CUDA_LIB_VERSION} \
        cuda-minimal-build-11-6=${NV_CUDA_LIB_VERSION} \
        cuda-libraries-dev-11-6=${NV_CUDA_LIB_VERSION} \
        cuda-nvml-dev-11-6=${NV_NVML_DEV_VERSION} \
        cuda-nvprof-11-6=${NV_NVPROF_VERSION} \
        ${NV_LIBNPP_DEV_PACKAGE} \
        libcusparse-dev-11-6=${NV_LIBCUSPARSE_DEV_VERSION} \
        ${NV_LIBCUBLAS_DEV_PACKAGE} \
        ${NV_LIBNCCL_DEV_PACKAGE} \
    # apt from auto upgrading the cublas package. See https://gitlab.com/nvidia/container-images/cuda/-/issues/88
    && apt-mark hold \
        ${NV_LIBCUBLAS_DEV_PACKAGE_NAME} \
        ${NV_LIBNCCL_DEV_PACKAGE_NAME} \
    # Cleanup - cannot use cleanup script here, otherwise too much is removed
    && apt-get clean \
    && rm -rf $HOME/.cache/* \
    && rm -rf /tmp/* \
    && rm -rf /var/lib/apt/lists/*
ENV \
    LIBRARY_PATH=/usr/local/cuda/lib64/stubs
RUN \
    nvcc --version
WORKDIR /root
FROM registry.dev.proneer.co/cuda:11.6.2-devel-ubuntu20.04
MAINTAINER proneer <phillip@proneer.co>
LABEL \
    maintainer="proneer <phillip@proneer.co>" \
        org.label-schema.docker.dockerfile="/Dockerfile.cuda11-6-2.devel.cudnn8" \
        org.label-schema.name="Base Ubuntu 20.04 CUDA 11.6 Update 2 Development Image with Cudnn8" \
        org.label-schema.url="https://www.proneer.co"
ENV \
    USER_GID=0 \
    DEBIAN_FRONTEND=noninteractive
ENV \
    NV_CUDNN_VERSION="8.4.0.27"
ENV \
    NV_CUDNN_PACKAGE="libcudnn8=$NV_CUDNN_VERSION-1+cuda11.6" \
    NV_CUDNN_PACKAGE_DEV="libcudnn8-dev=$NV_CUDNN_VERSION-1+cuda11.6" \
    NV_CUDNN_PACKAGE_NAME="libcudnn8"
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"
RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        ${NV_CUDNN_PACKAGE} \
        ${NV_CUDNN_PACKAGE_DEV} \
    && apt-mark hold \
        libcudnn8 \
    # Cleanup - cannot use cleanup script here, otherwise too much is removed
    && apt-get clean \
    && rm -rf $HOME/.cache/* \
    && rm -rf /tmp/* \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /root
FROM registry.dev.proneer.co/cuda:11.6.2-cudnn8-devel-ubuntu20.04
MAINTAINER proneer <phillip@proneer.co>
LABEL \
    maintainer="proneer <phillip@proneer.co>" \
        org.label-schema.docker.dockerfile="/Dockerfile.dev" \
        org.label-schema.name="Base development image" \
        org.label-schema.url="https://www.proneer.co"
USER root
ENV \
    USER_GID=0 \
    NB_USER="root" \
    DEBIAN_FRONTEND=noninteractive \
    RESOURCES_PATH="/resources" \
    SCRIPTS_PATH="/scripts" \
    APPS_PATH="/apps" \
    DATA_PATH="/data"
RUN \
    mkdir $RESOURCES_PATH && chmod a+rwx $RESOURCES_PATH \
    && mkdir $SCRIPTS_PATH && chmod a+rwx $SCRIPTS_PATH \
    && mkdir $APPS_PATH && chmod a+rwx $APPS_PATH \
    && mkdir $DATA_PATH && chmod a+rw $DATA_PATH
RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-pip \
        python3-venv \
        python3-dev \
        python3-setuptools \
        python3-testresources \
    # Cleanup
    && clean-layer.sh \
    && rm -rf /var/lib/apt/lists/* \
    # Fix permissions
    && fix-permissions.sh $HOME
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ="Etc/UTC"
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone
RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        tzdata \
        jq \
        libssl-dev \
        libgdbm-dev \
        libncurses5-dev \
        libncursesw5-dev \
        # Shells
        csh \
        zsh \
        fish \
        # Editors
        nano \
        emacs \
        vim \
        # System tools
        tuptime \
        ncdu \
        iotop \
        psmisc \
        lsof \
        # Terminal tools
        htop \
        screen \
        tmate \
        tmux \
        less \
        rename \
        whereami \
        xclip \
        clinfo \
        xmlstarlet \
        parallel \
        yara \
        rpl \
        locate \
        bash-completion \
        expect \
        catimg \
        autojump \
        lynx \
        # Net tools
        net-tools \
        dnsutils \
        iputils-ping \
        iputils-tracepath \
        netcat \
        rsync \
        nmap \
        iftop \
        # Cuda tools
        nvtop \
        # Build libs
        build-essential \
        checkinstall \
        make \
        #cmake \
        cmake-curses-gui \
        pkg-config \
        yasm \
        swig \
        libicu-dev \
        # Net libs
        libsodium-dev \
        # Sec libs
        libargon2-0-dev \
        # Version control
        subversion \
        jed \
        git-flow \
        git-extras \
        # Visualization
        graphviz \
        # DB libs
        sqlite3 \
        libhiredis-dev \
        libpq-dev \
        libsqlite3-dev \
        unixodbc unixodbc-dev \
        libmariadb-dev \
        libmariadbclient-dev \
        #libmysqlclient-dev \
        # Required by Pyenv
        libreadline-dev \
        libedit-dev \
        xz-utils \
        gawk \
        # Image/Media support
        imagemagick \
        libtiff-dev \
        libjpeg8-dev \
        libjpeg-dev \
        libpng-dev \
        libglib2.0-0 \
        libxext6 \
        libsm6 \
        libxext-dev \
        libxrender1 \
        libzmq3-dev \
        libavcodec-dev \
        libavformat-dev \
        libswscale-dev \
        libdc1394-22-dev \
        libxine2-dev \
        libv4l-dev \
        libgstreamer1.0-dev \
        libgstreamer-plugins-base1.0-dev \
        libfaac-dev \
        libmp3lame-dev \
        libtheora-dev \
        libvorbis-dev \
        libxvidcore-dev \
        libopencore-amrnb-dev \
        libopencore-amrwb-dev \
        libavresample-dev \
        x264 \
        v4l-utils \
        libgphoto2-dev \
        # GUI libs
        libgtk2.0-dev \
        # Protobuffer support
        protobuf-compiler \
        libprotobuf-dev \
        libprotoc-dev \
        autoconf \
        automake \
        libtool \
        cmake  \
        fonts-liberation \
        google-perftools \
        # C++
        libtbb-dev \
        qt5-default \
        libgflags-dev \
        libeigen3-dev \
        # Fortran
        gfortran \
        # Go
        libgoogle-glog-dev \
        # Math libs
        libatlas-base-dev \
        # Data libs
        libhdf5-dev \
        # Doc libs
        doxygen \
        # Compression libs
        gzip \
        lzop \
        libarchive-tools \
        zlibc \
        p7zip-full \
        unp \
        libbz2-dev \
        liblzma-dev \
        zlib1g-dev \
        libonig-dev \
        libzip-dev \
    # Cleanup
    && clean-layer.sh \
    # Fix permissions
    && fix-permissions.sh $HOME
RUN \
    echo "**** installing node.js dev environment ****" \
    apt-get update \
    # https://nodejs.org/en/about/releases/ use even numbered releases, i.e. LTS versions
    #&& curl -sL https://deb.nodesource.com/setup_14.x | sudo -E bash - \
    && curl -sL https://deb.nodesource.com/setup_lts.x | sudo -E bash - \
    && apt-get install -y nodejs \
    # As conda is first in path, the commands 'node' and 'npm' reference to the version of conda.
    # Replace those versions with the newly installed versions of node
    #&& rm -f /opt/conda/bin/node && ln -s /usr/bin/node /opt/conda/bin/node \
    #&& rm -f /opt/conda/bin/npm && ln -s /usr/bin/npm /opt/conda/bin/npm \
    # Fix permissions
    && chmod a+rwx /usr/bin/node \
    && chmod a+rwx /usr/bin/npm \
    # Fix node versions - put into own dir and before conda:
    && mkdir -p /opt/node/bin \
    && ln -s /usr/bin/node /opt/node/bin/node \
    && ln -s /usr/bin/npm /opt/node/bin/npm \
    # Install YARN
    && curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add - \
    && echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends yarn \
    # Install typescript
    && /usr/bin/npm install -g typescript \
    # Install webpack - 32 MB
    && /usr/bin/npm install -g webpack \
    # Install node-gyp
    && /usr/bin/npm install -g node-gyp
    # Cleanup
    #clean-layer.sh # throws error
ENV PATH="/opt/node/bin:$PATH"
RUN \
    echo "**** installing java dev environment ****" \
    apt-get update \
    && apt-get install -y --no-install-recommends openjdk-11-jdk maven scala \
    # Cleanup
    && clean-layer.sh
ENV JAVA_HOME="/usr/lib/jvm/java-11-openjdk-amd64"
RUN \
    echo "**** installing golang dev environment ****" \
    && mkdir $RESOURCES_PATH"/golang" \
    && cd $RESOURCES_PATH"/golang" \
    && GO_VERSION=$(curl -sX GET https://go.dev/dl/ | grep -o '<span.*>.*linux-amd64.*</span>' | grep -oP '(?<=go).*(?=.linux)') \
    && wget --quiet https://dl.google.com/go/go$GO_VERSION.linux-amd64.tar.gz -O ~/go.tgz \
    && tar -C /usr/local -xzf ~/go.tgz \
    && rm ~/go.tgz \
    && echo "export PATH="/usr/local/go/bin:$PATH"" >> ~/.bashrc \
    # Cleanup
    && clean-layer.sh
RUN \
    rm -r $RESOURCES_PATH"/golang" \
    # Fix permissions \
    && fix-permissions.sh $HOME \
    # Cleanup
    && clean-layer.sh
ENV GOPATH="/go"
ENV PATH="$GOPATH/bin:/usr/local/go/bin:$PATH"
RUN mkdir -p "$GOPATH/src" "$GOPATH/bin" && chmod -R 777 "$GOPATH"
RUN \
    echo "**** installing Openresty web server ****" \
    && OPEN_RESTY_VERSION="1.19.9.1" \
    && mkdir $RESOURCES_PATH"/openresty" \
    && cd $RESOURCES_PATH"/openresty" \
    && apt-get update \
    && apt-get purge -y \
        nginx \
        nginx-common \
    # libpcre required, otherwise you get a 'the HTTP rewrite module requires the PCRE library' error
    # Install apache2-utils to generate user:password file for nginx.
    && apt-get install -y \
        libssl-dev \
        libpcre3 \
        libpcre3-dev \
        apache2-utils \
    && wget --no-verbose https://openresty.org/download/openresty-$OPEN_RESTY_VERSION.tar.gz  -O ./openresty.tar.gz \
    && tar xfz ./openresty.tar.gz \
    && rm ./openresty.tar.gz \
    && cd ./openresty-$OPEN_RESTY_VERSION/ \
    # Surpress output - if there is a problem remove  > /dev/null
    && ./configure --with-http_stub_status_module --with-http_sub_module > /dev/null \
    && make -j2 > /dev/null \
    && make install > /dev/null \
    # create log dir and file - otherwise openresty will throw an error
    && mkdir -p /var/log/nginx/ \
    && touch /var/log/nginx/upstream.log \
    && cd $RESOURCES_PATH \
    && rm -r $RESOURCES_PATH"/openresty" \
    # Cleanup
    && clean-layer.sh \
    # Fix permissions
    && fix-permissions.sh $HOME
ENV PATH="/usr/local/openresty/nginx/sbin:$PATH"
RUN \
    echo "**** installing xcaddy builder ****" \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
        libnss3-tools \
    && go install github.com/caddyserver/xcaddy/cmd/xcaddy@latest \
    # Cleanup
    && clean-layer.sh
RUN \
    echo "**** building caddy ****" \
    && CGO_ENABLED=0 GOARCH=amd64 GOOS=linux \
        xcaddy build \
        --with github.com/caddy-dns/gandi \
        --with github.com/caddy-dns/cloudflare \
        --with github.com/caddy-dns/dnspod \
        --with github.com/caddy-dns/duckdns \
        --with github.com/greenpau/caddy-security \
        --with github.com/greenpau/caddy-trace \
        --output $RESOURCES_PATH"/caddy" \
    && cp $RESOURCES_PATH"/caddy" /usr/bin/caddy \
    && rm -r $RESOURCES_PATH"/caddy" \
    # Cleanup
    && clean-layer.sh \
    && fix-permissions.sh $HOME
RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        openssh-client \
        openssh-server \
        # SSLH for SSH + HTTP(s) Multiplexing
        sslh \
        # SSH Tooling
        autossh \
        mussh && \
    chmod go-w $HOME \
    && mkdir -p $HOME/.ssh/ \
    # create empty config file if not exists
    touch $HOME/.ssh/config \
    && chown -R $NB_USER:users $HOME/.ssh \
    && chmod 700 $HOME/.ssh \
    && printenv >> $HOME/.ssh/environment \
    && chmod -R a+rwx /usr/local/bin/ \
    # Cleanup
    && clean-layer.sh \
    # Fix permissions
    && fix-permissions.sh $HOME
RUN git clone https://github.com/pyenv/pyenv.git $RESOURCES_PATH/.pyenv
RUN git clone https://github.com/pyenv/pyenv-virtualenv.git $RESOURCES_PATH/.pyenv/plugins/pyenv-virtualenv
RUN git clone https://github.com/pyenv/pyenv-doctor.git $RESOURCES_PATH/plugins/pyenv-doctor
RUN git clone https://github.com/pyenv/pyenv-update.git $RESOURCES_PATH/plugins/pyenv-update
RUN git clone https://github.com/pyenv/pyenv-which-ext.git $RESOURCES_PATH/plugins/pyenv-which-ext
ENV \
    PATH="$RESOURCES_PATH/.pyenv/shims:$RESOURCES_PATH/.pyenv/bin:$PATH" \
    PYENV_ROOT="$RESOURCES_PATH/.pyenv"
ENV \
    PIPX_HOME="/usr/local/pipx" \
    PIPX_BIN_DIR="/usr/local/pipx/bin" \
    PATH="/usr/local/pipx/bin:$PATH"
RUN \
    mkdir -p "$PIPX_HOME" "$PIPX_BIN_DIR" && chmod -R 777 "$PIPX_HOME" \
    && pip3 install \
        pipx \
        pip-api \
        wheel \
        ipython \
        psutil \
        python-crontab \
        pyyaml \
        yamale \
        typing \
        docker \
        ansible \
        passlib \
        bcrypt \
        watchgod \
        coloredlogs \
    # Cleanup
    && clean-layer.sh
RUN \
    pipx install \
        httpie --force \
    # Cleanup
    && clean-layer.sh
RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends rsyslog \
    # Create sshd run directory - required for starting process via supervisor
    && mkdir -p /var/run/sshd && chmod 400 /var/run/sshd \
    # Install rsyslog for syslog logging
    && pipx install --force supervisor \
    && pipx inject supervisor supervisor-stdout \
    # supervisor needs this logging path
    && mkdir -p /var/log/supervisor/ \
    # Cleanup
    && clean-layer.sh
RUN \
    echo "Defaults secure_path=$PATH" > /etc/sudoers.d/securepath \
    && chmod 0440 /etc/sudoers.d/securepath
WORKDIR /root
FROM registry.dev.proneer.co/dev:11.6.2-cudnn8-devel-ubuntu20.04
MAINTAINER proneer <phillip@proneer.co>
LABEL \
    maintainer="proneer <phillip@proneer.co>" \
        org.label-schema.docker.dockerfile="/Dockerfile.vscode" \
        org.label-schema.name="Development image loaded with Vscode, filebrowsers and various WebUI utilities" \
        org.label-schema.url="https://www.proneer.co"
USER root
ENV \
    DEBIAN_FRONTEND=noninteractive \
    RESOURCES_PATH="/resources" \
    SCRIPTS_PATH="/scripts" \
    APPS_PATH="/apps" \
    DATA_PATH="/data" \
    WORKSPACE_HOME="/workspace"
RUN \
    curl -fsSL https://code-server.dev/install.sh | bash \
    # Cleanup
    && clean-layer.sh
RUN \
    curl -fsSL https://raw.githubusercontent.com/filebrowser/get/master/get.sh | bash \
    # Cleanup
    && clean-layer.sh
RUN sed -i '/imklog/s/^/#/' /etc/rsyslog.conf
COPY scripts/__init__.py $SCRIPTS_PATH
COPY scripts/docker-entrypoint.py /
COPY scripts/functions.py $SCRIPTS_PATH
COPY scripts/run_workspace.py $SCRIPTS_PATH
COPY scripts/setup_ssh.py $SCRIPTS_PATH
COPY scripts/configure_user.py $SCRIPTS_PATH
COPY scripts/configure_cron.py $SCRIPTS_PATH
COPY scripts/backup_restore_config.py $SCRIPTS_PATH
COPY configs/supervisor/conf.d /etc/supervisor/conf.d/
COPY configs/supervisor/supervisord.conf /etc/supervisor/supervisord.conf
COPY scripts/conda_parser.py $SCRIPTS_PATH
COPY scripts/users_mod.py $SCRIPTS_PATH
COPY scripts/configure_ssh.py $SCRIPTS_PATH
COPY scripts/configure_zsh.py $SCRIPTS_PATH
COPY scripts/configure_vscode.py $SCRIPTS_PATH
COPY scripts/configure_filebrowser.py $SCRIPTS_PATH
COPY scripts/configure_caddy.py $SCRIPTS_PATH
COPY scripts/configure_app.py $SCRIPTS_PATH
COPY scripts/setup_conda_envs.py $SCRIPTS_PATH
COPY scripts/run_installers.py $SCRIPTS_PATH
COPY configs/users.ymal $SCRIPTS_PATH
ENTRYPOINT python /docker-entrypoint.py
