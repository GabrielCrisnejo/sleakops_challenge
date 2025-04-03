FROM python:3.12.2-slim

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install cron, rsyslog and timezone data
RUN apt-get update && \
    apt-get install -y --no-install-recommends cron rsyslog tzdata && \
    rm -rf /var/lib/apt/lists/*

# Configure timezone
ENV TZ=America/Argentina/Cordoba
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && \
    echo $TZ > /etc/timezone

# Configure rsyslog for cron logs
RUN echo 'cron.* /proc/1/fd/1' > /etc/rsyslog.d/cron.conf && \
    echo 'module(load="imuxsock")' >> /etc/rsyslog.conf && \
    echo 'module(load="imklog")' >> /etc/rsyslog.conf

# Copy application code
COPY . .

# Setup cron job
COPY src/scheduler/cronjob /etc/cron.d/pricing-cron
RUN chmod 0644 /etc/cron.d/pricing-cron && \
    touch /var/log/cron.log

# Create logs directory (added this improvement)
RUN mkdir -p /app/logs

# Startup command
CMD ["/bin/sh", "-c", "rsyslogd && cron && tail -f /var/log/cron.log /app/logs/logger.log"]