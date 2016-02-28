#!/bin/bash 
export PATH="/bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin/"

if [ -t 1 ]; then
    BOLD=$(tput bold)
    NORMAL=$(tput sgr0)
else
    BOLD=$""
    NORMAL=$""
fi

echo "Subject: NorseCousre production build complete" 
echo
echo "BUILD LOG"
echo "-------------------------------------------------"

STARTTIME=$(date +"%Y-%m-%d %H:%M:%S")
echo "${BOLD}Start Time:${NORMAL}" $STARTTIME
echo

echo "${BOLD}git pull${NORMAL}"
cd /root/NorseCourse/NorseCourse-UI/
git pull
echo

echo "${BOLD}gulp build${NORMAL}"
cd /root/NorseCourse/NorseCourse-UI
npm install --unsafe-perm
apiRootNamespaceClean=""
while IFS='' read -r line || [[ -n "$line" ]]; do
	apiRootNamespaceClean=$line
done < /root/apiWebAddress.txt
sed -i "s/angular.module('norseCourse').constant('apiUrl', 'https:\/\/norsecourse.com:5000\/api');/angular.module('norseCourse').constant('apiUrl', '$apiRootNamespaceClean');/" /root/NorseCourse/NorseCourse-UI/src/app/constants.js
gulp build
cp -r /root/NorseCourse/NorseCourse-UI/dist/js/ /var/www/norsecourse.com/public_html/
cp -r /root/NorseCourse/NorseCourse-UI/dist/css/ /var/www/norsecourse.com/public_html/
cp -r /root/NorseCourse/NorseCourse-UI/dist/views/ /var/www/norsecourse.com/public_html/
cp -r /root/NorseCourse/NorseCourse-UI/images/ /var/www/norsecourse.com/public_html/
cp /root/NorseCourse/NorseCourse-UI/dist/index.html /var/www/norsecourse.com/public_html/

ENDTIME=$(date +"%Y-%m-%d %H:%M:%S")
ENDTIMESEC=$(date -d"$ENDTIME" +%s)
STARTTIMESEC=$(date -d"$STARTTIME" +%s)
ELAPSEDTIME=`expr $ENDTIMESEC - $STARTTIMESEC `

echo
echo "${BOLD}End Time:${NORMAL}" $ENDTIME
echo "${BOLD}Elapsed Time (sec):${NORMAL}" $ELAPSEDTIME
echo "-------------------------------------------------"
echo
echo "Happy Hosting!"

if [ -t 1 ]; then
    echo "${BOLD}UI BUILD IS COMPLETE${NORMAL}"
else
    sendmail "schabl01@luther.edu,norsecourse16@gmail.com" < ~/NorseCourse/Build/emailUI.txt
fi
