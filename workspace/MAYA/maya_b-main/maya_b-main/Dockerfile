FROM python:3.12.7-slim
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=UTF-8
ENV PATH /home/sofia/.local/bin:$PATH
ENV TZ America/Mexico_City
ENV HOME /home/sofia
ENV APP_HOME /home/sofia/backend
ENV LOG_LEVEL debug
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone && \
    useradd -ms /bin/bash sofia && mkdir /home/sofia/backend
WORKDIR $APP_HOME
COPY . $APP_HOME
USER sofia
RUN python -m pip install --upgrade pip && python -m pip install --no-cache-dir -r requirements.txt
CMD uvicorn main:app --host 0.0.0.0 --port 5000 --log-level $LOG_LEVEL
EXPOSE 5000