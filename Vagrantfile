# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  # Choisissez votre image de base. Ici, nous utilisons une image Ubuntu 18.04.
  config.vm.box = "ubuntu/bionic64"
  
  # Configurer le réseau privé pour accéder à l'interface web via un navigateur sur l'hôte
  config.vm.network "private_network", type: "dhcp"

  # Provisionner la VM avec un script shell pour installer Docker et Docker Compose
  config.vm.provision "shell", inline: <<-SHELL
    # Installer Docker
    sudo apt-get update
    sudo apt-get install -y apt-transport-https ca-certificates curl software-properties-common
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
    sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
    sudo apt-get update
    sudo apt-get install -y docker-ce
    
    # Installer Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    # Ajouter l'utilisateur `vagrant` au groupe `docker` pour permettre l'exécution de Docker sans sudo
    sudo usermod -aG docker $USER
  SHELL
  
  # Montez votre répertoire de projet dans la VM pour faciliter le partage de fichiers
  config.vm.synced_folder ".", "/vagrant", type: "virtualbox"
end
