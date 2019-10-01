FROM tiangolo/uwsgi-nginx:python3.7-alpine3.7
FROM continuumio/miniconda3

ADD environment.yml /tmp/environment.yml
RUN conda env create -f /tmp/environment.yml


ENV LISTEN_PORT=8000
EXPOSE 8000

# Indicate where uwsgi.ini lives
ENV UWSGI_INI uwsgi.ini

# Tell nginx where static files live (as typically collected using Django's
# collectstatic command.
ENV STATIC_URL /app/static_collected

# Copy the app files to a folder and run it from there
WORKDIR /app
ADD . /app

RUN easy_install pip
RUN pip install django
RUN pip install reportlab
#RUN pip install requests
# Make app folder writable for the sake of db.sqlite3, and make that file also writable.
RUN chmod g+w /app
RUN chmod g+w /app/db.sqlite3

# Make sure dependencies are installed
RUN echo "source activate $(head -1 /tmp/environment.yml | cut -d' ' -f2)" > ~/.bashrc
ENV PATH /opt/conda/envs/$(head -1 /tmp/environment.yml | cut -d' ' -f2)/bin:$PATH
#CMD [ "source activate myDjango" ]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]#, "8000"]