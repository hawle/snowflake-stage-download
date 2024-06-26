FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y curl git --no-install-recommends && \
    python3 -m pip install --no-cache-dir --upgrade pip

# Configure environments vars. Overriden by GitHub Actions
ENV INPUT_SNOWFLAKE_WAREHOUSE=
ENV INPUT_SNOWFLAKE_ACCOUNT=
ENV INPUT_SNOWFLAKE_USERNAME=
ENV INPUT_SNOWFLAKE_PASSWORD=
ENV INPUT_SNOWFLAKE_DATABASE=
ENV INPUT_SNOWFLAKE_SCHEMA=
ENV INPUT_SNOWFLAKE_STAGE_NAME=
ENV INPUT_LOCAL_DOWNLOAD_PATH=
ENV APP_DIR=/app

WORKDIR ${APP_DIR}

# setup python environ
COPY ./requirements.txt ${APP_DIR}
RUN pip install --no-cache-dir -r ${APP_DIR}/requirements.txt

# copy app files
COPY . .
# RUN useradd -ms /bin/bash toor && chown -R toor:toor /app
# USER toor
# command to run in container start
CMD python ${APP_DIR}/main.py