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

cd ~/NorseCourse/NorseCourse-UI/

echo "${BOLD}git pull${NORMAL}"
git pull


echo
echo "${BOLD}gulp build${NORMAL}"
gulp build

cd ~/NorseCourse/NorseCourse-UI/dist/

cp js/* /usr/share/javascript/norsecoursejs/
cp -r css /var/www/norsecourse.com/public_html/
cp -r views /var/www/norsecourse.com/public_html/
sed -i 's/<script src="\/js\/main.js"><\/script>/<script src="javascript\/norsecoursejs\/main.js"><\/script>/' index.html
cp index.html /var/www/norsecourse.com/public_html/

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
