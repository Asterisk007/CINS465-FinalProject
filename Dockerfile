FROM continuumio/miniconda:latest
COPY environment.yml ./
RUN conda env create -f environment.yml
RUN echo "conda activate env" > ~/.bashrc
COPY . app
COPY run_server.sh ./
RUN chmod +x run_server.sh
ENV PATH /opt/conda/envs/env/bin:$PATH
EXPOSE 8000
ENTRYPOINT ["./run_server.sh"]
