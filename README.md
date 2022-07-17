# Stack Exchange Search CLI
[![PyPI](https://img.shields.io/pypi/v/stack-exchange-cli?color=brightgreen)](https://pypi.org/project/stack-exchange-cli/) ![Build status](https://github.com/myke2424/stack-exchange-cli/actions/workflows/build.yaml/badge.svg)

Search stack exchange websites in your terminal!

With beautiful terminal formatting using Rich.

![Demo](https://media.giphy.com/media/TsWaWpgD0S4bP3SHv3/giphy.gif)
## How it works

Displays the highest up-voted question and top answer for your search request \
*Inspired by*: https://github.com/chubin/cheat.sh

## Install

##### Supported platforms

* Linux
* Windows
* Mac

##### Requirements

* Python 3.10 or higher

#####      
Just pip install it!
```bash
python3.10 -m pip install stack-exchange-cli
```

Or install the **requirements** file manually

```bash
python3.10 -m pip install -r requirements.txt
```

Or use **poetry** to install dependencies locally (https://python-poetry.org/docs/)

```bash
poetry install
```

Or run the `scripts/install.sh` script - in the **root directory**

```bash
sudo bash scripts/install.sh
```

Or build using make - in the **root directory**

```
make
```

Or build from source using poetry

```bash
poetry build
python3.10 -m pip install dist/stack_exchange_cli*.whl
```

## Usage

### Fast Search

Use the **-q** command followed by the search query:

```bash
python3 -m stack_exchange -q="BFS vs DFS"
```

The above command uses fast search, which fetches the top-voted question and answer and displays them to the console.

### Command Line Arguments

| Short | Long          | Description                                                                                   | Example                                                                  | Required | Default         |
|-------|---------------|-----------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|----------|-----------------|
| -q    | --query       | Search query                                                                                  | python3.10 -m stack_exchange -q="How to merge two dictionaries"          | True     | N/A             |
| -s    | --site        | Stack Exchange website to search on View all sites here: (https://stackexchange.com/sites)    | python3.10 -m stack_exchange -q="Big O" -s="softwareengineering"         | False    | "stackoverflow" |
| -t    | --tags        | Search tags (space-delimited)                                                                 | python3.10 -m stack_exchange -q="Segmentation fault cause" -t="c c++"    | False    | N/A             |
| -i    | --interactive | Allow the user to interact while searching                                                    | python3.10 -m stack_exchange -q="Tree traversal" -i                      | False    | False           |
| -n    | --num         | Number of results to display when interactive searching, must be used with -i                 | python3.10 -m stack_exchange -q="Segmentation fault cause" -i -n=20      | False    | 30              |
| -sb   | --sortby      | Method to sort the search results by choices = ["votes", "creation", "relevance", "activity"] | python3.10 -m stack_exchange -q="Python memory" -sb="relevance"          | False    | "votes"         |
| -v    | --verbose     | Verbose logging flag, set log level to DEBUG                                                  | python3.10 -m stack_exchange -q="Dictionary internals" -v                | False    | False           |
| -c    | --config      | config.yaml file path to use for API, redis and logging settings                              | python3.10 -m stack_exchange -q="Directed graph" -c="/mnt/c/config.yaml" | False    | N/A             |
| -k    | --key         | Use stack exchange API key for requests                                                       | python3.10 -m stack_exchange -q="Min heap vs max heap" -k="12345"        | False    | N/A             |
**Search query** [*REQUIRED*]

```bash
# -q or --query
python3.10 -m stack_exchange -q="How to merge two dictionaries"
```

**Stack exchange site** to search on [*OPTIONAL*] - default=stackoverflow \
View all sites here: (https://stackexchange.com/sites)

```bash
# -s or --site
python3.10 -m stack_exchange -q="Big O vs Big Theta" -s="softwareengineering"
```

**Stack exchange tags** [*OPTIONAL*]

```bash
# -t or --tags
python3.10 -m stack_exchange -q="Segmentation fault cause" -t="c c++ rust"
```

**Interactive Search** [*OPTIONAL*] \
Allow the user to interact while searching, analogous to browsing stackoverflow questions in your browser,
except in the terminal!

```bash
# -i or --interactive
python3.10 -m stack_exchange -q="Segmentation fault cause" -i
```

**Number of results** to display when interactive searching [*OPTIONAL*] - default=20

```bash
# -n or --num
python3.10 -m stack_exchange -q="Segmentation fault cause" -i -n=20
```

**Sort By** - default="votes"  [*OPTIONAL*] \
Method to sort the search results by, default we sort by highest score \
*choices* = ["votes", "creation", "relevance", "activity"]
```bash
# -sb or --sortby
python3.10 -m stack_exchange -q="Segmentation fault cause" -sb="relevance"
```

**Verbose logging flag** [*OPTIONAL*]
```bash
# -v or --verbose
python3.10 -m stack_exchange -q="Segmentation fault cause" -v
```

## Configuration

The application can be optionally configured using the `config.yaml` file in the root directory

### API Configuration

Fill out yaml `api` values with a stack exchange API key to prevent request throttling. Read more
here:  (https://api.stackexchange.com/docs/throttle)

### Redis Configuration

Fill out yaml `redis` values with redis credentials if you want to hook up the application to a redis db for request
caching.

### Logging configuration

Modify `logging` values to adjust application log settings.
