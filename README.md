# ack
This is a service that run a task in the b**ACK**ground (daemonizing it). It's **NOT** a container (as Docker) or a virtual machine. The service just starts the app in the daemon.
## Install
```sh
git clone https://github.com/medowic/ack.git
cd ack
bash install.sh
```
## Usage
### Start app in background:
When you start an app, the daemon gets the user by which the app was started, and the working directory in daemon is equal to the current directory.

Command is required to start the script (or app), if there is no shebang at the head of the file.

You must start the daemon using `sudo`
```sh
sudo ack [command]
```
Also, you can start daemon as root with `rack`
```sh
sudo rack [command]
```
### Show working daemons:
This command show all working daemons at the moment
```
$ sudo ack -l
List of working daemons:
1 # 65535 "python3 main.py 'Hello World!'" as root
2 # ...
3 # ...
```
### Restart daemon:
```sh
sudo ack -r [taskid]
```
For example, we have daemon with id 65535
```
$ sudo ack -r 65535
Daemon with id 65535 was restarted
```
### Stop daemon:
This command stop the daemon and delete service file
```sh
sudo ack -s [taskid]
```
For example, we have daemon with id 65535
```
$ sudo ack -s 65535
Daemon with id 65535 was stopped
```
## Flags
- `-s`, `--stop` - stop the daemon and delete service file
- `-r`, `--restart` - restart the daemon
- `-l`, `--list` - shows the started daemons with ID, command and daemon-user
## License
This is project is under the [MIT License](https://raw.githubusercontent.com/medowic/ack/master/LICENSE)
