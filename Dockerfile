FROM python:3.11

ARG USERNAME=locust
ARG TEST_RUNNER_UID=1001
ARG TEST_RUNNER_GID=$TEST_RUNNER_UID

ENV PERF_DIR /opt/locust
ENV PERF_WORK_DIR ${PERF_DIR}/temp
ENV PERF_TESTS_DIR ${PERF_DIR}/tests
ENV PYTHONPATH ${PYTHONPATH}:${PERF_TESTS_DIR}
ENV TZ Europe/Helsinki

RUN groupadd --gid $TEST_RUNNER_GID $USERNAME \
    && useradd --uid $TEST_RUNNER_UID --gid $TEST_RUNNER_GID -m $USERNAME \
    && apt-get update \
    && apt-get install -y sudo \
    && echo $USERNAME ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/$USERNAME \
    && chmod 0440 /etc/sudoers.d/$USERNAME

RUN mkdir -p ${PERF_WORK_DIR} \
    && mkdir -p ${PERF_TESTS_DIR} \
    && chown -R ${TEST_RUNNER_UID}:${TEST_RUNNER_GID} ${PERF_DIR} \
    && chmod -R ugo+w ${PERF_DIR}

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo ${TZ} > /etc/timezone

WORKDIR ${PERF_WORK_DIR}

COPY requirements.txt requirements.txt

USER ${USERNAME}

ENV PATH="/home/${USERNAME}/.local/bin:${PATH}"

RUN pip3 install -r requirements.txt

WORKDIR ${PERF_TESTS_DIR}

CMD [ "locust -f locustfiles/login_and_auth.py" ]
