package main

import (
	"fmt"
	"{{ cookiecutter.public_import_path }}/{{ cookiecutter.project_slug }}"
)

func run() string {
	return {{ cookiecutter.project_slug }}.Shout("This is an example")
}

func main() {
	fmt.Println(run())
}