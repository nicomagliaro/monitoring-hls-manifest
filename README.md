# HC MONITORING HLS PLAYLIST #

Proyecto de zabbix AWS

### What is this repository for? ###

* Zabbix
* Django 
* Docker & test

### API configs ###

```
    test: http://127.0.0.1:8000/check/?url=https://app-edge1.example.com/app/app.smil/playlist.m3u8
    test: http://127.0.0.1:8000/check/?url=https://app-cdn1.example.com/cosfc/cosfc.smil/playlist.m3u8
    test: http://hls-monitoring.aws.example.com.ar/check/?url=https://app-edge1.example.com/app/app.smil/playlist.m3u8

    Response:
    HTTP code (200 && Success) or 503 otherwise
```

### Contribution guidelines ###

* Optimize request handshake!

### Who do I talk to? ###

* Nicolas Magliaro <nicolasmagliaro@gmail.com> 
  - test: http://127.0.0.1:8000/check/?url=https://app-edge1.example.com/app/app.smil/playlist.m3u8
  - test: http://127.0.0.1:8000/check/?url=https://app-cdn1.example.com/app/app.smil/playlist.m3u8
  - test: http://hls-monitoring.zabbix.example.com.ar/check/?url=https://app-edge1.example.com/app/app.smil/playlist.m3u8