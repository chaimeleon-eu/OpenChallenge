FROM python:3.9-slim

RUN groupadd -r user && useradd -m --no-log-init -r -g user user

RUN mkdir -p /opt/app /input /output \
    && chown user:user /opt/app /input /output

USER user
WORKDIR /opt/app

ENV PATH="/home/user/.local/bin:${PATH}"

RUN python -m pip install --user -U pip && python -m pip install --user pip-tools

RUN pip install evalutils lifelines

COPY --chown=user:user ground-truth /opt/app/ground-truth
COPY --chown=user:user evaluation.py /opt/app/

ENTRYPOINT [ "python", "-m", "evaluation" ]


