#!/bin/sh

export DEBIAN_FRONTEND=noninteractive

echo "==> Cleaning tmp"
rm -rf /tmp/*

echo "==> Cleaning APT"
sudo apt-get -y autoremove --purge \
    && sudo apt-get -y clean \
    && sudo apt-get -y autoclean
