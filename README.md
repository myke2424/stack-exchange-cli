# Stack Exchange Search CLI

[![PyPI](https://img.shields.io/pypi/v/stack-exchange-cli?color=brightgreen)](https://pypi.org/project/stack-exchange-cli/) ![Build status](https://github.com/myke2424/stack-exchange-cli/actions/workflows/build.yaml/badge.svg)

Search stack exchange websites in your terminal!

With beautiful terminal formatting using Rich.

![Demo](https://media.giphy.com/media/TsWaWpgD0S4bP3SHv3/giphy.gif)


## Table of Contents
1. [How it works](#how-it-works)
2. [Install](#install)
3. [Usage](#usage)
4. [Command Line Arguments](#cli-args)
5. [Configuration](#config)
6. [Testing](#testing)

## How it works  <a name="how-it-works"></a>

Displays the highest up-voted question and top answer for your search request \
*Inspired by*: https://github.com/chubin/cheat.sh

## Install

##### Supported platforms

* Linux
* Windows
* Mac

##### Requirements

* Python 3.10 or higher
 

### Main Installation
Just pip install it!

```bash
python3.10 -m pip install stack-exchange-cli
```

### Alternative methods to install
- Install the **requirements** file manually

    ```bash
    python3.10 -m pip install -r requirements.txt
    ```
  
- Use **poetry** to install dependencies locally (https://python-poetry.org/docs/)

    ```bash
    poetry install
    ```

- Run the `scripts/install.sh` script to install into a venv named `.stack-exchange-venv` [*UBUNTU* ONLY]

    ```bash
    # run in root directory
    sudo bash scripts/install.sh
    ```

- Install to venv named `.stack-exchange-venv` using make 
    
  ```bash
  # run in root directory
  make
  ```

- Build from source using poetry

  ```bash
  # run in root directory
  poetry build
  python3.10 -m pip install dist/stack_exchange_cli*.whl
  ```

## Usage  <a name="usage"></a>

### Fast Search

Use the **-q** command followed by the search query:

```bash
python3 -m stack_exchange -q="BFS vs DFS"
```

The above command uses fast search, which fetches the top-voted question and answer and displays them to the console.

### Interactive Search
Use the **-q** command followed by the search query and **-i** or **--interactive**

```bash
python3 -m stack_exchange -q="BFS vs DFS" -i
```
Interactive search allows the user to interact while searching, analogous to browsing stackoverflow questions in your browser, except in the terminal!

## Command Line Arguments  <a name="cli-args"></a>
| Short | Long | Description | Example | Default |
|---|---|---|---|---|
| -q | --query | [*REQUIRED*] Search query | python3.10 -m stack_exchange -q="How to merge two dictionaries" | N/A |
| -s | --site | [*OPTIONAL*] Stack Exchange website to search on View all sites here: (https://stackexchange.com/sites) | python3.10 -m stack_exchange -q="Big O" -s="softwareengineering" | "stackoverflow" |
| -t | --tags | [*OPTIONAL*] Search tags (space-delimited) | python3.10 -m stack_exchange -q="Segmentation fault cause" -t="c c++" | N/A |
| -i | --interactive | [*OPTIONAL*] Allow the user to interact while searching | python3.10 -m stack_exchange -q="Tree traversal" -i | False |
| -n | --num | [*OPTIONAL*] Number of results to display when  interactive searching, must be used with -i | python3.10 -m stack_exchange -q="Segmentation fault cause" -i -n=20 | 30 |
| -sb | --sortby | [*OPTIONAL*] Method to sort the search results by  choices = ["votes", "creation", "relevance", "activity"] | python3.10 -m stack_exchange -q="Python memory" -sb="relevance" | "votes" |
| -vv | --verbose | [*OPTIONAL*] Verbose logging flag, set log level to DEBUG | python3.10 -m stack_exchange -q="Dictionary internals" -vv | False |
| -c | --config | [*OPTIONAL*] config.yaml file path to use for  API, Redis and logging settings | python3.10 -m stack_exchange -q="Directed graph" -c="/mnt/c/config.yaml" | N/A |
| -k | --key | [*OPTIONAL*] Use stack exchange API key for requests | python3.10 -m stack_exchange -q="Min heap vs max heap" -k="12345" | N/A |
| -h | --help | [*OPTIONAL*] Displays help text  | python3.10 -m stack_exchange -h | N/A |
| -v | --version | [*OPTIONAL*] Displays version number | python3.10 -m stack_exchange -v | N/A |

## Configuration  <a name="config"></a>

The application can be optionally configured using the `config.yaml` file in the root directory or by using the `-c` cmd argument to point it to a config file path.

### API Configuration

Fill out yaml `api` values with a stack exchange `API key` to prevent **request throttling**. \
Read more here:  https://api.stackexchange.com/docs/throttle

You can get an API Key by **registering** as a new app from here: http://stackapps.com/apps/oauth/register

### Redis Configuration

Fill out yaml `redis` values with redis credentials if you want to hook up the application to a redis db for request caching.

Speed benefits are minor, but it will help with being throttled as it will just read the cache instead of going over the network to the stack exchange API if you request the same thing more than once.

This isn't needed but if you want to use the redis free tier, check out: https://redis.com/try-free/
### Logging configuration

Modify `logging` values to adjust application log settings.

By default, logging to a file will be disabled and the log level will be critical to avoid polluting the output.

### Example Config File
*config.yaml*
```yaml
api:
  api_key: your_api_key
  default_site: "stackoverflow" 
  version: 2.3

redis:
  host: redis-notarealhost.redislabs.com
  port: 12345
  password: redisdbfakepassword

logging:
  log_to_file: true
  log_filename: "stackexchange.log"
  log_level: "DEBUG"
```

## Testing  <a name="testing"></a>
Run tests using pytest
```bash
python3.10 -m pytest
```