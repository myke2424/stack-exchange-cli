sudo apt update && sudo apt upgrade -y
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10 -y
sudo apt install python3.10-distutils
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
sudo python3.10 -m pip install --upgrade pip
sudo apt install -y build-essential libssl-dev libffi-dev
sudo python3.10 -m pip install stack-exchange-cli