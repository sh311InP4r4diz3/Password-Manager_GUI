# Password-Manager_GUI
A GUI based Password Manager.



## Deployment![flow1](https://user-images.githubusercontent.com/103438798/209862741-e6943837-385b-4f67-bba3-3c18f5cc5aac.png)


Requirements:
MYSQL-Workbench(Windows), Mariadb-server(Linux), Python







## Installation

Installing MYSQL-Workbench on Windows

```
link to download: https://dev.mysql.com/downloads/ 
Installation video: https://www.youtube.com/watch?v=u96rVINbAUI
```
```
#Creating and granting privileges to the user, Using MYSQL Shell.

mysql> CREATE USER 'test'@'localhost' identified by 'password';

mysql> GRANT ALL PRIVILEGES on *.* to 'test'@'localhost';
```
Installing Mariadb-Server on Debian based Linux.

```
$sudo apt-get update && sudo apt-get upgrade -y
$sudo apt-get install mariadb-server -y
$sudo systemctl mysql start/stop    #start (or) stop the mysql server.
```
```
sudo mysql -u root -p

mariadb> CREATE USER 'test'@'localhost' identified by 'password';
mariadb> SHOW GRANTS FOR test@localhost;
mariadb> GRANT ALL PRIVILEGES on *.* to 'test'@'localhost';
```
Installing Python Modules
```
pip3 install pymysql
pip3 install cryptography
pip3 install pyperclip
pip3 install tkinter
```


## Usage/Examples

```python
$ ./pm_gui.py
python3 pm_gui.py
```


## Authors

- b00g3ym4n


## 🚀 About Me
I'm a Penetration tester, Python Programmer.


