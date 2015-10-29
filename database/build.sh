export PATH="/bin:/usr/bin:/usr/local/bin:/sbin:/usr/sbin:/usr/local/sbin/"

echo "Subject: NorseCousre production build complete" 
echo
echo "BUILD LOG"
echo "-------------------------------------------------"

STARTTIME=$(date +"%Y-%m-%d %H:%M:%S")
echo "Start Time:" $STARTTIME
echo

cd ~/NorseCourse/NorseCourse-UI/

echo "git pull"
git pull


echo
echo "gulp build"
gulp build

cd ~/NorseCourse/NorseCourse-UI/dist/

cp -r js /usr/share/javascript/
cp -r css /var/www/html/
cp -r views /var/www/html/
sed -i 's/<script src="\/js\/main.js"><\/script>/<script src="javascript\/js\/main.js"><\/script>/' index.html
cp index.html /var/www/html/

ENDTIME=$(date +"%Y-%m-%d %H:%M:%S")
ENDTIMESEC=$(date -d"$ENDTIME" +%s)
STARTTIMESEC=$(date -d"$STARTTIME" +%s)
ELAPSEDTIME=`expr $ENDTIMESEC - $STARTTIMESEC `

echo
echo "End Time:" $ENDTIME
echo "Elapsed Time (sec):" $ELAPSEDTIME
echo "-------------------------------------------------"
echo
echo "Happy Hosting!"

sendmail schabl01@luther.edu < ~/NorseCourse/Build/email.txt
