# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from urllib.parse import urlparse
from .check_hls import Hls


def verify(request, url):
    """ test: http://127.0.0.1:8000/check/?url=https://tycsports-edge1.tbxdrm.com/tycsports/tycsports.smil/playlist.m3u8
        test: http://127.0.0.1:8000/check/?url=https://cbo-cdn1.tbxdrm.com/cosfc/cosfc.smil/playlist.m3u8
        test: http://hls-monitoring.aws.hostclick.com.ar/check/?url=https://tycsports-edge1.tbxdrm.com/tycsports/tycsports.smil/playlist.m3u8 """
    if request.method == 'GET':
        try:
            url = request.GET.get('url')
        except ValueError:
            return HttpResponse(0)

        if not url:
            return HttpResponse(0)

        # Parse url from request
        url_parsed = urlparse(url)

        # Extract server url
        host = url_parsed.netloc

        # Extract app path
        path = url_parsed.path

        # Instance Hls obj
        playlist = Hls(host, path)

        #Get playlist from server
        get_playlist = playlist.hls()

        # Get chunks from playlist
        if get_playlist is not None and 'Success:' in get_playlist:
            return HttpResponse('{}'.format(get_playlist), status=200)
        else:
            return HttpResponse(status=503)

    return HttpResponse(status=503)
