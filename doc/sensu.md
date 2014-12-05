# Install Sensu server dependencies

## Generating SSL certificates
```shell
which openssl
openssl version

wget http://sensuapp.org/docs/0.16/tools/ssl_certs.tar
tar -xvf ssl_certs.tar
cd ssl_certs
./ssl_certs.sh generate
```

## Installing RabbitMQ
### Step #1 - Install erlang
```shell
apt-get install erlang-nox
```

### Step #2 - Install RabbitMQ
```shell
wget http://www.rabbitmq.com/rabbitmq-signing-key-public.asc
apt-key add rabbitmq-signing-key-public.asc
echo "deb     http://www.rabbitmq.com/debian/ testing main" > /etc/apt/sources.list.d/rabbitmq.list
apt-get update
apt-get install rabbitmq-server
```

### Start the RabbitMQ server
```shell
update-rc.d rabbitmq-server defaults
/etc/init.d/rabbitmq-server start
```

### Step #1 - Install RabbitMQ certificate authority and certificates
```shell
mkdir -p /etc/rabbitmq/ssl
cp sensu_ca/cacert.pem /etc/rabbitmq/ssl
cp server/cert.pem /etc/rabbitmq/ssl
cp server/key.pem /etc/rabbitmq/ssl
```

### Step #2 - Configure the RabbitMQ SSL listener
```shell
/etc/rabbitmq/rabbitmq.config
[
    {rabbit, [
    {ssl_listeners, [5671]},
    {ssl_options, [{cacertfile,"/etc/rabbitmq/ssl/cacert.pem"},
                   {certfile,"/etc/rabbitmq/ssl/cert.pem"},
                   {keyfile,"/etc/rabbitmq/ssl/key.pem"},
                   {verify,verify_peer},
                   {fail_if_no_peer_cert,true}]}
  ]}
].

/etc/init.d/rabbitmq-server restart
```

### Step #1 - Create a RabbitMQ vhost for Sensu
```shell
rabbitmqctl add_vhost /sensu
```
### Step #2 - Create a RabbitMQ user with permissions for the Sensu vhost
```shell
rabbitmqctl add_user sensu mypass
rabbitmqctl set_permissions -p /sensu sensu ".*" ".*" ".*"
```
### [Optional] Enable the RabbitMQ web management console
```shell
rabbitmq-plugins enable rabbitmq_management
```

## Installing Redis
### Install Redis on Debian and Ubuntu
```shell
apt-get install redis-server
```

# Install Sensu

## Step #1 - Install the repository public key
```shell
wget -q http://repos.sensuapp.org/apt/pubkey.gpg -O- | sudo apt-key add -
```

## Step #2 - Add the repository
```shell
Main repository (stable).
echo "deb     http://repos.sensuapp.org/apt sensu main" > /etc/apt/sources.list.d/sensu.list

Or the unstable repository.
echo "deb     http://repos.sensuapp.org/apt sensu unstable" > /etc/apt/sources.list.d/sensu.list
```

## Step #3 - Install Sensu
```shell
apt-get update
apt-get install sensu
```

# Configure Sensu connections
```shell
mkdir -p /etc/sensu/ssl
cp client/cert.pem /etc/sensu/ssl/
cp client/key.pem /etc/sensu/ssl/

vi /etc/sensu/conf.d/rabbitmq.json
{
  "rabbitmq": {
    "ssl": {
      "cert_chain_file": "/etc/sensu/ssl/cert.pem",
      "private_key_file": "/etc/sensu/ssl/key.pem"
    },
    "host": "SUBSTITUTE_ME",
    "port": 5671,
    "vhost": "/sensu",
    "user": "sensu",
    "password": "SUBSTITUTE_ME"
  }
}

vi /etc/sensu/conf.d/redis.json
{
  "redis": {
    "host": "localhost",
    "port": 6379
  }
}
```

# Configure the Sensu API
```shell
vi /etc/sensu/conf.d/api.json
{
  "api": {
    "host": "localhost",
    "port": 4567,
    "user": "admin",
    "password": "secret"
  }
}
```

# Configure the Sensu clients
```shell
vi /etc/sensu/conf.d/client.json
{
  "client": {
    "name": "SUBSTITUTE_ME",
    "address": "SUBSTITUTE_ME",
    "subscriptions": [ "all" ]
  }
}
```

# Enable Sensu services
```shell
server
update-rc.d sensu-server defaults
update-rc.d sensu-client defaults
update-rc.d sensu-api defaults

client
update-rc.d sensu-client defaults
```

# Start Sensu services
```shell
server
/etc/init.d/sensu-server start
/etc/init.d/sensu-client start
/etc/init.d/sensu-api start

client
/etc/init.d/sensu-client start
```

# link
- [Guide](http://sensuapp.org/docs/0.16/guide)
- [SSL certificates](http://sensuapp.org/docs/0.16/certificates)
- [RabbitMQ](http://sensuapp.org/docs/0.16/rabbitmq)
- [Redis](http://sensuapp.org/docs/0.16/redis)
- [How To Configure Sensu Monitoring, RabbitMQ, and Redis on Ubuntu 14.04](https://www.digitalocean.com/community/tutorials/how-to-configure-sensu-monitoring-rabbitmq-and-redis-on-ubuntu-14-04)