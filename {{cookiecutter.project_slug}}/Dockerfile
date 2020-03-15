FROM golang:latest

LABEL maintainer="{{ cookiecutter.email }}"

ENV GO111MODULE=on

WORKDIR /app
COPY ./ /app

{% if cookiecutter.project_type == 'both' -%}
RUN CGO_ENABLED=0 GOOS=linux go build -o app "{{ cookiecutter.public_import_path }}/{{ cookiecutter.project_slug }}/cmd/{{ cookiecutter.project_slug }}"
{% elif cookiecutter.project_type == 'tool' -%}
RUN CGO_ENABLED=0 GOOS=linux go build -o app "{{ cookiecutter.public_import_path }}/{{ cookiecutter.project_slug }}"
{% endif %}

ENTRYPOINT [ "./app" ]
