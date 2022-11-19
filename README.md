# home-temperature

### prerequisites 

- python3
- make


### Setup System From Scratch

- Build nodes according to spec with pico w and dht11 sensor
    - TODO: Add circuit diagram

1. Connect node to machine via USB
2. Run the following and follow the prompts
    ```bash
    make generate_dashboard clear_board config upload run
    ```

The `dashboard` endpoint will be avaliable on every node configured by going to http://<IP>/dashboard 

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