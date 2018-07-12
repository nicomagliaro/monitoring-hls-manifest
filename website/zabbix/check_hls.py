from .hls import Stream, StreamError
import shutil


class Hls:
    def __init__(self, host, path, port=None, ssl=True, checkchunk=False, timeout=10, bandwidths='all', duration=30):
        self.host = host
        self.path = path
        self.ssl = ssl
        self.checkchunk = checkchunk
        self.port = port
        self.timeout = timeout
        self.bandwidths = bandwidths
        self.duration = duration

    @staticmethod
    def urlize(url):
        """ returns urllized url """
        return '<a href="{}">{}</a>'.format(url, url)

    @staticmethod
    def clean(path):
        """ Expects list of dirs to remove. """
        try:
            shutil.rmtree(path)
        except OSError as e:
            return False
        return True

    def hls(self):
        try:
            stream = Stream(self.host, self.path, port=self.port, timeout=self.timeout, ssl=self.ssl)
        except StreamError as e:
            return 'Critical: {} {}'.format(e.error_str, self.urlize(e.url))

        # retrieve playlist
        playlist = stream.playlist.read().decode('utf-8').splitlines()
        if self.checkchunk:
            files = {}
            # get variant playlists if they exist in playlist
            if '#EXT-X-STREAM-INF' in ''.join(playlist):
                try:
                    variants = stream.get_variants(playlist, self.bandwidths)
                    print(variants)
                except StreamError as e:
                    return 'Critical: {} {} bandwidth: {}.'.format(e.error_str, self.urlize(e.url), e.bandwidth)

                for bandwidth in variants:
                    variant_addr, variant_playlist = variants[bandwidth]
                    response = variant_playlist
                    try:
                        files.update(stream.retrieve_segments(variant_addr, variant_playlist, duration=self.duration))
                    except StreamError as e:
                        return 'Critical: {} {}'.format(e.error_str, self.urlize(e.url))
            else:  # no variants, so get segments for initial playlist
                try:
                    files.update(stream.retrieve_segments(stream.addr, playlist, duration=self.duration))
                except StreamError as e:
                    return 'Critical: {} {}'.format(e.error_str, self.urlize(e.url))

            # check file size of each segment
            tmp_dirs = []
            for addr in files:
                try:
                    stream.check_size(files[addr])
                    # collect tmp_dirs for removal
                    dirname = '/'.join(files[addr].split('/')[:-1])
                    if dirname not in tmp_dirs:
                        tmp_dirs.append(dirname)
                except ValueError as e:
                    print(e)
                    return

            # remove files
            for td in tmp_dirs:
                try:
                    self.clean(td)
                except:
                    return 'Critical: unable to remove temporary directories: {}'.format(td)

            return 'Success: {} is up'.format(self.urlize(stream.addr))
        else:
            # Solo verifica que los chunks en la lista devuelvan HTTP 200/OK
            if '#EXT-X-STREAM-INF' in ''.join(playlist):
                try:
                    variants = stream.get_variants(playlist, self.bandwidths)
                except StreamError as e:
                    return
            for bandwidth in variants:
                variant_addr, variant_playlist = variants[bandwidth]
                response = variant_playlist
                if (response.status in [200, 302]) and response.reason == 'OK':
                    pass
                else:
                    return 'Critical: Something went wrong: code {} status {}'.format(response.status, response.status)
            return 'Success:'

@staticmethod
def delete_tmp_dirs():
    """ Delete zombie dirs undeleted because timeouts request"""
    delete_tmp = Housekeep()
    delete_tmp.delete_old()
