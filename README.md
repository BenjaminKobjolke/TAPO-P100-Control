#Info
 Uses https://github.com/fishbigger/TapoP100
 
 # Use

## Python script
> python tapo.py TAPO_USERNAME TAPO_PASSWORD IP on|off

### Examples
> python tapo.py test@test.com 12345 192.168.10.82 off

> python tapo.py test@test.com 12345 192.168.10.82 on

## Exe from release
tapo.exe TAPO_USERNAME TAPO_PASSWORD IP on|off

### Examples

> tapo.exe test@test.com 12345 192.168.10.82 off

> tapo.exe test@test.com 12345 192.168.10.82 on

# Develop 
## Install
- https://visualstudio.microsoft.com/visual-cpp-build-tools/
- install.bat

## Build exe
- pip install pyinstaller
- pyinstaller -F tapo.py
- exe will be in dist/

