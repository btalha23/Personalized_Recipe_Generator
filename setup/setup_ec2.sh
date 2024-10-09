#!/bin/bash

# Run using the below command
# bash setup_vm.sh

echo "Downloading anaconda..."
mkdir -p ../software && cd ~/software && \
wget https://repo.anaconda.com/archive/Anaconda3-2024.06-1-Linux-x86_64.sh

echo "Running anaconda script..."
bash ~/software/Anaconda3-2024.06-1-Linux-x86_64.sh

echo "Removing anaconda script..."
rm ~/software/Anaconda3-2024.06-1-Linux-x86_64.sh

echo "Deactivating conda at startup..."
conda config --set auto_activate_base false

echo "Running sudo apt-get update..."
sudo apt update

echo "Installing Docker..."
sudo apt install docker.io

echo "Docker without sudo setup..."
sudo groupadd docker
sudo gpasswd -a ${USER} docker
sudo service docker restart

echo "Installing docker-compose..."
cd ~/software && wget https://github.com/docker/compose/releases/download/v2.29.2/docker-compose-linux-x86_64 -O docker-compose && \
sudo chmod +x docker-compose

echo "Setup .bashrc..."
echo '' >> ~/.bashrc
echo 'export PATH=${HOME}/software:${PATH}' >> ~/.bashrc
eval "$(cat ~/.bashrc | tail -n +10)"

echo "docker-compose version..."
docker-compose --version

echo "Installing AWS CLI..."
sudo apt install unzip
cd ~/software && curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && sudo ./aws/install

echo "aws cli version..."
aws --version

echo "Installing MySQL..."
cd ~/software && wget https://dev.mysql.com/get/mysql-apt-config_0.8.15-1_all.deb
sudo dpkg -i mysql-apt-config_0.8.15-1_all.deb

sudo apt update
sudo apt install -f mysql-client=8.0* mysql-community-server=8.0* mysql-server=8.0*
echo "aws cli version..."
mysql –V

mysqladmin -u root -p version

sudo systemctl start mysqld 
sudo systemctl enable mysqld 




echo "Activate conda environment..."
conda activate

echo "Making sure that python 3.11 is exploited in this project..."
conda install -c conda-forge python=3.11

echo "Installing necessary packages..."

pip install pandas numpy matplotlib seaborn wordcloud scikit-learn keras tabulate
pip install langchain langchain_community langchain_experimental langchain_openai langsmith openai
pip install streamlit streamlit_feedback
pip install mysql-connector-python sqlalchemy
pip install python-dotenv
