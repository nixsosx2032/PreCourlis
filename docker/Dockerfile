# Might be replaced by qgis/qgis:3.10
FROM camptocamp/qgis-server:3.10 as test

RUN pip3 install \
    pytest==5.4.1 \
    pytest-cov \
    pydevd

RUN mkdir -p /app
WORKDIR /app

ENV DISPLAY=:99
RUN mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix
COPY /docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["pytest"]
