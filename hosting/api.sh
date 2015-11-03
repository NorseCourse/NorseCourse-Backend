#!/bin/bash 
export PATH="/bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin/"

echo "Subject: NorseCourse API production build complete"
echo
echo "BUILD LOG"
echo "-------------------------------------------------"

STARTTIME=$(date +"%Y-%m-%d %H:%M:%S")
echo "Start Time:" $STARTTIME
echo

# cd into the clone of the backend directory that the root owns amd grab the most uptodated code
cd /root/NorseCourse/NorseCourse-Backend
echo "git pull"
git pull
echo 

# Copy the requirements over so any packages the server may need can be installed
cp /root/NorseCourse/NorseCourse-Backend/hosting/requirements.txt /var/www/norsecourse.com.api/

# Install the packages in the apps virtual environment
echo "Installing packages for the virtual environment"
cd /var/www/norsecourse.com.api/
source API/venv/bin/activate
pip install -r requirements.txt
deactivate
echo

# Install the packages on the entire server, not sure why, but I found that it was necessary
echo "Installing packages system wide"
pip install -r requirements.txt 
echo

# Copy the init file over and add the last two lines needed to run in production
cp /root/NorseCourse/NorseCourse-Backend/API/API/__init__.py /var/www/norsecourse.com.api/API
echo -e "\n" >> /var/www/norsecourse.com.api/API/__init__.py
echo "if __name__ == \"__main__\":" >> /var/www/norsecourse.com.api/API/__init__.py
echo -e "\tapp.run()" >> /var/www/norsecourse.com.api/API/__init__.py

# Copy over all of the api files
cd /root/NorseCourse/NorseCourse-Backend/API/API
cp courses.py departments.py divisions.py genEds.py NorseCourseObjects.py schedules.py sections.py terms.py /var/www/norsecourse.com.api/API/

echo "Restarting Apache2"
service apache2 restart
echo

ENDTIME=$(date +"%Y-%m-%d %H:%M:%S")
ENDTIMESEC=$(date -d"$ENDTIME" +%s)
STARTTIMESEC=$(date -d"$STARTTIME" +%s)
ELAPSEDTIME=`expr $ENDTIMESEC - $STARTTIMESEC `

echo "End Time:" $ENDTIME
echo "Elapsed Time (sec):" $ELAPSEDTIME
echo "-------------------------------------------------"
echo
echo "Happy Hosting!"

sendmail "schabl01@luther.edu,norsecourse16@gmail.com" < ~/NorseCourse/Build/emailAPI.txt
