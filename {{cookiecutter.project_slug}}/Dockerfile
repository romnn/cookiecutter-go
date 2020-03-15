FROM golang:alpine AS BUILD

LABEL maintainer="{{ cookiecutter.email }}"

ENV GO111MODULE=on

WORKDIR /app
COPY ./ /app

# This removes debug information from the binary
# Assumes go 1.10+
{% if cookiecutter.project_type == 'both' -%}
RUN CGO_ENABLED=0 GOARCH=amd64 GOOS=linux go build -a -ldflags="-w -s" -o app "{{ cookiecutter.public_import_path }}/{{ cookiecutter.project_slug }}/cmd/{{ cookiecutter.project_slug }}"
{% elif cookiecutter.project_type == 'tool' -%}
RUN CGO_ENABLED=0 GOARCH=amd64 GOOS=linux go build -a -ldflags="-w -s" -o app "{{ cookiecutter.public_import_path }}/{{ cookiecutter.project_slug }}"
{% endif %}

FROM gcr.io/distroless/static
COPY --from=BUILD /app/app /app
ENV PORT 3000
EXPOSE 3000
ENTRYPOINT [ "/app" ]
