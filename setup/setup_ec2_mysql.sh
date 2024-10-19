#!/bin/bash

# Run using the below command
# bash setup_vm.sh

echo "Initializing the password variable"
read -sp "Press ENTER as your password for MySQL: " mysqlpswd

echo "Installing MySQL..."
sudo apt install mysql-server -y

echo "mysql version..."
mysql --version

echo "enable MySQL to automatically start at boot time...."
sudo systemctl enable mysql 

echo "start the MySQL database server...."
sudo systemctl start mysql 

echo "view the MySQL database server status...."
sudo systemctl status mysql

echo "Log in to the MySQL database server as root...."
sudo mysql -u root -pmysqlpswd

echo "Change root user password..."
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'root';
