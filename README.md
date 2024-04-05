# instometer

You can run this in your terminal too! 

```bash
# export vars
export INSTOMETER_API_KEY="..."
export INSTOMETER_VIRTUAL_HARDWARE="true"
# install deps 
pip3 install trio trio-websocket rich textual
# run
python3 main.py
```

## Rough notes 

_These are some notes I jotted down, to turn this into a real README for raspberry pi users_


- sudo raspi-config
- set boot to console autologin
- set name instometer
- enable ssh
- log in via ssh pi@instometer.local
- enter the default pass
- change it: `passwd`
- set -g status off
- gnome-terminal --full-screen 

