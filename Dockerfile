FROM python:3.12.2-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Instalar cron, rsyslog y tzdata (para la zona horaria)
RUN apt-get update && \
    apt-get install -y cron rsyslog tzdata && \
    rm -rf /var/lib/apt/lists/*

# Configurar la zona horaria
ENV TZ=America/Argentina/Cordoba 
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# Configurar rsyslog para redirigir logs de cron
RUN echo 'cron.* /proc/1/fd/1' > /etc/rsyslog.d/cron.conf && \
    echo 'module(load="imuxsock")' >> /etc/rsyslog.conf && \
    echo 'module(load="imklog")' >> /etc/rsyslog.conf

# Copiar todo el proyecto
COPY . .

# Configurar CRON
COPY src/scheduler/cronjob /etc/cron.d/pricing-cron
RUN chmod 0644 /etc/cron.d/pricing-cron && \
    touch /var/log/cron.log

# Comando para iniciar servicios
CMD ["/bin/sh", "-c", "rsyslogd && cron && tail -f /var/log/cron.log /app/logs/logger.log"]