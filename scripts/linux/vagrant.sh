#!/bin/sh

# Store build time
date > /etc/vagrant_box_build_time

# Install vagrant key
mkdir -pm 700 ~/.ssh
wget https://raw.githubusercontent.com/hashicorp/vagrant/main/keys/vagrant.pub -O ~/.ssh/authorized_keys \
    && chmod 0600 ~/.ssh/authorized_keys
