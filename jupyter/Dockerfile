FROM jupyter/scipy-notebook:latest

USER root

RUN apt-get update && apt-get install -y \
    build-essential \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

USER $NB_UID

COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN pip install --no-cache-dir \
    jupyterlab \
    ipywidgets \
    matplotlib \
    seaborn \
    plotly

WORKDIR /home/jovyan

EXPOSE 8888

CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token='zenith'"]
