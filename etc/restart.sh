#!/bin/sh -e

/etc/init.d/celerybeat restart
/etc/init.d/celeryd restart
sudo /etc/init.d/httpd restart