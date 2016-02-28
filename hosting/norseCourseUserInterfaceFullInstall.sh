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
echo "${BOLD}Beginning Front End Installation...${NORMAL}"
echo

echo "${BOLD}Running apt-get update and upgrade...${NORMAL}"
apt-get update
apt-get upgrade
echo "${BOLD}Finished running apt-get update and upgrade.${NORMAL}"
echo

echo "${BOLD}Installing Node.js and npm...${NORMAL}"
curl -sL https://deb.nodesource.com/setup_5.x | sudo -E bash -
apt-get install -y nodejs
echo "${BOLD}Finished installing Node.js and npm.${NORMAL}"
echo

echo "${BOLD}Installing GulpJS globally and updating its dependencies...${NORMAL}"
npm install -g gulp
npm install -g graceful-fs
npm install -g lodash
echo "${BOLD}Finished installing GulpJS globally and updating its dependencies.${NORMAL}"
echo

echo "${BOLD}Cloning NorseCourse User Interface Repo...${NORMAL}"
mkdir /root/NorseCourse
cd /root/NorseCourse
git clone https://github.com/NorseCourse/NorseCourse-UI.git
echo "${BOLD}Finished cloning NorseCourse User Interface Repo.${NORMAL}"
echo

echo "${BOLD}Building Front End...${NORMAL}"
cd /root/NorseCourse/NorseCourse-UI
npm install --unsafe-perm
echo -n "Enter root namespace web addres the API, for example, 'http://norsecourse.com:5000/api' then press [ENTER]: "
read apiRootNamespaceDirty
apiRootNamespaceClean=${apiRootNamespaceDirty//\//\\\/}
echo "$apiRootNamespaceClean" > /root/NorseCourse/NorseCourse-Backend/hosting/apiWebAddress.txt
sed -i "s/angular.module('norseCourse').constant('apiUrl', 'https:\/\/norsecourse.com:5000\/api');/angular.module('norseCourse').constant('apiUrl', '$apiRootNamespaceClean');/" /root/NorseCourse/NorseCourse-UI/src/app/constants.js
gulp build
mkdir /var/www/norsecourse.com
mkdir /var/www/norsecourse.com/public_html
cp -r /root/NorseCourse/NorseCourse-UI/dist/js/ /var/www/norsecourse.com/public_html/
cp -r /root/NorseCourse/NorseCourse-UI/dist/css/ /var/www/norsecourse.com/public_html/
cp -r /root/NorseCourse/NorseCourse-UI/dist/views/ /var/www/norsecourse.com/public_html/
cp -r /root/NorseCourse/NorseCourse-UI/images/ /var/www/norsecourse.com/public_html/
cp /root/NorseCourse/NorseCourse-UI/dist/index.html /var/www/norsecourse.com/public_html/
echo "${BOLD}Finished building Front End.${NORMAL}"
echo

echo "${BOLD}Create and activate Apache2 virtual host configuration...${NORMAL}"
rm /etc/apache2/sites-available/norsecourse.com.conf
touch /etc/apache2/sites-available/norsecourse.com.conf
echo "<VirtualHost *:80>" >> /etc/apache2/sites-available/norsecourse.com.conf
echo -n "Enter server admin's email address, then press [ENTER]: "
read serverAdmin
echo -e "\tServerAdmin $serverAdmin" >> /etc/apache2/sites-available/norsecourse.com.conf
echo -n "Enter server name, for example, norsecourse.com then press [ENTER]: "
read serverName
echo -e "\tServerName $serverName" >> /etc/apache2/sites-available/norsecourse.com.conf
echo -n "Enter server alias, for example, www.norsecourse.com then press [ENTER]: "
read serverAlias
echo -e "\tServerAlias $serverAlias" >> /etc/apache2/sites-available/norsecourse.com.conf
echo -e "\tDocumentRoot /var/www/norsecourse.com/public_html" >> /etc/apache2/sites-available/norsecourse.com.conf
echo "" >> /etc/apache2/sites-available/norsecourse.com.conf 
echo -e "\t# Uncomment the three following lines if you configure HTTPS" >> /etc/apache2/sites-available/norsecourse.com.conf
echo -e "\t#RewriteEngine On" >> /etc/apache2/sites-available/norsecourse.com.conf
echo -e "\t#RewriteCond %{HTTPS} off" >> /etc/apache2/sites-available/norsecourse.com.conf
echo -e "\t#RewriteRule (.*) https://%{HTTP_HOST}%{REQUEST_URI}" >> /etc/apache2/sites-available/norsecourse.com.conf
echo "" >> /etc/apache2/sites-available/norsecourse.com.conf 
echo -e "\tErrorLog \${APACHE_LOG_DIR}/error.log" >> /etc/apache2/sites-available/norsecourse.com.conf
echo -e "\tCustomLog \${APACHE_LOG_DIR}/access.log combined" >> /etc/apache2/sites-available/norsecourse.com.conf
echo "</VirtualHost>" >> /etc/apache2/sites-available/norsecourse.com.conf
echo "" >> /etc/apache2/sites-available/norsecourse.com.conf 
echo "# Uncomment the following virtual host if you want to cofigure HTTPS" >> /etc/apache2/sites-available/norsecourse.com.conf
echo "# You will also need to uncomment the three lines in the above virtual host" >> /etc/apache2/sites-available/norsecourse.com.conf
echo "# Additionally run 'a2enmod rewrite' and restart apache2" >> /etc/apache2/sites-available/norsecourse.com.conf
echo "" >> /etc/apache2/sites-available/norsecourse.com.conf 
echo "#<VirtualHost *:443>" >> /etc/apache2/sites-available/norsecourse.com.conf
echo -e "\t#ServerAdmin $serverAdmin" >> /etc/apache2/sites-available/norsecourse.com.conf
echo -e "\t#ServerName $serverName" >> /etc/apache2/sites-available/norsecourse.com.conf
echo -e "\t#ServerAlias $serverAlias" >> /etc/apache2/sites-available/norsecourse.com.conf
echo -e "\t#DocumentRoot " >> /etc/apache2/sites-available/norsecourse.com.conf
echo "" >> /etc/apache2/sites-available/norsecourse.com.conf 
echo -e "\t#ErrorLog \${APACHE_LOG_DIR}/error.log" >> /etc/apache2/sites-available/norsecourse.com.conf
echo -e "\t#CustomLog \${APACHE_LOG_DIR}/access.log combined" >> /etc/apache2/sites-available/norsecourse.com.conf
echo "" >> /etc/apache2/sites-available/norsecourse.com.conf 
echo -e "\t#SSLEngine on" >> /etc/apache2/sites-available/norsecourse.com.conf
echo -e "\t#SSLCertificateFile {path_to_cert.pem}" >> /etc/apache2/sites-available/norsecourse.com.conf
echo -e "\t#SSLCertificateKeyFile {path_to_privkey.pem}" >> /etc/apache2/sites-available/norsecourse.com.conf
echo -e "\t#SSLCertificateChainFile {path_to_chain.pem}" >> /etc/apache2/sites-available/norsecourse.com.conf
echo "#</VirtualHost>" >> /etc/apache2/sites-available/norsecourse.com.conf
a2dissite 000-default.conf
a2ensite norsecourse.com.conf
service apache2 restart
echo "${BOLD}Finished creating and activating Apache2 virtual host configuration.${NORMAL}"
echo

echo "${BOLD}Creating cronjob for nightly build at 3:30 AM, this can be altered by entering the command sudo crontab -e ...${NORMAL}"
touch /root/NorseCourse/NorseCourse-Backend/hosting/emailUI.txt
touch /root/NorseCourse/NorseCourse-Backend/hosting/tempCron
crontab -l > /root/NorseCourse/NorseCourse-Backend/hosting/tempCron
echo "30 3 * * * /root/NorseCourse/NorseCourse-Backend/hosting/api2.sh > /root/NorseCourse/NorseCourse-Backend/hosting/emailUI.txt" >> /root/NorseCourse/NorseCourse-Backend/hosting/tempCron
crontab /root/NorseCourse/NorseCourse-Backend/hosting/tempCron
rm /root/NorseCourse/NorseCourse-Backend/hosting/tempCron
echo "${BOLD}Finished creating cronjob for nightly build at 3:30 AM.${NORMAL}"
echo

echo "${BOLD}Finished Front End Installation. Happy Hosting!${NORMAL}"
echo "${BOLD}To test if the installation was successful enter the servers ip address into a web browser.${NORMAL}"
echo






















