# open Platform of Universal Board Game
>A RPI SD&D Project

**open Platform of Universal Board Game** (a.k.a. openPubg) is an open text-based gaming platform that allows users to host your own servers and play different game through text messages or emails. This project is designed to be modularized, and also allows game developers to implement your own games through APIs for this platform.


## Installation
#### Run from binary
The pre-built binary can be run in Linux systems without any pre-installation. You can simply download the binary files from the [release page]().

#### Run from source code
You can also choose to run the server from Python source code. The server requires Python 3 (3.5 or above) and Google Gmail Python API. Users can either manually install all the requirements or run the automatic installation script that is included in the repository:
```shell
./install.sh
```

#### Build from source code
For more advanced usages, you can also build openPubg from source. The Python binary is built through `pyinstaller`. So, you need install `pyinstaller` first and then build openPubg:
```shell
pip3 install pyinstaller
pyinstaller ./src/openPubg.py

```
This commands will generate a `dist` folder, and you can find the bundled app in the folder.


## Usage
To start the server, you can run the binary:
```shell
./openPubg/openPubg
```
or run the source code:
```shell
./src/openPubg.py
# or
python3 ./src/openPubg.py
```
Then, the program will redirect you into a web browser that allows you to login a Gmail account. The Gmail account you login will be the address of the server. If you have previously used the server on the current machine, the program will automatically login the previous account. To forget the old account, you can simple delete the `.credentials` folder.

#### Commands
After lunching the server, you will see the openPubg command line interface. There are several commands can be used in the command line:

| Command       | Description                                        |
|---------------|----------------------------------------------------|
|echo [message] |Print the given message                             |
|list           |List all the current running rooms                  |
|send           |Send a short message to given phone number or email |
|info           |Show the info log of the server                     |
