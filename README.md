# NorseCourse: Backend

This section of the project is where to find code responsible for serving APIs used by the user interface. Additionally, this repo contains scripts for installing the entire application on a new server. By following the installation process below back and front end will be configured and operational.


## Installation

1. Login to your server (We used a Ubuntu server running 14.04)
2. Make sure your server is configured with a **[static ip address](https://www.youtube.com/results?search_query=ubuntu+server+static+ip)**
3. Install git if it isn't already: `sudo apt-get install -y git`
4. Execute the following commands and follow on-screen prompts when necessary:

```
sudo su
cd
mkdir NorseCourse
cd NorseCourse
git clone https://github.com/NorseCourse/NorseCourse-Backend.git
cd NorseCourse/NorseCourse-Backend/hosting/
./norseCourseWrapper.sh
```

*Test the installation. Enter the servers ip address for the UI or the servers ip address followed colon (:) port-you-chose into a web browser. You can also use the domain name you have one configured. For example, [norsecourse.com](https://norsecourse.com) and [norsecourse.com:5000](https://norsecourse.com:5000)*


[comment]: <##Usage>

[comment]: <TODO:WriteUsageInstructions>


## Contributing

1. Fork it!
2. Create your feature branch: `git checkout -b my-new-feature`
3. Commit your changes: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request :D


[comment]: <##History>

[comment]: <TODO:WriteHistory> 


## Credits

* Blaise Schaeffer, Luther College '16
* Grant Barnes, Luther College '16
* John Doorenbos, Luther College '16
* Michael Moore, Luther College '16


[comment]: <##License>

[comment]: <TODO:WriteLicense>