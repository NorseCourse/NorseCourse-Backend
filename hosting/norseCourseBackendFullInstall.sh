#!/bin/bash 
export PATH="/bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin/"

if [ -t 1 ]; then
    BOLD=$(tput bold)
    NORMAL=$(tput sgr0)
else
    BOLD=$""
    NORMAL=$""
fi

echo "${BOLD}This script has to be run as the root user for everything to work properly${NORMAL}"
echo "${BOLD}Beginning Backend Installation...${NORMAL}"
echo

echo "${BOLD}Running apt-get update and upgrade...${NORMAL}"
apt-get update
apt-get upgrade -y
echo "${BOLD}Finished running apt-get update and upgrade.${NORMAL}"
echo

echo "${BOLD}Installing Apache2...${NORMAL}"
apt-get install -y apache2
echo "${BOLD}Finished installing Apache2.${NORMAL}"
echo

echo "${BOLD}Configuring global server name and data compression for Apache2...${NORMAL}"
echo "" >> /etc/apache2/apache2.conf
echo "# Setting Server Name Globally" >> /etc/apache2/apache2.conf
echo "serverName localhost" >> /etc/apache2/apache2.conf
echo "" >> /etc/apache2/apache2.conf
echo "# mod_deflate configurations" >> /etc/apache2/apache2.conf
echo "SetOutputFilter DEFLATE" >> /etc/apache2/apache2.conf
echo "${BOLD}Finished configuring data compression for Apache2.${NORMAL}"
echo

echo "${BOLD}Restarting Apache2...${NORMAL}"
service apache2 restart 
echo "${BOLD}Finished restarting Apache2.${NORMAL}"
echo

echo "${BOLD}Installing Git...${NORMAL}"
apt-get install -y git
echo "${BOLD}Finished installing Git.${NORMAL}"
echo

echo "${BOLD}Installing Python Pip (Version 3)...${NORMAL}"
apt-get install -y python3-pip
echo "${BOLD}Finished installing Python Pip (Version 3).${NORMAL}"
echo

echo "${BOLD}Installing Flask, flask-restplus, and pandas with pip3...${NORMAL}"
pip3 install Flask flask-restplus pandas
echo "${BOLD}Finished installing Flask and flask-restplus with pip3.${NORMAL}"
echo

echo "${BOLD}Installing mysql.connector...${NORMAL}"
wget http://dev.mysql.com/get/Downloads/Connector-Python/mysql-connector-python-py3_2.1.3-1ubuntu14.04_all.deb
dpkg -i mysql-connector-python-py3_2.1.3-1ubuntu14.04_all.deb
rm mysql-connector-python-py3_2.1.3-1ubuntu14.04_all.deb
echo "${BOLD}Finished installing mysql.connector.${NORMAL}"
echo

echo "${BOLD}Creating NorseCourse folder under /root/ and moving into it...${NORMAL}"
mkdir /root/NorseCourse
cd /root/NorseCourse
echo "${BOLD}Finished creating NorseCourse folder under /root/ and moving into it.${NORMAL}"
echo 

echo "${BOLD}Cloning NorseCourse Backend Repo...${NORMAL}"
git clone https://github.com/NorseCourse/NorseCourse-Backend.git
echo "${BOLD}Finished cloning NorseCourse Backend Repo.${NORMAL}"
echo

echo "${BOLD}Make Apache2 paths for serving the api...${NORMAL}"
mkdir /var/www/norsecourse.com.api/
mkdir /var/www/norsecourse.com.api/API
echo "${BOLD}Finished making Apache2 paths for serving the api.${NORMAL}"
echo

echo "${BOLD}Create API.wsgi file, this file will need to be opened manually and be configured further...${NORMAL}"
rm /var/www/norsecourse.com.api/API.wsgi
touch /var/www/norsecourse.com.api/API.wsgi
echo "#!/usr/bin/python" >> /var/www/norsecourse.com.api/API.wsgi                                                                                  
echo "import sys" >> /var/www/norsecourse.com.api/API.wsgi
echo "import logging" >> /var/www/norsecourse.com.api/API.wsgi
echo "logging.basicConfig(stream=sys.stderr)" >> /var/www/norsecourse.com.api/API.wsgi
echo 'sys.path.insert(0,"/var/www/norsecourse.com.api/")' >> /var/www/norsecourse.com.api/API.wsgi
echo "" >> /var/www/norsecourse.com.api/API.wsgi
echo "from API import app as application" >> /var/www/norsecourse.com.api/API.wsgi
echo -n "Enter a secret key for the appication, then press [ENTER]: "
read appSecretKey
echo "application.secret_key = '$appSecretKey'" >> /var/www/norsecourse.com.api/API.wsgi
echo "${BOLD}Finished creating API.wsgi file.${NORMAL}"
echo

echo "${BOLD}Copy contents from NorseCourse Backend folder to Apache2 folders and format init file...${NORMAL}"
cp /root/NorseCourse/NorseCourse-Backend/API/API/*.py /var/www/norsecourse.com.api/API/
echo -e "\n" >> /var/www/norsecourse.com.api/API/__init__.py
echo "if __name__ == \"__main__\":" >> /var/www/norsecourse.com.api/API/__init__.py
echo -e "\tapp.run()" >> /var/www/norsecourse.com.api/API/__init__.py
echo "${BOLD}Finished copying contents from NorseCourse Backend folder to Apache2 folders and formatting init file.${NORMAL}"
echo

echo "${BOLD}Creating config.py under /var/www/norsecourse.com.api/API/${NORMAL}"
rm /var/www/norsecourse.com.api/API/config.py
touch /var/www/norsecourse.com.api/API/config.py
echo "# Configuration file specifying how to connect to the MySQL server." >> /var/www/norsecourse.com.api/API/config.py                                      
echo "" >> /var/www/norsecourse.com.api/API/config.py
echo "# Configuration for initializing the database." >> /var/www/norsecourse.com.api/API/config.py                                                        
echo -n "Enter a database username for NorseCourse, we recommend using 'NorseCourse' and press [ENTER]: "
read databaseUsername
echo "init_db_config = {" >> /var/www/norsecourse.com.api/API/config.py
echo "    'user': '$databaseUsername'," >> /var/www/norsecourse.com.api/API/config.py
echo -n "Enter a password for this user and press [ENTER]: "
read databaseUserPassword
echo "    'password': '$databaseUserPassword'," >> /var/www/norsecourse.com.api/API/config.py
echo -n "Enter the the ip address of this server and press [ENTER]: "
read hostIpAddress
echo "    'host': '$hostIpAddress'," >> /var/www/norsecourse.com.api/API/config.py
echo "    'raise_on_warnings': True," >> /var/www/norsecourse.com.api/API/config.py
echo "}" >> /var/www/norsecourse.com.api/API/config.py
echo "" >> /var/www/norsecourse.com.api/API/config.py
echo "# Configuration for the connection pool." >> /var/www/norsecourse.com.api/API/config.py                                                                 
echo "# Database name needs to match the name typed in" >> /var/www/norsecourse.com.api/API/config.py                                                        
echo "# when initializeDB.py was ran." >> /var/www/norsecourse.com.api/API/config.py                                                                         
echo "db_pool_config = {" >> /var/www/norsecourse.com.api/API/config.py
echo "    'user': '$databaseUsername'," >> /var/www/norsecourse.com.api/API/config.py
echo "    'password': '$databaseUserPassword'," >> /var/www/norsecourse.com.api/API/config.py
echo "    'host': '$hostIpAddress'," >> /var/www/norsecourse.com.api/API/config.py
echo -n "Enter a database name, we recommend using NorseCourse here as well, then press [ENTER]: "
read databaseName
echo "    'database': '$databaseName'," >> /var/www/norsecourse.com.api/API/config.py
echo "    'raise_on_warnings': True," >> /var/www/norsecourse.com.api/API/config.py
echo "    'pool_name': 'norse_course_connection_pool'," >> /var/www/norsecourse.com.api/API/config.py
echo "    'pool_size': 32," >> /var/www/norsecourse.com.api/API/config.py
echo "    'pool_reset_session': True" >> /var/www/norsecourse.com.api/API/config.py
echo "}" >> /var/www/norsecourse.com.api/API/config.py
echo "${BOLD}Finished creating config file. Manually, you need to configure the config.py under /var/www/norsecourse.com.api/API/ this is not done automatically in the script for security purposes, and because it needs to be set up with your desired specifications. Restart Apache2 after you have done so with 'service apache2 restart'${NORMAL}"
echo

echo "${BOLD}Install and activate WSGI Mod for Apache2 (Python3 version)...${NORMAL}"
apt-get install libapache2-mod-wsgi-py3
a2enmod wsgi
echo "${BOLD}Finished installing and activating WSGI Mod for Apache2 (Python3 version).${NORMAL}"
echo

echo "${BOLD}Create and activate Apache2 virtual host configuration...${NORMAL}"
rm /etc/apache2/sites-available/norsecourse.com.api.conf
touch /etc/apache2/sites-available/norsecourse.com.api.conf
echo -n "Enter the port you wish to use for serving APIs, for example 5000, then press [ENTER]: "
read apiPort
echo "Listen $apiPort" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo "" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo "<VirtualHost *:$apiPort>" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo -n "Enter server admin's email address, then press [ENTER]: "
read serverAdmin
echo "        ServerAdmin $serverAdmin" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo -n "Enter server name, for example, norsecourse.com then press [ENTER]: "
read serverName
echo "        ServerName $serverName" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo -n "Enter server alias, for example, www.norsecourse.com then press [ENTER]: "
read ServerAlias
echo "        ServerAlias $ServerAlias" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo "" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo "#       Uncomment and configure for https" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo "#        SSLEngine on" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo "#        SSLCertificateFile {path_to_cert.pem}" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo "#        SSLCertificateKeyFile {path_to_privkey.pem}" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo "#        SSLCertificateChainFile {path_to_chain.pem}" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo "" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo "        WSGIScriptAlias / /var/www/norsecourse.com.api/API.wsgi" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo "        <Directory /var/www/norsecourse.com.api/API/>" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo "                   Order allow,deny" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo "                   Allow from all" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo "        </Directory>" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo "" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo -e "        ErrorLog \${APACHE_LOG_DIR}/error.log" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo -e "        CustomLog \${APACHE_LOG_DIR}/access.log combined" >> /etc/apache2/sites-available/norsecourse.com.api.conf
echo "</VirtualHost>" >> /etc/apache2/sites-available/norsecourse.com.api.conf
a2ensite norsecourse.com.api.conf
service apache2 restart
echo "${BOLD}Finished creating and activating Apache2 virtual host configuration.${NORMAL}"
echo

echo "${BOLD}Install MySQL Server, you will need to enter root user information...${NORMAL}"
apt-get install -y mysql-server
echo "${BOLD}Finished installing MySQL Server.${NORMAL}"
echo

echo "${BOLD}Installing sendmail for daily build notifications...${NORMAL}"
apt-get install -y sendmail
echo "${BOLD}Finished installing sendmail.${NORMAL}"
echo

echo "${BOLD}Creating cronjob for nightly build at 3:00 AM, this can be altered by entering the command sudo crontab -e ...${NORMAL}"
touch /root/NorseCourse/NorseCourse-Backend/hosting/emailAPI.txt
touch /root/NorseCourse/NorseCourse-Backend/hosting/tempCron
crontab -l > /root/NorseCourse/NorseCourse-Backend/hosting/tempCron
echo "0 3 * * * /root/NorseCourse/NorseCourse-Backend/hosting/api.sh > /root/NorseCourse/NorseCourse-Backend/hosting/emailAPI.txt" >> /root/NorseCourse/NorseCourse-Backend/hosting/tempCron
crontab /root/NorseCourse/NorseCourse-Backend/hosting/tempCron
rm /root/NorseCourse/NorseCourse-Backend/hosting/tempCron
echo "${BOLD}Finished creating cronjob for nightly build at 3:00 AM.${NORMAL}"
echo

echo "${BOLD}Configuring MySQL, create and initialize a database, and populate the database. Run as super user, execute sudo su and cd once:${NORMAL}"
echo -n "Enter the MySQL root user's password that you creted earlier, then press [ENTER]: "
read databaseRootUserPassword
mysql --user="root" --password="$databaseRootUserPassword" --execute="CREATE USER '$databaseUsername'@'%' IDENTIFIED BY '$databaseUserPassword'; FLUSH PRIVILEGES; GRANT ALL ON $databaseName.* TO '$databaseUsername'@'%'; FLUSH PRIVILEGES; "
sed -i "s/bind-address\t\t= 127.0.0.1/bind-address\t\t= $hostIpAddress/" /etc/mysql/my.cnf
sed -i 's/#max_connections        = 100/max_connections        = 10000/' /etc/mysql/my.cnf
service mysql stop
service mysql start
cp /var/www/norsecourse.com.api/API/config.py /root/NorseCourse/NorseCourse-Backend/database/
cd /root/NorseCourse/NorseCourse-Backend/database/
python3 /root/NorseCourse/NorseCourse-Backend/database/initializeDB.py
python3 /root/NorseCourse/NorseCourse-Backend/database/readCSV.py
python3 /root/NorseCourse/NorseCourse-Backend/database/populateDB.py
cd
echo "${BOLD}Finished configuring, creating, initializing, and populating the MySQL database.${NORMAL}"
echo

echo "${BOLD}Finished Backend Installation. Happy Hosting!${NORMAL}"
echo "${BOLD}To test if the installation was successful enter the servers ip address into a web browser followed by :$apiPort. Like this: $hostIpAddress:$apiPort ${NORMAL}"
echo