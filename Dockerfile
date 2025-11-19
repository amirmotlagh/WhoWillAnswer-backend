FROM python:3.12-alpine as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user -r requirements.txt

FROM python:3.12-alpine
WORKDIR /app
RUN apk add --no-cache pkgconfig gcc musl-dev mariadb-dev
RUN adduser -D myuser
USER myuser
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH
COPY app .
RUN mkdir -p /var/log/django/ && \
    touch /var/log/django/errors.log
RUN python manage.py collectstatic --noinput
EXPOSE 8000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health/ || exit 1
CMD ["", "", "", ""]