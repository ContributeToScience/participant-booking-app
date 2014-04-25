Install
=========

Fedora 64
---------

1. Update your system

::

    $ sudo yum update -y

If you're using root account you can avoid sudo, otherwise you need add your account to /etc/sudoers

2. Install the requirements

::

    $ sudo yum install wget git gcc python-devel python27 python27-devel httpd httpd-devel mod_wsgi mod_ssl mysql mysql-server mysql-devel -y

3. Clone project from github.com

::

    $ git clone https://github.com/ContributeToScience/participant-booking-app.git

This command will clone the project from github.com to current directory and create participant-booking-app directory.

4. Install virtualenv and create virtualenv

::

    $ sudo pip install virtualenv

How to install pip:

.. code-block:: c::

    $ wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
    $ sudo python get-pip.py

5. Install the requirements for project

.. code-block:: c::

    $ cd participant-booking-app/
    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt

6. Configure project settings

We can configure the system parameters in

In participant-booking-app/booking/booking/settings/production.py, we need to configure the project's settings.

.. code-block:: python::

    SECRET_KEY = get_env_setting('SECRET_KEY')

    ########## EMAIL CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
    EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.gmail.com')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
    EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
    EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'your_email@example.com')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
    EMAIL_PORT = environ.get('EMAIL_PORT', 587)

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
    EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
    EMAIL_USE_TLS = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
    SERVER_EMAIL = EMAIL_HOST_USER
    ########## END EMAIL CONFIGURATION

    # If you want to use amazon ses to send email
    ########## EMAIL CONFIGURATION
    # See: https://github.com/hmarr/django-ses
    #DEFAULT_FROM_EMAIL = 'bookingapp123@gmail.com'
    #AWS_ACCESS_KEY_ID = get_env_setting('AWS_ACCESS_KEY_ID')
    #AWS_SECRET_ACCESS_KEY = get_env_setting('AWS_SECRET_ACCESS_KEY')
    #EMAIL_BACKEND = 'django_ses.SESBackend'
    # Additionally, you can specify an optional region, like so:
    #AWS_SES_REGION_NAME = 'us-east-1'
    #AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
    #EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME
    ########## END EMAIL CONFIGURATION

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': get_env_setting('RDS_DB_NAME'),
            'USER': get_env_setting('RDS_USERNAME'),
            'PASSWORD': get_env_setting('RDS_PASSWORD'),
            'HOST': get_env_setting('RDS_HOSTNAME'),
            'PORT': get_env_setting('RDS_PORT'),
        }
    }

    ALLOWED_HOSTS = [
        '127.0.0.1',
        # Your domain or ip
    ]

    PAYPAL_RECEIVER_EMAIL = environ.get('PAYPAL_RECEIVER_EMAIL', '')
    SITE_NAME = environ.get('SITE_NAME', 'booking')
    PAYPAL_API_USERNAME = environ.get('PAYPAL_API_USERNAME', '')
    PAYPAL_API_PASSWORD = environ.get('PAYPAL_API_PASSWORD', '')
    PAYPAL_API_SIGNATURE = environ.get('PAYPAL_API_SIGNATURE', '')
    PAYPAL_API_ENVIRONMENT = environ.get('PAYPAL_API_ENVIRONMENT', '')
    PAYPAL_APPLICTION_ID = environ.get('PAYPAL_APPLICTION_ID', '')
    PAYPAL_ACTION = environ.get('PAYPAL_ACTION', '')
    PAYPAL_SERVICE = environ.get('PAYPAL_SERVICE', '')

    TWILIO_ACCOUNT_SID = environ.get('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = environ.get('TWILIO_AUTH_TOKEN', '')
    TWILIO_FROM_NUMBER = environ.get('TWILIO_FROM_NUMBER', '')

    # MAX LENGTH 32 BYTE
    ENCRYPT_KEY = environ.get('ENCRYPT_KEY', '')

You can edit the ~/.bashrc to export these parameters, for example:

.. code-block:: c::

    export SECRET_KEY=r"qipu176jbf8661i32p58fyqe&%$P[132u1v"
    # db configurations
    export RDS_DB_NAME=booking
    export RDS_USERNAME=booking
    export RDS_PASSWORD=password
    export RDS_HOSTNAME=localhost
    export RDS_PORT=3306

7. Create mysql database and configure

.. code-block:: mysql::

    $ sudo service mysqld start
    $ mysql -u root -p
    mysql> CREATE DATABASE <RDS_USERNAME> CHARACTER SET utf8;
    mysql> GRANT ALL PRIVILEGES ON <RDS_USERNAME>.* TO "<RDS_USERNAME>"@"<RDS_HOSTNAME>" IDENTIFIED BY "<RDS_PASSWORD>";
    mysql> FLUSH PRIVILEGES;
    mysql> EXIT;

::

    sudo vi /etc/my.cnf

Add content as below:

.. code-block:: mysql::

    [mysqld]
    init_connect='SET NAMES utf8'
    [client]
    default-character-set=utf8

Create database and load data

.. code-block:: c::

    $ cd participant-booking-app/booking
    $ python manage.py syncdb --settings=booking.settings.production
    $ python manage.py migrate --settings=booking.settings.production
    $ python manage.py loaddata fixtures/*.json --settings=booking.settings.production

8. Other settings

Collect static files

::

    $ python manage.py collectstatic --settings=booking.settings.production

9. Configure apache httpd

::

    sudo vi /etc/httpd/conf.d/wsgi.conf

.. code-block:: c::

    #----------Begin----------#

    SetEnv SECRET_KEY qipu176jbf8661i32p58fyqe&%$P[132u1v

    # db configurations
    SetEnv RDS_DB_NAME booking
    SetEnv RDS_USERNAME booking
    SetEnv RDS_PASSWORD password
    SetEnv RDS_HOSTNAME localhost
    SetEnv RDS_PORT 3306

    LoadModule wsgi_module modules/mod_wsgi.so
    WSGISocketPrefix /var/run/wsgi
    WSGIDaemonProcess booking python-path=/home/jeffrey/participant-booking-app/env/lib64/python2.7/site-packages/
    WSGIProcessGroup booking
    WSGIScriptAlias / /home/jeffrey/participant-booking-app/booking/booking/wsgi.py
    WSGIPassAuthorization On
    Alias /static/ /home/jeffrey/participant-booking-app/booking/assets/
    Alias /media/ /home/jeffrey/participant-booking-app/booking/media/
    #-----------End-----------#

If you get some errors caused by SELinux, you can disable this service.

::

    $ sudo vi /etc/selinux/config

    SELINUX=disabled


Debian 7
--------
If you account didn't in sudoers, you can ask root user add you with:

::

    adduser <your_user_name> sudo


1. Update your system

::

    $ sudo apt-get update
    $ sudo apt-get upgrade


2. Install the software

::

    sudo apt-get install wget git gcc python python-dev apache2 libapache2-mod-wsgi mysql libmysqlclient-dev libbz2-dev apache2-threaded-dev

3. Clone project from github.com

::

    $ git clone https://github.com/ContributeToScience/participant-booking-app.git

This command will clone the project from github.com to current directory and create participant-booking-app directory.

4. Install virtualenv and create virtualenv

::

    $ sudo pip install virtualenv

How to install pip:

.. code-block:: c::

    $ wget https://raw.github.com/pypa/pip/master/contrib/get-pip.py
    $ sudo python get-pip.py

5. Install the requirements for project

.. code-block:: c::

    $ cd participant-booking-app/
    $ virtualenv env
    $ source env/bin/activate
    $ pip install -r requirements.txt

6. Configure project settings

We can configure the system parameters in

In participant-booking-app/booking/booking/settings/production.py, we need to configure the project's settings.

.. code-block:: python::

    SECRET_KEY = get_env_setting('SECRET_KEY')

    ########## EMAIL CONFIGURATION
    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host
    EMAIL_HOST = environ.get('EMAIL_HOST', 'smtp.gmail.com')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-password
    EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD', '')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-host-user
    EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER', 'your_email@example.com')

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-port
    EMAIL_PORT = environ.get('EMAIL_PORT', 587)

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
    EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-use-tls
    EMAIL_USE_TLS = True

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#server-email
    SERVER_EMAIL = EMAIL_HOST_USER
    ########## END EMAIL CONFIGURATION

    # If you want to use amazon ses to send email
    ########## EMAIL CONFIGURATION
    # See: https://github.com/hmarr/django-ses
    #DEFAULT_FROM_EMAIL = 'bookingapp123@gmail.com'
    #AWS_ACCESS_KEY_ID = get_env_setting('AWS_ACCESS_KEY_ID')
    #AWS_SECRET_ACCESS_KEY = get_env_setting('AWS_SECRET_ACCESS_KEY')
    #EMAIL_BACKEND = 'django_ses.SESBackend'
    # Additionally, you can specify an optional region, like so:
    #AWS_SES_REGION_NAME = 'us-east-1'
    #AWS_SES_REGION_ENDPOINT = 'email.us-east-1.amazonaws.com'

    # See: https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
    #EMAIL_SUBJECT_PREFIX = '[%s] ' % SITE_NAME
    ########## END EMAIL CONFIGURATION

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': get_env_setting('RDS_DB_NAME'),
            'USER': get_env_setting('RDS_USERNAME'),
            'PASSWORD': get_env_setting('RDS_PASSWORD'),
            'HOST': get_env_setting('RDS_HOSTNAME'),
            'PORT': get_env_setting('RDS_PORT'),
        }
    }

    ALLOWED_HOSTS = [
        '127.0.0.1',
        # Your domain or ip
    ]

    PAYPAL_RECEIVER_EMAIL = environ.get('PAYPAL_RECEIVER_EMAIL', '')
    SITE_NAME = environ.get('SITE_NAME', 'booking')
    PAYPAL_API_USERNAME = environ.get('PAYPAL_API_USERNAME', '')
    PAYPAL_API_PASSWORD = environ.get('PAYPAL_API_PASSWORD', '')
    PAYPAL_API_SIGNATURE = environ.get('PAYPAL_API_SIGNATURE', '')
    PAYPAL_API_ENVIRONMENT = environ.get('PAYPAL_API_ENVIRONMENT', '')
    PAYPAL_APPLICTION_ID = environ.get('PAYPAL_APPLICTION_ID', '')
    PAYPAL_ACTION = environ.get('PAYPAL_ACTION', '')
    PAYPAL_SERVICE = environ.get('PAYPAL_SERVICE', '')

    TWILIO_ACCOUNT_SID = environ.get('TWILIO_ACCOUNT_SID', '')
    TWILIO_AUTH_TOKEN = environ.get('TWILIO_AUTH_TOKEN', '')
    TWILIO_FROM_NUMBER = environ.get('TWILIO_FROM_NUMBER', '')

    # MAX LENGTH 32 BYTE
    ENCRYPT_KEY = environ.get('ENCRYPT_KEY', '')

You can edit the ~/.bashrc to export these parameters, for example:

.. code-block:: c::

    export SECRET_KEY=r"qipu176jbf8661i32p58fyqe&%$P[132u1v"
    # db configurations
    export RDS_DB_NAME=booking
    export RDS_USERNAME=booking
    export RDS_PASSWORD=password
    export RDS_HOSTNAME=localhost
    export RDS_PORT=3306

7. Create mysql database and configure

.. code-block:: mysql::

    $ sudo service mysql start
    $ mysql -u root -p
    mysql> CREATE DATABASE <RDS_USERNAME> CHARACTER SET utf8;
    mysql> GRANT ALL PRIVILEGES ON <RDS_USERNAME>.* TO "<RDS_USERNAME>"@"<RDS_HOSTNAME>" IDENTIFIED BY "<RDS_PASSWORD>";
    mysql> FLUSH PRIVILEGES;
    mysql> EXIT;

::

    sudo vi /etc/mysql/my.cnf

Add content as below:

.. code-block:: mysql::

    [mysqld]
    init_connect='SET NAMES utf8'
    [client]
    default-character-set=utf8

    $ sudo service mysql start

Create database and load data

.. code-block:: c::

    $ cd participant-booking-app/booking
    $ python manage.py syncdb --settings=booking.settings.production
    $ python manage.py migrate --settings=booking.settings.production
    $ python manage.py loaddata fixtures/*.json --settings=booking.settings.production

8. Other settings

Collect static files

::

    $ python manage.py collectstatic --settings=booking.settings.production

9. Configure apache httpd

::

    sudo a2enmod wsgi
    sudo gedit /etc/apache2/mod-available/wsgi.conf

.. code-block:: c::

    #----------Begin----------#

    SetEnv SECRET_KEY qipu176jbf8661i32p58fyqe&%$P[132u1v

    # db configurations
    SetEnv RDS_DB_NAME booking
    SetEnv RDS_USERNAME booking
    SetEnv RDS_PASSWORD password
    SetEnv RDS_HOSTNAME localhost
    SetEnv RDS_PORT 3306

    LoadModule wsgi_module modules/mod_wsgi.so
    WSGISocketPrefix /var/run/wsgi
    WSGIDaemonProcess booking python-path=/home/jeffrey/participant-booking-app/env/lib/python2.7/site-packages/
    WSGIProcessGroup booking
    WSGIScriptAlias / /home/jeffrey/participant-booking-app/booking/booking/wsgi.py
    WSGIPassAuthorization On
    Alias /static/ /home/jeffrey/participant-booking-app/booking/assets/
    Alias /media/ /home/jeffrey/participant-booking-app/booking/media/
    #-----------End-----------#
