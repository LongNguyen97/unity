FROM python:3.8
ENV PYTHONUNBUFFERED 1
ENV PATH /tmp/.local/bin:$PATH

COPY . /code
RUN adduser --uid 1000 --disabled-password --gecos '' devuser
RUN chown -R devuser:devuser code/

USER devuser
RUN pip install -r /code/requirements.txt
WORKDIR /code