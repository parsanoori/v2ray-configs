# My v2ray configs

## How to setup

1. Clone the repo.

2. Generate the `dh-params.pem` to the `{domestic, foreign}-server-nginx/certbot/conf` folders.

```
openssl dhparam -out ./domestic-server-nginx/certbot/conf/ssl-dhparams.pem 2048
openssl dhparam -out ./foreign-server-nginx/certbot/conf/ssl-dhparams.pem 2048
```

3. Change the `DOMESTICIP` and `DOMESTICDOMAIN` and `YOUREMAIL` in  the following files:

+ `./domestic-server-nginx/templates/default.conf.template`
+ `./domestic-server-nginx/templates/home.conf.template`
+ `./domestic-server-nginx/docker-compose.yml`

and `FOREIGNIP` and `FOREIGNDOMAIN` and `YOUREMAIL` in:

+ `./foreign-server-nginx/templates/default.conf.template`
+ `./foreign-server-nginx/templates/home.conf.template`
+ `./foreign-server-nginx/docker-compose.yml`
+ `./domestic-server-v2ray/config.json`

4. Choose good random 4 digit numbers for port numbers of trojan and dokodemo-door. Namely they are `TROJANPORT` and `DOKODEMOPORT`. Pay attention that these should be the same in each server. Set the in the following files:  

+ `./foreign-server-v2ray/config.json`
+ `./foreign-server-v2ray/docker-compose.yml`
+ `./foreign-server-nginx/templates/home.conf.template`

And on the other side:  

+ `./domestic-server-v2ray/config.json`
+ `./domestic-server-v2ray/docker-compose.yml`
+ `./domestic-server-nginx/templates/home.conf.template`

5. Use `uuidgen` to generate uuid for passwords of the users in files `./domestic-server-v2ray/config.json` and `./foreign-server-v2ray/config.json`. Also pay attention to set the `FOREIGNDOMAIN` and `AFOREIGNSERVERUSERPASSWORD` and `AFOREIGNSERVERUSER` accordingly.     

6. Comment out the second server block in `./domestic-server-nginx/templates/home.conf.template` and `./domestic-server-nginx/templates/home.conf.template`.

7. Copy the files to the `/srv` folder of of the servers.

8. Per each server do:

+ Run the docker-compose of the nginx servers. Which means running the following in the `./{foreign, domestic}-server-v2ray` folders.

```
sudo docker-compose up -d nginx
```

Run the certbot:

```
sudo docker-compose up certbot
```

Remove the comments on step 4 and run:

```
sudo docker-compose down && sudo docker-compose up -d nginx
```

9. Run the v2ray per each sever. Which means run the following in the folders `./domestic-server-v2ray` and `./foreign-server-v2ray`:  

```
sudo docker-compose up -d
```

10. Set the cronjob in the same folders:

```
crontab ./crontab
```

11. Use `./domestic-server-v2ray/confgen.py` to generate the configs on the domestic server.

12. Occasionally use `./domestic-server-v2ray/v2stat.py` to make sure the configs are not spread exponentially.

13. Pull up your middle finger to those who made this messy shit.


## Cloudflare

My suggested architecture as following:

```
freedom <-> foreign server <-> Cloudflare's CDN <-> domestic server <-> client
```

For this you just need to set you FOREIGNDOMAIN'S nameservers to Cloudflare's nameservers and enable be proxy for your subdomain.  

**Bonus point BUT sometimes necessiry**: Use the script `./cftest.py` to find the almost suitable Cloudflare's server. Then choose that ip for assigning it to the domain in `/etc/hosts`.  


### Features
 
+ The domestic server directs Iran's IPs and .ir domains to it's real internet interface. Hence internet banks work.  
+ Stats are stored on a period of 5 minutes  

### TODO

+ Make it more user friendly by using `envsubst`. So that the   
+ Automation of Bunos point using cronjob.
+ Shell script for minimal setup.


