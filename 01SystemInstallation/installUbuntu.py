# Install basic tools
sudo apt-get update
sudo apt-get install apache2
sudo apt-get install curl
sudo apt-get install wget
# Installs python relateds
wget http://peak.telecommunity.com/dist/ez_setup.py
sudo python ez_setup.py
sudo apt-get install python3-pip
sudo easy_install3 -U pip
sudo pip3 install tweepy
sudo pip3 install couchdb
sudo pip3 install jsonpickle
sudo pip3 install -U nltk
sudo pip3 install -U textblob
sudo apt-get update
#install CouchDB
sudo apt-get install couchdb
# Mount the formatted volume to make it part of the filesystem hierarchy
sudo mkfs.ext4 /dev/vdb
sudo mkdir /mnt/data
sudo mount /dev/vdb /mnt/data
sudo chown -R ubuntu /mnt/data
# Move couchdb data to volume
sudo mkdir /mnt/data/database
sudo mkdir /mnt/data/database/couchdb
sudo mkdir /mnt/data/database/couchview
sudo cp -R -p /var/lib/couchdb /mnt/data/database/couchdb
sudo chown -R couchdb:couchdb /mnt/data/database/couchdb
sudo chown -R couchdb:couchdb /mnt/data/database/couchview
# edit etc/couchdb default.ini bind address
sudo service couchdb restart
