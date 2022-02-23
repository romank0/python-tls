# Simple TLS connection

This example was tested under Ubuntu 18.04.2 with python 3.6.8.

Open the terminal and enter the following commands:

```bash
sudo apt install git -y
git clone https://github.com/arthurazs/python-tls
```

The first command install git, the second command downloads this repository.

## Self-signed certificate

### Generate the certificate and private key

Open the terminal and enter the following commands:

```bash
openssl req -new -x509 -days 365 -nodes -out cert.pem -keyout key.pem -subj "/C=BR/ST=Rio de Janeiro/L=Niteroi/O=UFF/OU=Midiacom/CN=example.org/emailAddress=arthurazs@midiacom.uff.br"
```

The first command changes the directory to the downloaded repository, the second command generates the certificate and private key.

Note that you can change some parameters:

- **C**, which is a 2 letter code for a country;
- **ST**, which is a state or province name;
- **L** *(optional)*, which is a city name;
- **O**, which is an organization name;
- **OU** *(optional)*, which is an organizational unit name;
- **CN**, which is the hostname:
  - **Warning** If you change the **CN** value, you have to change the hostname under [client.py](client.py) to reflect the new hostname.
- **emailAddress** *(optional)*, which is an email address.

## Self-signed certificate with Custom CA

```bash
mkdir -p ca/example.org
```

### Create Root CA (Done once)

#### Create Root Key

**Attention:** this is the key used to sign the certificate requests, anyone
holding this can sign certificates on your behalf. So keep it in a safe place!

```bash
openssl genrsa -des3 -out ca/rootCA.key 4096
```

If you want a non password protected key just remove the `-des3` option


## Create and self sign the Root Certificate

```bash
openssl req -x509 -new -nodes -key ca/rootCA.key -sha256 -days 1024 -out ca/rootCA.crt
```

Here we used our root key to create the root certificate that needs to be distributed in all the computers that have to trust us.


# Create a certificate (Done for each server)

This procedure needs to be followed for each server/appliance that needs a trusted certificate from our CA

## Create the certificate key

```
openssl genrsa -out ca/example.org/example.org.key 2048
```

## Create the signing  (csr)

The certificate signing request is where you specify the details for the certificate you want to generate.
This request will be processed by the owner of the Root key (you in this case since you create it earlier) to generate the certificate.

**Important:** Please mind that while creating the signign request is important to specify the `Common Name` providing the IP address or domain name for the service, otherwise the certificate cannot be verified.

I will describe here two ways to gener

### Method A (Interactive)

If you generate the csr in this way, openssl will ask you questions about the certificate to generate like the organization details and the `Common Name` (CN) that is the web address you are creating the certificate for, e.g `example.org`.

```
openssl req -new -key ca/example.org/example.org.key -out ca/example.org/example.org.csr
```

### Method B (One Liner)

This method generates the same output as Method A but it's suitable for use in your automation :) .

```
openssl req -new -sha256 -key ca/example.org/example.org.key -subj "/C=US/ST=CA/O=MyExampleOrg, Inc./CN=example.org" -out ca/example.org/example.org.csr
```

If you need to pass additional config you can use the `-config` parameter, here for example I want to add alternative names to my certificate.

```
openssl req -new -sha256 \
    -key example.org.key \
    -subj "/C=US/ST=CA/O=MyExampleOrg, Inc./CN=example.org" \
    -reqexts SAN \
    -config <(cat /etc/ssl/openssl.cnf \
        <(printf "\n[SAN]\nsubjectAltName=DNS:example.org,DNS:www.example.org")) \
    -out ca/example.org/example.org.csr
```


## Verify the csr's content

```
openssl req -in ca/example.org/example.org.csr -noout -text
```

## Generate the certificate using the `example.org` csr and key along with the CA Root key

```
openssl x509 -req -in ca/example.org/example.org.csr -CA ca/rootCA.crt -CAkey ca/rootCA.key -CAcreateserial -out ca/example.org/example.org.crt -days 500 -sha256
```

## Verify the certificate's content

```
openssl x509 -in ca/example.org/example.org.crt -text -noout
```
## Running the TLS connection example

### Run the server example

Open the terminal and enter the following commands:

```bash
python3 server.py [--with-ca]
```

### Run the client example

Open the terminal and enter the following commands:

```bash
python3 client.py [--with-ca]
```
