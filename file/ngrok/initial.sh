#!/bin/sh
mkdir ~/Desktop/Ngrok
cp ./ngrok.cfg ~/Desktop/Ngrok/ngrok.cfg
cp ./server.sh ~/Desktop/Ngrok/server.sh
cp ./client.sh ~/Desktop/Ngrok/client.sh
cd ~/Desktop
git clone https://github.com/tutumcloud/ngrok.git ngrok
cd ngrok
NGROK_DOMAIN="www.bear-services.com" 
openssl genrsa -out base.key 2048 
openssl req -new -x509 -nodes -key base.key -days 10000 -subj "/CN=$NGROK_DOMAIN" -out base.pem 
openssl genrsa -out server.key 2048 
openssl req -new -key server.key -subj "/CN=$NGROK_DOMAIN" -out server.csr 
openssl x509 -req -in server.csr -CA base.pem -CAkey base.key -CAcreateserial -days 10000 -out server.crt
cp base.pem assets/client/tls/ngrokroot.crt
cp server.crt assets/server/tls/snakeoil.crt
cp server.key assets/server/tls/snakeoil.key
sudo make release-server release-client
cd ..
cp ./ngrok/bin/ngrok ./Ngrok/ngrok
cp ./ngrok/bin/ngrokd ./Ngrok/ngrokd
chmod 777 ./Ngrok/ngrok
chmod 777 ./Ngrok/ngrokd
cp ./ngrok/server.crt ./Ngrok/server.crt
cp ./ngrok/server.key ./Ngrok/server.key
exit

