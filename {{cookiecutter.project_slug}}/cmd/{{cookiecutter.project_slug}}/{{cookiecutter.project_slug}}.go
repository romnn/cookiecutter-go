package main

import (
	"os"

	log "github.com/sirupsen/logrus"
	"github.com/urfave/cli/v2"
)

// Rev is set on build time to the git HEAD
var Rev = ""

// Version is incremented using bump2version
const Version = "0.0.1"


func serve() error {
	log.Debug("Hi this is entry")
	return nil
}


func main() {
	app := &cli.App{
		Name:  "{{ cookiecutter.project_slug }}",
		Usage: "t.b.a",
		Flags: []cli.Flag{
			&cli.StringFlag{
				Name:    "file",
				Aliases: []string{"f"},
				Usage:   "Load configuration from `FILE`",
			},
		},
		Action: func(c *cli.Context) error {
			err := serve(c)
			return err
		},
	}
	err := app.Run(os.Args)
	if err != nil {
		log.Fatal(err)
	}
}