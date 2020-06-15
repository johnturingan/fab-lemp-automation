"""
Machine Enviroment Setup Automation
Version 1.0
usage: fab -i pem/project.pem -H=ubuntu@127.0.0.1 init
"""


import os
from invoke import task
import json

local_path = os.path.realpath(os.getcwd())

with open('env.json') as f:
    env = json.load(f)

webEnv = env['web_setup']



@task
def init(c):


    try:
        deploy_user(c)
    except:
        pass

    update_repositories(c)

    php_installation(c)
    server_installation(c)
    package_manager_installation(c)

    setup_web_directory(c)
    setup_nginx(c)

    configure_services(c)

    restart(c)



@task
def deploy_user(c):
    banner('Preparing deploy user', 'header')

    banner('Add deploy user')
    c.sudo('adduser deploy')
    c.sudo('usermod -aG sudo deploy')

    banner('Creating .ssh folder in deploy user')
    c.sudo('mkdir -p /home/deploy/.ssh')

    banner('Uploading ssh keys from local to remote /tmp/folder', 'header')

    c.put(local_path + '/ssh/authorized_keys', '/tmp/authorized_keys')
    c.put(local_path + '/ssh/id_rsa', '/tmp/id_rsa')
    c.put(local_path + '/ssh/id_rsa.pub', '/tmp/id_rsa.pub')

    banner('Moving ssh keys to deploy .ssh folder', 'header')

    c.sudo('mv /tmp/authorized_keys /home/deploy/.ssh/authorized_keys')
    c.sudo('mv /tmp/id_rsa /home/deploy/.ssh/id_rsa')
    c.sudo('mv /tmp/id_rsa.pub /home/deploy/.ssh/id_rsa.pub')

    banner('Changing permission and owner')
    c.sudo('chmod 0600 /home/deploy/.ssh/ -R')
    c.sudo('chmod 0700 /home/deploy/.ssh/')
    c.sudo('chown deploy:deploy /home/deploy/.ssh/ -R')

    c.run("echo 'deploy ALL=(ALL) NOPASSWD:ALL' | sudo EDITOR='tee -a' visudo")

@task
def update_repositories(c):
    banner('Updating Repositories', 'header')

    banner('Downloading necessary sources')
    c.run('curl -sL https://deb.nodesource.com/setup_10.x -o nodesource_setup.sh')
    c.run('curl -sS https://dl.yarnpkg.com/debian/pubkey.gpg | sudo apt-key add -')
    c.sudo('echo "deb https://dl.yarnpkg.com/debian/ stable main" | sudo tee /etc/apt/sources.list.d/yarn.list')
    c.sudo('apt-get install software-properties-common')
    c.sudo('apt-get update -y')
    c.sudo('apt-get upgrade -y')

@task
def php_installation(c):
    banner('Installing PHP', 'header')
    c.sudo('apt-get install -y '
           'php7.4-fpm '
           'php7.4-common '
           'php7.4-mbstring '
           'php7.4-xmlrpc '
           'php7.4-soap '
           'php7.4-gd '
           'php7.4-xml '
           'php7.4-intl '
           'php7.4-mysql '
           'php7.4-cli '
           'php7.4-zip '
           'php7.4-curl '
           'php7.4-imagick '
           'php7.4-dev '
           'php7.4-imap '
           'php7.4-opcache '
           'memcached')

@task
def server_installation(c):

    banner('Installing Servers', 'header')
    c.sudo('apt-get install -y nginx')
    c.sudo('apt-get install -y mariadb-server')

@task
def package_manager_installation(c):
    banner('Installing Package Managers', 'header')
    c.sudo('bash nodesource_setup.sh ')
    c.sudo('apt-get install -y yarn')
    c.sudo('apt-get install -y composer')

@task
def setup_web_directory(c):
    banner('Setting up web directories')
    c.sudo('mkdir -p /srv/http/cms')
    c.sudo('mkdir -p /srv/http/web')
    c.sudo('mkdir -p /srv/http/api')
    c.sudo('mkdir -p /srv/http/' + webEnv['type'] + '/' + webEnv['project_name'])
    banner('Writing initial php file')
    c.sudo('echo "Hello ' + webEnv['project_name'] + '" | sudo tee  /srv/http/' + webEnv['type'] + '/' + webEnv['project_name'] + '/index.php')
    c.sudo('chown deploy:deploy /srv/ -R')

@task
def setup_nginx(c):

    banner('Setting up NGINX', 'header')

    banner('Create log files')
    c.sudo('touch /var/log/nginx/' + webEnv['nginx']['log_name']['error'])
    c.sudo('touch /var/log/nginx/' + webEnv['nginx']['log_name']['access'])

    banner('Upload nginx site-available file to tmp')
    print(local_path + webEnv['nginx']['template_path'] + webEnv['nginx']['template'])

    c.put(
        local_path + webEnv['nginx']['template_path'] + webEnv['nginx']['template'],
        '/tmp/' + webEnv['nginx']['template']
    )

    print('cleaning sites-enabled to avoid error')
    c.sudo('rm -rf /etc/nginx/sites-enabled/' + webEnv['nginx']['template'])

    banner('Moving nginx file to sites-available')
    c.sudo(
        'mv /tmp/' + webEnv['nginx']['template'] + ' ' +
        '/etc/nginx/sites-available/' + webEnv['nginx']['template']
    )

    banner('Creating symbolic link for site-enabled')
    c.sudo('ln -s /etc/nginx/sites-available/' + webEnv['nginx']['template'] + ' /etc/nginx/sites-enabled/' + webEnv['nginx']['template'])
    c.sudo('chown root:root /etc/nginx/sites-available/' + webEnv['nginx']['template'])

@task
def configure_services(c):

    banner('Configuring Services')
    banner('Configuring MariaDB ...')

    c.sudo('sed -ie "s/.*bind-address.*/bind-address = 0.0.0.0/" /etc/mysql/mariadb.conf.d/50-server.cnf')

    banner('Configuring MariaDB Done')
    banner('Configuring PHP ...')

    c.sudo('sed -ie "s/.*user = .*/user = deploy/" /etc/php/7.4/fpm/pool.d/www.conf ')
    c.sudo('sed -ie "s/.*group = .*/group = deploy/" /etc/php/7.4/fpm/pool.d/www.conf ')
    c.sudo('sed -ie "s/.*listen = .*/listen = 127.0.0.1:9000/" /etc/php/7.4/fpm/pool.d/www.conf ')

    banner('Configuring PHP Done')
    banner('Configuring Nginx ...')

    c.sudo('sed -ie "s/.*user .*/user deploy;/" /etc/nginx/nginx.conf ')

    banner('Configuring Nginx Done')

def restart(c):
    banner('restarting services!')

    c.sudo('service nginx restart')
    c.sudo('service php7.4-fpm restart')
    c.sudo('service mysql restart')



def banner (message, type = 'message'):

    if type == 'header':
        print("\n")
        print("************************************************")
        print(message)
        print("************************************************")
        print("\n")
    else:
        print(">>>>>>>>>>  " + message + "  <<<<<<<<<<<")

