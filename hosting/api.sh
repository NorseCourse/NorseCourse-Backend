#!/bin/bash 
export PATH="/bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin/"

BOLD=$(tput bold)
NORMAL=$(tput sgr0)

echo "Subject: NorseCourse API production build complete"
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

# Copy the requirements over so any packages the server may need can be installed
cp /root/NorseCourse/NorseCourse-Backend/hosting/requirements.txt /var/www/norsecourse.com.api/

# Install the packages in the apps virtual environment
echo "${BOLD}Installing packages for the virtual environment${NORMAL}"
cd /var/www/norsecourse.com.api/
source API/venv/bin/activate
pip install -r requirements.txt
deactivate
echo

# Install the packages on the entire server, not sure why, but I found that it was necessary
echo "${BOLD}Installing packages system wide${NORMAL}"
pip install -r requirements.txt 
echo

# Copy the init file over and add the last two lines needed to run in production
cp /root/NorseCourse/NorseCourse-Backend/API/API/*.py /var/www/norsecourse.com.api/API/
echo -e "\n" >> /var/www/norsecourse.com.api/API/__init__.py
echo "if __name__ == \"__main__\":" >> /var/www/norsecourse.com.api/API/__init__.py
echo -e "\tapp.run()" >> /var/www/norsecourse.com.api/API/__init__.py

# Copy over all of the api files and other related files that are not __init__.py
# cd /root/NorseCourse/NorseCourse-Backend/API/API
# cp /root/NorseCourse/NorseCourse-Backend/API/API/[A-Za-z]*.py /var/www/norsecourse.com.api/API/
# cp courses.py departments.py divisions.py genEds.py NorseCourseObjects.py schedules.py sections.py terms.py /var/www/norsecourse.com.api/API/

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

sendmail "schabl01@luther.edu,norsecourse16@gmail.com" < ~/NorseCourse/Build/emailAPI.txt
