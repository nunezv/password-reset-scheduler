#!/bin/bash
#Author: Joshua Kroger
#https://github.com/ProbieK/


length=$(shuf -i 64-128 -n 1)

password=$(strings - /dev/urandom | grep -o "[[:"graph":]]" | head -n "$length" | tr -d '\n')

# Add "--recipient KEY_FINGERPRINT" to the gpg command below for each user you wish to encrypt to
echo -e "$password" | gpg --recipient 12345678 --armour --encrypt
