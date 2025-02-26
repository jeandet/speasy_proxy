FROM fedora:36

ARG PORT=6543
ARG SPEASY=speasy

ENV SPEASY_CACHE_PATH=/data \
    SPEASY_CACHE_SIZE="20e9" \
    SPEASY_INDEX_PATH=/index \
    SPEASY_LOG_PATH=/log \
    SPEASY_PROXY="true" \
    SPEASY_PROXY_PREFIX="" \
    SPEASY_PROXY_URL="" \
    SPEASY_PROXY_LOG_LEVEL="WARN"\
    PORT=$PORT

RUN useradd speasy && mkdir -p $SPEASY_CACHE_PATH $SPEASY_INDEX_PATH \
    && dnf install -y git python3.11.x86_64 python3.11-devel.x86_64 libxslt-devel gcc g++ \
    && dnf clean all \
    && chown -R speasy $SPEASY_CACHE_PATH $SPEASY_INDEX_PATH \
    && mkdir -p $SPEASY_LOG_PATH/speasy \
    && chown -R speasy $SPEASY_LOG_PATH/speasy

COPY speasy_proxy/*.ini speasy_proxy/*.py speasy_proxy/*.txt /home/speasy/speasy_proxy/
COPY speasy_proxy/speasy_proxy /home/speasy/speasy_proxy/speasy_proxy
RUN chown -R speasy /home/speasy/speasy_proxy

USER speasy
WORKDIR /home/speasy

RUN cd speasy_proxy &&\
    python3.11 -m ensurepip &&\
    python3.11 -mpip install -U pip &&\
    python3.11 -mpip install -U . &&\
    python3.11 -mpip install -U $SPEASY

ADD speasy_proxy/docker/entry_point.sh /home/speasy/entry_point.sh

VOLUME $SPEASY_CACHE_PATH
VOLUME $SPEASY_LOG_PATH
VOLUME $SPEASY_INDEX_PATH
EXPOSE $PORT/tcp
CMD ["/home/speasy/entry_point.sh"]
