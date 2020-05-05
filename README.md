# papirus-gadget
USB gadget controlled by PaPiRus e-ink screen and buttons

# Usage
* Use the up and down buttons to scroll through the list of files.
    * The file list will loop forever.  The list of available files is refreshed when looping past the last element.
* The screen uses quick updates to make file browsing snappy.  If it becomes unreadable press the redraw button.
* Press select to attempt to load the file display on the top line
* "DISK OK" means the modprobe command succeeded.  It does not guarantee the disk will function. 
* The bottom line shows the last selected file.
* To load a file as a cdrom the cdrom button to append "cdrom=y" to the next selection.  A lower case "cdrom" will appear to the right.  Press select to load the file as a cdrom.  The status line should now read "CDROM OK".

# Install
* Setup PaPiRus: https://github.com/PiSupply/PaPiRus
  * For Arch see my fork: 
* Create a directory for disks
  * Use the default location or modify papirus-gadget.service
* Make the gadget directory:
```
sudo mkdir /gadget_disks
sudo chown `whoami` /gadget_disks
ln -s /gadget_disks $HOME/
```
* Copy or link files into place:
```
sudo ln -s `pwd`/papirus-gadget.py /usr/local/bin/
sudo cp papirus-gadget.service /etc/systemd/system/
```
* Start and enable service:
```
sudo systemctl start papirus-gadget.service
sudo systemctl enable papirus-gadget.service
```

# Torrent setup
Putting a torrent client directly on the Pi is an easy way to download and verify iso files.  For this I've chosen rtorrent: 
* Only runs when you launch it; no background processes by default
* Works well via ssh
* Other clients were overwhelming the Pi, this one had a simple performance tuning wiki 

# Useful tutorials

* https://linux-sunxi.org/USB_Gadget/Mass_storage
* https://rys.pw/raspberry_pi_as_fake_mass_storage
