FROM jasonrivers/nagios:latest
USER root
COPY portfolio.cfg /opt/nagios/etc/objects/portfolio.cfg
RUN grep -q "portfolio.cfg" /opt/nagios/etc/nagios.cfg \
    || echo "cfg_file=/opt/nagios/etc/objects/portfolio.cfg" >> /opt/nagios/etc/nagios.cfg
