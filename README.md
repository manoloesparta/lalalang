![La La Lang Logo](./docs/logo.png)

# 3LANG ♪♪

![Python version](https://img.shields.io/badge/Python-3.9%2B-blue)
![Project version](https://img.shields.io/badge/Version-0.3.5-blueviolet)
![Branch status](https://github.com/manoloesparta/lalalang/actions/workflows/main.yml/badge.svg)
![Coverage Status](https://coveralls.io/repos/github/manoloesparta/lalalang/badge.svg?t=xGQ81l)
![License](https://img.shields.io/badge/License-MIT-red)

> A programming language with a silly name 

I saw recently the **amazing** movie [La La Land](https://www.youtube.com/watch?v=xVVqlm8Fq3Y) and inspired by only the movie's name and my learning obsession I decided to learn how to make a programming language and give it a funny name 🙂. 

**Warning**: This shouldn't be used in any production enviroment, it is very slow and poorly designed, it was made with educational purposes only.

## Installation

The only requirement is to have Python 3.9+ (you can install it [directly](https://www.python.org/downloads/release/python-396/) or with [pyenv](https://github.com/pyenv/pyenv)).

You can install with pip:

```bash
$ pip install lalalang
```

Or by source

```bash
$ git clone https://github.com/manoloesparta/lalalang && cd alalang
$ make setup env=python # Here goes the path of your python 3.9 executable
$ make install
```

**Info**: If the terminal returns `command not found: 3lang` you should see where pip is installing your package and add that directory to PATH, sometimes using `sudo` with pip solves it, or adding the `--user` flag, if none of these options works can still use the interpreter with the command `python -m lalalang`.

## Usage

You can see the main options with this command

```bash
$ 3lang --help

Usage: 3lang [OPTIONS]

Options:
  --mode TEXT  REPL mode (lex|parse|eval)
  --src TEXT   Input file with 3lang code
  --help       Show this message and exit.
```

To enter the interpreter and run code on the fly, type

```bash
$ 3lang

Welcome to the city of stars!🌟
This is the La La Lang Programming Languag v0.3!
♪♪ > 
```

To read a file and execute it, type

```bash
$ 3lang --src random_program.3la
```

You can enter other in the stages of lexing and parsing of the interpreter with the ```--mode``` flag.

## Syntax

You can see the syntax of lalalang in [here](./docs).

See the [examples](./examples) directory to get a wider idea.

## License

This project is under the MIT license.
