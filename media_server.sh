#!/usr/bin/env bash
# TODO: make service for auto  start
sudo /etc/init.d/plexmediaserver start
sudo systemctl daemon-reload
sudo service apache2 restart