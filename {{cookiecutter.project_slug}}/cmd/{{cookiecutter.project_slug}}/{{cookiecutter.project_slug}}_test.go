package main

import (
	"os"
	"testing"
)

func TestCli(t *testing.T) {
	args := os.Args[0:1] // Name of the program.
	args = append(args, "--name=Peter")
	err := run(args)
	if err != nil {
		t.Errorf("--name option yielded error: %s", err.Error())
	}
}
