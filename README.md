## CU Mongol - PP Management

### 1. Ubuntu package -уудыг суулгах
    sudo apt-get install apache2
    sudo apt-get install mysql-server
    sudo apt-get install mysql-client
    sudo apt-get install libmysqlclient-dev
    sudo apt-get install python-pip
    sudo apt-get install python-dev
    sudo apt-get install libpq-dev
    sudo apt-get install libapache2-mod-wsgi-py3
    sudo apt-get install python3-pip

### 2. Create Database
    create database cupp character set utf8 collate utf8_unicode_ci;

### 3. Deploy хйих серверийн SSH key тохирруулах  
Gitlab repo-д имэйлээр хандалт олгосон байгаа бөгөөд,
[Repository Settings](https://gitlab.com/cumongol/cupp/settings/repository) -ийн Deploy Keys хэсэгт хандан серверийн public ssh key-ийг readonly эрхтэйгээр нэмж өгнө. 

### 4. Source code-ыг серверт clone хийх
    sudo mkdir /var/www/cupp
    sudo chmod 777 /var/www/cupp
    git clone git@gitlab.com:cumongol/cupp.git /var/www/cupp
    sudo mkdir /var/www/cupp/.store/media
    sudo chmod -R 777 /var/www/cupp/.store

### 5. /var/www/cupp/cupp/local_settings.py файл үүсгээд дараах утгуудыг тохируулах
    DB_HOST = 'localhost'
    DB_NAME = 'cupp'
    DB_USER = 'username'
    DB_PASSWORD = 'password'
    
### 6. Python package -уудыг суулгах 
    cd /var/www/cupp
    pip3 install -r requirements.txt

### 7. Django анхны горимын коммандуудыг ажиллуулах
    cd /var/www/cupp
    python3 manage.py resetdb // энэ комманд нь системийн бүх мэдээллийн устгаад шинээр үүсгэдэг тул дахин хэрэгдэхгүй байх
    python3 manage.py collectstatic
    python3 manage.py createsuperuser
    
    
### 8. Apache conf тохиргоо
    sudo vi /etc/apache2/sites-available/000-default.conf
```
<VirtualHost *:80>
    ServerName pp.cumongol.mn

    DocumentRoot /var/www/cupp

    WSGIDaemonProcess pp.cumongol.mn processes=5 threads=10 display-name=%{GROUP} python-path=/var/www/cupp/
    WSGIProcessGroup pp.cumongol.mn
    WSGIScriptAlias / /var/www/cupp/cupp/wsgi.py

    Alias /favicon.ico /var/www/cupp/.store/static/images/favicon.png
    Alias /static /var/www/cupp/.store/static
    Alias /media /var/www/cupp/.store/media

    <FilesMatch "\.(htaccess|htpasswd|ini|log|sh|inc|bak|xml)$">
        Order Allow,Deny
        Deny from all
    </FilesMatch>

    <Directory /var/www/cupp>
        WSGIApplicationGroup %{GLOBAL}
        Allow from All
    </Directory>
</VirtualHost>
```
    sudo service apache2 restart
    