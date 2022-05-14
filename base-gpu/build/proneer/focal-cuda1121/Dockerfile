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
        org.label-schema.docker.dockerfile="/Dockerfile.cuda11-2-1.devel.cudnn8" \
        org.label-schema.name="Base Ubuntu 20.04 CUDA 11.2 Update 1 Development Image with Cudnn8" \
        org.label-schema.url="https://www.proneer.co"
ENV \
    USER_GID=0 \
    DEBIAN_FRONTEND=noninteractive
ENV \
    CUDA="11.2" \
    CUDNN_VERSION="8.1.0.77"
LABEL com.nvidia.cudnn.version="${CUDNN_VERSION}"
RUN \
    apt-get update \
    && apt-get install -y --no-install-recommends \
        libcudnn8=$CUDNN_VERSION-1+cuda$CUDA \
        libcudnn8-dev=$CUDNN_VERSION-1+cuda$CUDA \
    && apt-mark hold \
        libcudnn8 \
    # Cleanup - cannot use cleanup script here, otherwise too much is removed
    && apt-get clean \
    && rm -rf $HOME/.cache/* \
    && rm -rf /tmp/* \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /root
CMD nvidia-smi
