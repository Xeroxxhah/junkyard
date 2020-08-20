#!/bin/bash
if [ $(id -u) != '0' ]
then
  echo 'This Script must be run as root'
  exit
else
  mkdir .PasSBox
  touch .PasSBox/users.txt
  echo 'Setup Sucessfull'
  echo 'Syntax: python3 PasSBox.py'
  echo 'Bug Report at xeroxxhah@pm.me'
fi
