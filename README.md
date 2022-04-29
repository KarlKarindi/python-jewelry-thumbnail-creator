## To use: ##

Simply write 

`pip3 install -r requirements.txt`

`python .\src\ui\menu.py`


## Making an exe: ##

`pyinstaller --onefile -w .\src\ui\menu.py`

drag from dist folder the menu.exe to root folder, delete dist

create a ZIP of the root folder by right clicking on root and "Send to .zip"

open NSIS app -> Installer based on ZIP file -> Set the zip file here

This takes a few minutes but all is done