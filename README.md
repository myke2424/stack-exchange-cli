# Stack Exchange Search CLI

[![PyPI](https://img.shields.io/pypi/v/stack-exchange-cli?color=brightgreen)](https://pypi.org/project/stack-exchange-cli/) ![Build status](https://github.com/myke2424/stack-exchange-cli/actions/workflows/build.yaml/badge.svg)

Search stack exchange websites in your terminal!

With beautiful terminal formatting using Rich.

All stack exchange websites available for searching: https://stackexchange.com/sites

### Fast Search
![Fast search Demo](https://s1.gifyu.com/images/Recording-2022-07-17-at-18.39.33-4.gif)

### Interactive Search
![Interactive search Demo](https://s4.gifyu.com/images/Recording-2022-07-21-at-11.33.13.gif)

## Table of Contents
1. [How it works](#how-it-works)
2. [Install](#install)
3. [Usage](#usage)
4. [Command Line Arguments](#cli-args)
5. [Configuration](#config)
6. [Testing](#testing)
7. [TODO](#todo)

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
Just pip install it! Fast and easy.

```bash
python3.10 -m pip install stack-exchange-cli
```

### Install Python 3.10

#### Mac
```bash
brew install python@3.10
```

#### Linux
```bash
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install python3.10 -y
```
#### Windows
Download from here: https://www.python.org/downloads/

### Alternative methods to install
- Install the **requirements** file manually

    ```bash
    python3.10 -m pip install -r requirements.txt
    ```
  
- Use **poetry** to install dependencies locally (https://python-poetry.org/docs/)

    ```bash
    poetry install
    ```

- Run the `scripts/install_ubuntu.sh` script [*UBUNTU* ONLY]

    ```bash
    # run in root directory
    sudo bash scripts/install_ubuntu.sh
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
se -q="BFS vs DFS"
```

The above command uses fast search, which fetches the top-voted question and answer and displays them to the console.

### Interactive Search
Use the **-q** command followed by the search query and **-i** or **--interactive**

```bash
se -q="BFS vs DFS" -i
```
Interactive search allows the user to interact while searching, analogous to browsing stack-exchange questions in your browser, except in the terminal!



### Run directly with python interpreter
```bash
python3.10 -m stack_exchange -q="BFS vs DFS"
```

## Command Line Arguments  <a name="cli-args"></a>
| Short | Long | Description | Example | Default |
|---|---|---|---|---|
| -q | --query | [*REQUIRED FOR SEARCH*] Search query | se -q="How to merge two dictionaries" | N/A |
| -s | --site | [*OPTIONAL*] Stack Exchange website to search on View all sites here: (https://stackexchange.com/sites) | se -q="Big O" -s="softwareengineering" | "stackoverflow" |
| -t | --tags | [*OPTIONAL*] Search tags (space-delimited) | se -q="Segmentation fault cause" -t="c c++" | N/A |
| -i | --interactive | [*OPTIONAL*] Allow the user to interact while searching | se -q="Tree traversal" -i | False |
| -n | --num | [*OPTIONAL*] [*INTERACTIVE ONLY*] Number of results to display | se -q="Segmentation fault cause" -i -n=20 | 30 |
| -sb | --sortby | [*OPTIONAL*]  Method to sort the search results by  choices = ["votes", "creation", "relevance", "activity"] | se -q="Python memory" -sb="relevance" | "votes" |
| -vv | --verbose | [*OPTIONAL*] Verbose logging flag, set log level to DEBUG | se -q="Dictionary internals" -vv | False |
| -c | --config | [*OPTIONAL*] config.yaml file path to use for  API, Redis and logging settings | se -q="Directed graph" -c="/mnt/c/config.yaml" | N/A |
| -k | --key | [*OPTIONAL*] Use stack exchange API key for requests | se -q="Min heap vs max heap" -k="12345" | N/A |
| -sk | --set-key | [*OPTIONAL*] Set stack exchange API key in config.yaml, to avoid repeating using -k in search commands  | se -sk="12345" | N/A |
| -fc | --flush-cache | [*OPTIONAL*] Flush all keys/values in redis cache | se -fc | False |
| -oc | --overwrite-cache | [*OPTIONAL*] Overwrite cache value if key exists | se -q="DFS vs BFS" -oc | False |
| -j | --json | [*OPTIONAL*] Print search results as json to stdout | se -q="DFS vs BFS" -j | False |
| -a | --alias | [*OPTIONAL*] View the cached search result under the specified alias | se -a ="my_alias_i_saved_my_search_result" | N/A |
| -h | --help | [*OPTIONAL*] Displays help text  | se -h | N/A |
| -v | --version | [*OPTIONAL*] Displays version number | se -v | N/A |
## Configuration  <a name="config"></a>

The application can be configured by using the `-c` cmd line argument to point it to a `yaml` config file path. 
```bash
se -q="DFS vs BFS" -c="/mnt/c/my_config_file.yaml"
```

**Note**: Most users won't need to configure the application, it's supposed to be easy to use out of the box! These are **optional** configuration settings the user can use. By default, the application will be packaged up with the `config.yaml` in the root directory.
### API Configuration

Fill out yaml `api` values with a stack exchange `API key` to prevent **request throttling**. \
Read more here:  https://api.stackexchange.com/docs/throttle

You can get an API Key by **registering** as a new app from here: http://stackapps.com/apps/oauth/register \
If you use an api key, you will have a daily request limit of **10000**

**Note**: You probably won't need an API key if you are a light-user.

**From stack-exchange**: "Every application is subject to an IP based concurrent request throttle. If a single IP is making more than 30 requests a second, new requests will be dropped. The exact ban period is subject to change, but will be on the order of 30 seconds to a few minutes typically."


### Redis Configuration

Fill out yaml `redis` values with redis credentials if you want to hook up the application to a redis db for request caching.

Speed benefits are minor, but it will help with being throttled as it will just read the cache instead of going over the network to the stack exchange API if you request the same thing more than once.

There are also command line arguments for interfacing with the cache, i.e. overwrite values in the cache or flush the cache.

This isn't needed but if you want to use the redis free tier, check out: https://redis.com/try-free/
### Logging configuration

Modify `logging` values to adjust application log settings.

By default, logging to a file will be disabled and the log level will be critical to avoid polluting the output.

### Example Config File
*config.yaml*
```yaml
api:
  api_key: your_api_key # optional
  default_site: "stackoverflow"  # required
  version: 2.3 # required

redis: # all fields optional
  host: redis-notarealhost.redislabs.com
  port: 12345
  password: redisdbfakepassword

logging: # all fields required
  log_to_file: true 
  log_filename: "stackexchange.log"
  log_level: "DEBUG"
```

## Testing  <a name="testing"></a>
Run tests using pytest
```bash
python3.10 -m pytest
```

## TODO <a name="todo"></a>
Refactor CLI to use https://github.com/Textualize/textual for interactive search