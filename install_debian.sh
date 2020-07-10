#!/bin/bash
APP="SomePythonThings Calc"
ICON="icon.png"
APP_NO_SPACES="SomePythonThings_Calc"
TARGET_DIR="$HOME/.SomePythonThings/$APP_NO_SPACES"
clear
echo $APP + ' Installer\n\nThis .sh file is only for debian based distros, such as Ubuntu, Linux Mint, Debian, ElementaryOS, etc. If not, make sure you have the "xdg-user-dirs" package installed. If you wish to continue press into:'
read NULL
DESKTOP=`xdg-user-dir DESKTOP`
clear
echo 'Working...'
sudo apt install xdg-user-dirs -y
sudo mkdir "$HOME/.SomePythonThings"
sudo mkdir "$TARGET_DIR"
sudo cp "$APP" $TARGET_DIR
sudo chmod +x "$TARGET_DIR/$APP"
sudo cp $ICON "$TARGET_DIR"
sudo echo -e "#!/bin/bash\ncd $TARGET_DIR\n'./$APP'\nread HELLO" > start.sh
sudo mv start.sh $TARGET_DIR
sudo chmod +x "$TARGET_DIR/start.sh"
cd "$DESKTOP"
echo -e "[Desktop Entry]\nType=Application\nName=$APP\nComment=$APP\nIcon=$TARGET_DIR/$ICON\n Exec=$TARGET_DIR/start.sh\nTerminal=false\nCategories=SomePythonThings" > "./$APP.desktop"
sudo cp "./$APP.desktop" "~/.local/share/applications"
clear
echo 'Done!'
