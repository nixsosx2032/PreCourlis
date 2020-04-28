# Might be replaced by qgis/qgis:3.10
#FROM camptocamp/qgis-server:3.4 as test
FROM qgis/qgis:release-3_10 as test

RUN apt update \
     && apt remove -y python3-coverage \
     && apt install -y \
        python3-venv \
        vim

RUN pip3 install \
    black \
    coverage \
    flake8 \
    nose \
    pydevd \
    pytest \
    pytest-cov

RUN mkdir -p /app /home/user && chmod 777 /home/user
WORKDIR /app

ENV DISPLAY=:99 \
    HOME=/home/user

RUN mkdir -p /tmp/.X11-unix && chmod 1777 /tmp/.X11-unix
COPY /docker-entrypoint.sh /
ENTRYPOINT ["/docker-entrypoint.sh"]

CMD ["pytest"]
