FROM debian:12

RUN apt-get update && apt-get install -y \
    nginx \
    tor \
    openssh-server \
    curl \
    sed

RUN mkdir -p /var/run/sshd /root/.ssh && \
    mkdir -p /var/lib/tor/hidden_service && \
    chown -R debian-tor:debian-tor /var/lib/tor/hidden_service && \
    chmod 700 /var/lib/tor/hidden_service

RUN echo "root:root" | chpasswd

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY torrc /etc/tor/torrc
COPY sshd_config /etc/ssh/sshd_config
COPY index.html /var/www/html/index.html

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 80 4242

CMD ["/entrypoint.sh"]