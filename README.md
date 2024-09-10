# Autodiscover
Simple docker image that provides autodiscover for mail clients


This solution uses only Python’s built-in libraries and serves a simple application on port 8000 in the container. You can then use Nginx to proxy requests to this container.


## How to use

First, build the Docker image:

```bash
docker build -t autodiscover .
```
Run the container:

```bash
docker run -d -p 8000:8000 autodiscover
```

Or, if you're using Docker Compose:

```bash
docker-compose up -d
```


Then add to nginx conf file for domain:
```bash
    location /AutoDiscover {
        proxy_pass http://localhost:8000/autodiscover/autodiscover.xml;
    }

    location /mail {
        proxy_pass http://localhost:8000/mail/config-v1.1.xml;
    }
```

## Credits

Based on https://www.canaletto.fr/post/autodiscover-and-autoconfig-imap-smtp

