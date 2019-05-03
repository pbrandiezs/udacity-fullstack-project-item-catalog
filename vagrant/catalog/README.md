# Program: application.py 
* Author: Perry Brandiezs
* Date: May 1, 2019


This program demonstrates CRUD operations using an Item Catalog.

*   Create: Ability to create an airplane item
*   Read:   Ability to read an inventory list showing category name, item name, item description.  Ability to show item detail, login required.
*   Update: Ability to edit item detail, login required.
*   Delete: Ability to delete an item, login required and must be item creator.

This program demonstrates OAuth2 authentication and authorization using a third party provider.
*   Login / Logout using Facebook is provided, link can be found at the top-right of the main screen.
*   Login required to display item detail, update an item, or delete an item.
*   Must also be the item creator to delete.

This program demonstrates API endpoints.
*   Display all items
*   Display specific item detail
*   Display all users


## Installation 
This program requires Virtualbox and Vagrant to be installed.

### System Preparation
These procedures document the setup on an HP laptop running WIN 10 Pro.

#### BIOS setup
* Reboot the system to access the BIOS setup, by pressing F10 as the system powers-up
* Move to the settings screen
* Enable Virtualization Technologies
* Save the change and continue the system boot
#### Disable hyper-v
If previously enabled, it is necessary to disable hyper-v to run Ubuntu 64 bit in Virtual-box.
* Select Windows logo
* Type Control Panel
* Select Programs
* Turn Windows features on or off
* Make sure Hyper-V, and it's options are not selected
* Click OK
### Virtualbox Installation
Download and install VirtualBox following the procedures here:
https://www.virtualbox.org/wiki/Downloads

This program was tested with the most recent version of VirtualBox Version 6.0.4 r128413 (Qt5.6.2)
### Virtualbox Extension Pack Installation
Download and install Virtual Box Extension Pack following the procedures here:
https://www.virtualbox.org/wiki/Downloads
### Vagrant Installation
Download and install Vagrant following the procedures here:
https://www.vagrantup.com/downloads.html

This program was tested with the most recent version Vagrant 2.2.4
### Vagrant VM Installation
* Download, uncompress, and install the Vagrant VM from this link:
https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip
* Change into the vagrant directory: **cd vagrant**
* Start the VM, this may take a few minutes: **vagrant up**
* Connect to the VM: **vagrant ssh**
* ctrl-d to exit from Vagrant
### Data Load Procedures
Initial database creation is done with the program models.py.  Testing data can be loaded with the programe create_planes.py.
* Connect to the VM: **vagrant ssh**
* cd to the shared vagrant directory: **cd /vagrant/catalog**
* python models.py
* python create_planes.py
* ctrl-d to exit from Vagrant
## Usage
The main program can be run with python application.py
* cd to the vagrant directory
* Connect to the VM: **vagrant ssh**
* cd to the VM's vagrant directory: **cd /vagrant/catalog**
* Execute the program: **python application.py**
* ctrl-c to interrupt the program / webserver
* ctrl-d to exit from Vagrant
* vagrant halt to shutdown the vagrant VM (restart again with vagrant up)
## Website
While the program is running, connect to the webserver at the link using your browser:
http://localhost:8000/
## API endpoints
Reach the API endpoints at:
```
http://localhost:8000/items/JSON
http://localhost:8000/item/<int:item_id>/JSON
http://localhost:8000/users/JSON
```
## Expected Output
* See the file Expected_Output.docx for screenshots
## Test Users
Facebook test users have been created to assist with evaluating this program.  You may use these User ID's for testing.

Name                            User ID	        Email	
Samantha Alcfecacfabha Smithsen	100036531361281	owfdypjzrh_1556917027@tfbnw.net
Ethan Alcfdejffdaje Alisonberg	100036450664105	vlugcdqxcw_1556917029@tfbnw.net
Helen Alcfdddicdcbf Goldmanescu	100036444934326	liuvpscgnn_1556917024@tfbnw.net
