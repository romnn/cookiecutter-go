{% if cookiecutter.project_type == 'tool' -%}
package main
{% else %}
package {{ cookiecutter.project_slug }}
{% endif %}

import "testing"

func TestShout(t *testing.T) {
	if Shout("Test") != "Test!" {
		t.Errorf("Got %s but want \"Test!\"", Shout("Test"))
	}
	if Shout("") != "!" {
		t.Errorf("Got %s but want \"!\"", Shout(""))
	}
}