# [Fab](http://www.fabfile.org/)-Lemp-Automation

> Is a very Simple Web Server Setup Automation for LEMP Stack using Python Fabric. 
> 
> This will install all the necessary components and configure the important modules to get you started without having to manually do all the dirty stuff.


## Installation :large_blue_circle:

Simply clone the repository

```
git clone https://github.com/johnturingan/fab-lemp-automation.git
```

or download the zip file and extract it

```
https://github.com/johnturingan/fab-lemp-automation/archive/master.zip
```
##### PEM Folder
> Inside the **pem** folder, you need to put the following:
> 
 * **Remote Server Private Key (.pem)** - Will use this to connect to your remote server. Make sure that your .pem permission is **0400**. Change it if not.
 ``` $ chmod 0400 YourPrivateKey.pem```

##### SSH Folder
>  
 *  **id_rsa** - Deploy user private key
 *  **id_rsa.pub** - Deploy user public key
 *  **authorized_keys** = public key of the users you want to have access to your remote server. Usually this is your personal public key

##### NGINX Folder

> Inside the nginx folder is where you need to put your nginx configuration of your setup. Check the template-cms for your reference

##### ENV 

> Make a copy of env.sample.json at name it **env.json**. Adjust any configuration based on what you need.

## Usage :white_check_mark:

After cloning or downloading, go to the folder and run the command

```
$ fab -i pem/project.pem -H=user@127.0.0.1 init
```
* **project.pem** - This is the private key to access your remote server
* **user** - Change this to server's user account. (AWS default for Ubuntu Server is **ubuntu**)
* **127.0.0.1** - Change this to remote server's ip address

## What's Inside? :question::o::question:

This script runs on your local machine and connect to your remote server via ssh and execute commands.

Below is the simple bullet diagram about how this automation works. 

> 
* Deploy User - Create deploy user
  * create .ssh folder
  * copy```authorized_keys, id_rsa, id_rsa.pub``` from the **pem** folder and put it to **.ssh/** folder of your remote server
* Update Repositories
 * Add necessary sources then update and upgrade.
* PHP Installation
 * Includes the following 
>	
```
	php7.4-fpm 
	php7.4-common 
	php7.4-mbstring 
	php7.4-xmlrpc 
	php7.4-soap 
	php7.4-gd 
	php7.4-xml 
	php7.4-intl 
	php7.4-mysql 
	php7.4-cli 
	php7.4-zip 
	php7.4-curl 
	php7.4-imagick 
	php7.4-dev 
	php7.4-imap 
	php7.4-opcache 
	memcached
```
>
*  Nginx Installation
*  MariaDB Installation
*  Package Manager Installation
 *  Install Yarn
 *  Install Composer
*  Setup Nginx 
 *  create virtual host
 *  setup initial root directory
*  Restart All services


###### LAST NOTE:

Please feel free to use this simple automation and send me any comment or suggestions, file a bug or enhancments to make this project works for all of us.




----
**[MIT](LICENSE) LICENSE** <br>
copyright &copy; 2020 Scripts and Pixels.









