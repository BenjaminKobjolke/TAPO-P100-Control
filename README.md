# Install
- https://visualstudio.microsoft.com/visual-cpp-build-tools/
- install.bat

# Use
> python tapo.py TAPO_USERNAME TAPO_PASSWORD IP on|off

Examples
> python tapo.py test@test.com 12345 192.168.10.82 off
> > python tapo.py test@test.com 12345 192.168.10.82 on


# Build exe
- pip install pyinstaller
- pyinstaller -F tapo.py
- exe will be in dist/

