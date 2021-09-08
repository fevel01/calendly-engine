FROM registry.gitlab.com/nomnomdata/tools/nomnomdata-engine:v1.1.22 as builder

COPY requirements.txt /nomnom/requirements.txt
RUN pip wheel --wheel-dir /python_packages -r /nomnom/requirements.txt

FROM registry.gitlab.com/nomnomdata/tools/nomnomdata-engine:v1.1.22-slim

COPY --from=builder /python_packages /python_packages
RUN pip install --no-index --find-links /python_packages /python_packages/* && rm -rf /python_packages

WORKDIR /nomnom/

COPY pkg /nomnom/pkg/
COPY main.py /nomnom/main.py
CMD python main.py run
