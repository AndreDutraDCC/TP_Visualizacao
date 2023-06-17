#Some packages are only available for linux
#Run this on sudo mode to install dependencies:
#sudo bash requirements.sh

pip install phonemizer
apt-get install espeak

pip install flask

cd network_chart
git clone https://github.com/bhargavchippada/forceatlas2
cd forceatlas2
pip install . --user

cd ../..