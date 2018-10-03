FROM python:3.6.6

RUN pip install --no-cache-dir \
  kubernetes requests

COPY ./job_killer.py /tmp/job_killer.py

ENTRYPOINT ["python", "-u", "/tmp/job_killer.py"]