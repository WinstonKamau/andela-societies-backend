#!/bin/bash

# set -o errexit
set -o pipefail

RED=$(tput setaf 1)
GREEN=$(tput setaf 2)
YELLOW=$(tput setaf 3)
WHITE=$(tput setaf 7)

function checkDocker() {
    if [[ -n "$(which docker)" ]]; then
        echo "Docker installed"
    else
        installDocker
    fi
    
}

function installDocker() {
    if [[ -n "$(which brew)" ]]; then
        echo "${YELLOW}====> Installing docker version 18.03-ce${WHITE}"
        brew cask install https://raw.githubusercontent.com/Homebrew/homebrew-cask/4bbea3bf6e453b35079848e4f77c75d45ae38502/Casks/docker.rb
    else
        echo "${YELLOW}====> Installing brew${WHITE}"
        /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
        echo "${YELLOW}====> Installing docker version 18.03-ce${WHITE}"
        brew cask install https://raw.githubusercontent.com/Homebrew/homebrew-cask/4bbea3bf6e453b35079848e4f77c75d45ae38502/Casks/docker.rb
    fi
}

function checkPackages() {
    declare -a packages=("$@")
    for package in "${packages[@]}"; do
        if [[ -n "$(which ${package})" ]]; then
            echo "${package} installed"
        else
            install "${package}"
        fi
    done
}

function install {
    case $1 in
        "kubectl")
            brew install https://raw.githubusercontent.com/Homebrew/homebrew-core/357ba36ac39a9a60f2a53e9452db8ad3e305e7bc/Formula/kubernetes-cli.rb ;;
        "brew")
            echo "${YELLOW}====> Installing brew${WHITE}"
            /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)";;
        "minikube")
            brew cask install https://raw.githubusercontent.com/Homebrew/homebrew-cask/a9c48c546066b4846ff8c73655634e96b645ed2d/Casks/minikube.rb;;
        "docker")
            brew cask install https://raw.githubusercontent.com/Homebrew/homebrew-cask/4bbea3bf6e453b35079848e4f77c75d45ae38502/Casks/docker.rb;;
        "virtualbox")
            brew cask install https://raw.githubusercontent.com/Homebrew/homebrew-cask/2213260d720c1f3128d801309a57d9a1a82facd2/Casks/virtualbox.rb;;
        *)
            echo "${RED}====> Invalid option selected${WHITE}"
    esac
}

function checkFrontend() {
    if [ -n "$(docker container ps -q --filter "name=soc_frontend_1")" ];then
        echo "${GREEN}====> The Frontend application is running${WHITE}"
    else
        echo "${YELLOW}====> The Frontend application is not running"
        echo -e "You can either start it up or just view the backend alone.${WHITE}\\n"
    fi
}

function configureHosts() {
    IP="$2"
    HOST="$1"
    STATE=$(grep -c "${IP}\\t${HOST}" /etc/hosts)
    if [ "$STATE" -eq 1 ];then
        echo "${GREEN}====> Backend host ${HOST} already exists on this machine.${WHITE}"
    elif [ "$STATE" -gt 1 ]; then
        echo "${RED}====> More than one match for the host ${HOST} was found!${WHITE}"
    else
        echo "${YELLOW}====> Adding backend Host ${HOST}${WHITE}"
        sudo bash -c "echo -e \"${IP}\\t${HOST}\" >> /etc/hosts"
        echo "${GREEN}====> Host added${WHITE}"
    fi
}

"$@"
