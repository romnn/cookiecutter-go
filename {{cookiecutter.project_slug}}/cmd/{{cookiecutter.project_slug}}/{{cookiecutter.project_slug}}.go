package main

import (
	"os"
	"fmt"

	"{{ cookiecutter.public_import_path }}/{{ cookiecutter.project_slug }}"
	log "github.com/sirupsen/logrus"
	"github.com/urfave/cli/v2"
)

// Rev is set on build time to the git HEAD
var Rev = ""

// Version is incremented using bump2version
const Version = "0.0.1"


func serve(c *cli.Context) error {
	greeting := fmt.Sprintf("Hi %s", c.String("name"))
	log.Info({{ cookiecutter.project_slug }}.Shout(greeting))
	return nil
}


func run(args []string) error {
	app := &cli.App{
		Name:  "{{ cookiecutter.project_slug }}",
		Usage: "",
		Flags: []cli.Flag{
			&cli.StringFlag{
				Name:    "name",
				Aliases: []string{"n"},
				Usage:   "Your name",
			},
		},
		Action: func(c *cli.Context) error {
			err := serve(c)
			return err
		},
	}
	return app.Run(args)
}

func main() {
    err := run(os.Args)
	if err != nil {
		log.Fatal(err)
	}
}