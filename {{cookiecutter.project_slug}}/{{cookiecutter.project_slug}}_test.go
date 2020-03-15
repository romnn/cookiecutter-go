package {{ cookiecutter.project_slug }}

{% if cookiecutter.project_type == 'tool' -%}
// Rev is set on build time to the git HEAD
var Rev = ""
{% endif %}

// Version is incremented using bump2version
const Version = "0.0.1"

{% if cookiecutter.project_type == 'tool' -%}
// TODO Add cli and everything here
{% else %}

{% endif %}