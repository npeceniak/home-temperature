# home-temperature

## Submodule Commands
Pull code for all submodules
```bash
git submodule update --init --recursive
```

Update all submodules to lastest version
```bash
git submodule update --remote
```


## Board Communication

rshell is used to communicate with the pico.

once connected to the pico via rshell you can see the files on the board by running `cd /pyboard`

connect to the pico and run the main.py file. Debug info will be printed to the console.
```bash
rshell repl pyboard import main
```


Copy code off of board to current directory.
```bash
rshell cp -r /pyboard .
```