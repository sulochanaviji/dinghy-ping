### Dinghy Ping

[![Build Status](https://travis-ci.org/silvermullet/dinghy-ping.svg?branch=master)](https://travis-ci.org/silvermullet/dinghy-ping)

![dinghy](https://user-images.githubusercontent.com/538171/47242041-7d96d600-d3a2-11e8-8c55-a04e1249bc46.jpeg)

#### Docker Run as Daemon

```
docker run -p 80:80 -d sepulworld/dinghy-ping:latest
```

#### Requirements

```pipenv install```

#### Localhost

```python3 api.py```

#### Local Docker Build

```bash
docker build . --tag dinghy:latest
docker run -p 80:80 dinghy:latest
```

#### Dinghy ping single endpoint

```bash
curl "http://127.0.0.1/dinghy/ping/https/google.com"
```

#### Dinghy ping single endpoint with params

```bash
curl "http://127.0.0.1/dinghy/ping/https/www.google.com/search?source=hp&ei=aIHTW9mLNuOJ0gK8g624Ag&q=dinghy&btnK=Google+Search&oq=dinghy&gs_l=psy-ab.3..35i39l2j0i131j0i20i264j0j0i20i264j0l4.4754.5606..6143...1.0..0.585.957.6j5-1......0....1..gws-wiz.....6..0i67j0i131i20i264.oe0qJ9brs-8"
```

#### Dinghy ping multiple sites

```bash
# dinghy-ping multiple sites
curl -vX POST "http://127.0.0.1/dinghy/ping/domains" \
  -d @tests/multiple_domains.json \
  --header "Content-Type: application/json"
```

#### Helm Install

```
helm install -n dinghy-ping ./helm/dinghy-ping
```
