# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "debian/contrib-jessie64"
  config.vm.synced_folder ".", "/vagrant"
  config.vm.network "forwarded_port", guest: 5432, host: 5432  # PostgreSQL
  config.vm.network "forwarded_port", guest: 8000, host: 8000  # Django development server

  config.vm.provision "shell", inline: <<-SHELL
    # Adds Node.js repos and runs apt-get update
    curl -sL https://deb.nodesource.com/setup_6.x|sudo -E bash -

    sudo apt-get install -y --upgrade \
        git imagemagick postgresql-9.4 postgresql-client-9.4 \
        nodejs python python-dev python-pip python-virtualenv \
        zlib1g-dev libpq-dev libldap2-dev libsasl2-dev libssl-dev \
        libjpeg62-turbo-dev libpng12-dev libtiff5-dev libfreetype6-dev

    sudo npm i -g bower
    sudo pip install --upgrade pip virtualenv wheel

    sudo -u vagrant bash -c "
        cd /vagrant
        [ -d 'virtualenv' ] || virtualenv --always-copy virtualenv
        source virtualenv/bin/activate
        pip install -r requirements.txt
        bower install
    "

    sudo -u postgres psql -c "CREATE USER modeemintternet WITH PASSWORD 'modeemintternet';"
    sudo -u postgres psql -c "ALTER USER modeemintternet CREATEDB;"
    sudo -u postgres psql -c "CREATE DATABASE modeemiuserdb ENCODING 'UTF8' OWNER modeemintternet;"
  SHELL
end
