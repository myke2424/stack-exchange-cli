## Stack Exchange Search CLI

Search stack exchange websites in your terminal!

With beautiful terminal formatting using Rich.

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

Install **python3.10** and just use **pip** to install the requirements file

```bash
python3.10 -m pip install -r requirements.txt
```

Or use **poetry** to install dependencies (https://python-poetry.org/docs/)

```bash
poetry install
```

Or run the `scripts/install.sh` script in the **root directory**

```bash
sudo bash install.sh
```

## Usage

### Fast Search

Use the **-q** command followed by the search query:

```bash
python3 -m stack_exchange -q="BFS vs DFS"
```

The above command uses fast search, which fetches the top-voted question and answer and displays them to the console.

### Command Line Arguments

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

## Configuration

The application can be optionally configured using the `config.yaml` file in the root directory

### API Configuration

Fill out yaml `api` values with stack exchange API credentials to prevent request throttling. Read more
here:  (https://api.stackexchange.com/docs)

### Redis Configuration

Fill out yaml `redis` values with redis credentials if you want to hook up the application to a redis db for request
caching.

### Logging configuration

Modify `logging` values to adjust application log settings.
