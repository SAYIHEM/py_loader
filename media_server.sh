sudo /etc/init.d/plexmediaserver start
sudo systemctl daemon-reload
sudo service apache2 restart
python /home/pi/py_loader/main.py