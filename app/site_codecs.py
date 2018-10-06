import codecs

import werkzeug

__all__ = ['Codec']

class Codec(object):
    codecs = {}

    def __init_subclass__(cls):
        if cls.name is not None:
            cls.codecs[cls.name] = cls

    @classmethod
    def encode(cls, s):
        try:
            return cls._encode(s)
        except Exception:
            raise UnicodeError

    @classmethod
    def decode(cls, s):
        try:
            return cls._decode(s)
        except Exception:
            raise UnicodeError

    def __new__(cls, name):
        codec_type = cls.codecs.get(name, None)
        if codec_type is None:
            raise KeyError
        return super().__new__(codec_type)

    name = None

    @classmethod
    def _encode(cls, s):
        raise NotImplementedError

    @classmethod
    def _decode(cls, s):
        raise NotImplementedError

class StdCodecsCodec(Codec):
    codec_name = None

    @classmethod
    def _encode(cls, s):
        try:
            ret = codecs.encode(s.encode(), cls.codec_name)
            if isinstance(ret, bytes):
                ret = ret.decode()
            return ret
        except Exception:
            pass
        ret = codecs.encode(s, cls.codec_name)
        if isinstance(ret, bytes):
            ret = ret.decode()
        return ret

    @classmethod
    def _decode(cls, s):
        try:
            ret = codecs.decode(s, cls.codec_name)
            if isinstance(ret, bytes):
                ret = ret.decode()
            return ret
        except Exception:
            pass
        ret = codecs.decode(s.encode(), cls.codec_name)
        if isinstance(ret, bytes):
            ret = ret.decode()
        return ret


class Base64Codec(StdCodecsCodec):
    name = codec_name = 'base64'

class HexCodec(StdCodecsCodec):
    name = codec_name = 'hex'

class PunycodeCodec(StdCodecsCodec):
    name = codec_name = 'punycode'

class UrlCodec(Codec):
    name = 'url'

    @classmethod
    def _encode(cls, s):
        return werkzeug.url_encode({'q': s})[2:]

    @classmethod
    def _decode(cls, s):
        return werkzeug.url_decode('q=' + s)['q']
