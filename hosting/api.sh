#!/bin/bash 
export PATH="/bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin/"

if [ -t 1 ]; then
    BOLD=$(tput bold)
    NORMAL=$(tput sgr0)
else
    BOLD=$""
    NORMAL=$""
fi

echo "Subject: NorseCourse API Production Build Complete"
echo
echo "BUILD LOG"
echo "-------------------------------------------------"

STARTTIME=$(date +"%Y-%m-%d %H:%M:%S")
echo "${BOLD}Start Time:${NORMAL}" $STARTTIME
echo

# cd into the clone of the backend directory that the root owns amd grab the most uptodated code
cd /root/NorseCourse/NorseCourse-Backend
echo "${BOLD}git pull${NORMAL}"
git pull
echo 

# Copy the init file over and add the last two lines needed to run in production
cp /root/NorseCourse/NorseCourse-Backend/API/API/*.py /var/www/norsecourse.com.api/API/
echo -e "\n" >> /var/www/norsecourse.com.api/API/__init__.py
echo "if __name__ == \"__main__\":" >> /var/www/norsecourse.com.api/API/__init__.py
echo -e "\tapp.run()" >> /var/www/norsecourse.com.api/API/__init__.py

# Restart Apache2
echo "${BOLD}Restarting Apache2${NORMAL}"
service apache2 restart
echo

ENDTIME=$(date +"%Y-%m-%d %H:%M:%S")
ENDTIMESEC=$(date -d"$ENDTIME" +%s)
STARTTIMESEC=$(date -d"$STARTTIME" +%s)
ELAPSEDTIME=`expr $ENDTIMESEC - $STARTTIMESEC `

echo "${BOLD}End Time:${NORMAL}" $ENDTIME
echo "${BOLD}Elapsed Time (sec):${NORMAL}" $ELAPSEDTIME
echo "-------------------------------------------------"
echo
echo "Happy Hosting!"

if [ -t 1 ]; then
    echo "${BOLD}API BUILD IS COMPLETE${NORMAL}"
    echo
else
    sendmail "norsecourse16@gmail.com" < /root/NorseCourse/NorseCourse-Backend/hosting/emailAPI.txt
fi
