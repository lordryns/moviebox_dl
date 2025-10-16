
This tool is an unofficial client for downloading movies from the terminal

### How to get started 
You'll need to have [Python](https://www.python.org/) installed to run this script, you'll also need a package manager in order to install the necessary dependencies, luckily, Python comes with [pip](https://en.wikipedia.org/wiki/Pip_(package_manager)) preinstalled. 

### Setup 
Now for the main setup, you'll need to clone this repo first (assuming you have [git](https://git-scm.com/) installed. If that is not the case, simply download this repo and extract the folder.)

To use git to clone this repo: 
```bash 
git clone https://github.com/lordryns/moviebox_dl.git
```

then enter the path:
```bash 
cd moviebox_dl
```

After this stage, you'll need to install the necessary dependencies to run this script, to do this run:
```bash
pip install -r requirements.txt
```

or if you're using uv: 
```bash 
uv sync
```

*use any package manager of your choice, it doesn't really matter* 

This should set up everything successfully but if it doesn't, please leave an [issue](https://github.com/lordryns/moviebox_dl/issues/new) and we'll try to assist you with the setup.

### How to use
Despite being just a single python script, moviebox_dl works like a cli tool. 
Example usage:

```bash 
python main.py find -s "Star Wars"
```

or if you're using uv to run:
```bash 
uv run main.py find -s "Star Wars"
```

moviebox_dl takes two commands:
- find (as seen above)
- audit

The `audit` command is much more easy to use as its job is simply to detect any existing issues you might be encountering and suggest ways to fix them.

to use:
```bash 
python main.py audit # or uv run
```

The `find` sub-command is what you'll be using most of the time, it takes quite a number of options:

- `-s or --search`: This is arguably the most important, it should be used alongside an argument
	- **usage**:
	```bash 
	python run main.py find -s "Star Wars"
	```

- `--browser-id`: Use this to set the browser id you want to use for the download process, defaults to Chrome. 
	**options**:
		- `0`: Chrome (default)
		- `1`: Firefox
	**usage**:
	```bash 
	python main.py find -s "Star Wars" --browser-id 1 # this sets it to firefox
	```

- `-t or --timeout`: This sets the wait time the script should adhere to after every request, adjusting this might prove useful in cases of bad internet connection, it takes a number as an argument and defaults to 2.
	- **usage**:
	```bash
	python main.py find -s "Star Wars" -t 5 # 5 seconds of wait after every request
	```

- `-h`: By default, moviebox_dl runs in headless mode mode meaning it does not bring up a browser while executing commands, if you want to see a visible browser while the script is running, include this flag
	- **usage**:
```bash 
python main.py find -s "Search" -h
```


Thats all for now, if you encounter any issues while running, please submit an [issue](https://github.com/lordryns/moviebox_dl/issues/new) and we'll attend to it immediately.

Happy downloading :)

