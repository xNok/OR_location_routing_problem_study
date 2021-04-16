FROM jupyter/scipy-notebook

LABEL Name=or Version=0.0.1

USER root

EXPOSE 8888

# Environment Variables
ENV JUPYTER_ENABLE_LAB=yes
ENV PROJ_LIB=/opt/conda/share/proj

# Install Cplex
ADD . /opt/cplex
RUN  chmod +x /opt/cplex/cplex_studio128.linux-x86-64.bin \
 && /opt/cplex/cplex_studio128.linux-x86-64.bin -f ./installer.properties

# Setup Cplex environnements
RUN cd /opt/ibm/ILOG/CPLEX_Studio128/python \
 && python setup.py install \
 && jupyter labextension install @jupyterlab/github

RUN conda install -y pymongo \
 && conda install -y basemap

 # Collabortory compatibility
 #&& pip install jupyter_http_over_ws \
 #&& jupyter serverextension enable --py jupyter_http_over_ws \
 #&& jupyter notebook --NotebookApp.allow_origin='https://colab.research.google.com' --port=8889 --allow-root

 # Github extention
 # jupyter labextension install @jupyterlab/github
 # pip install jupyterlab_github
 # jupyter serverextension enable --sys-prefix jupyterlab_github

 # Git extention
 # jupyter labextension install @jupyterlab/git
 # pip install jupyterlab-git
 # jupyter serverextension enable --py jupyterlab_git
