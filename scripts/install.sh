sudo apt update && sudo apt upgrade -y
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10 -y
sudo curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
sudo python3.10 -m pip install --upgrade pip
sudo apt install -y build-essential libssl-dev libffi-dev
sudo apt install python3.10-venv
python3.10 -m venv .stack-exchange-venv
source .stack-exchange-venv/bin/activate
.stack-exchange-venv/bin/python3.10 -m pip install -r requirements.txt