"""Tracking utilities."""
import urllib.parse


LINIO_TRACKING_URL = 'http://linio.go2cloud.org/'
LINIO_TRACKING_URL += 'aff_c?offer_id=16&aff_id=7429&url={}'
LINIO_TRACKING_URL += '?utm_source=affiliates&utm_medium=hasoffers'
LINIO_TRACKING_URL += '&utm_campaign=7429&aff_sub='

SOICOS_NETSHOES_TRACKING_URL = 'http://ad.soicos.com/-ZYB?dl={}'

SOICOS_TROCAFONE_TRACKING_URL = 'http://ad.soicos.com/-109d?url={}'

SOICOS_BANGHO_TRACKING_URL = 'http://ad.soicos.com/-10e6?dl={}'

SOICOS_YOINS_TRACKING_URL = 'http://ad.soicos.com/-10UJ?dl={}'

SOICOS_DAFITI_TRACKING_URL = 'http://ad.soicos.com/-14kH?dl={}'


STORE_URL_MAP = {
    'linio': LINIO_TRACKING_URL,
    'netshoes': SOICOS_NETSHOES_TRACKING_URL,
    'trocafone': SOICOS_TROCAFONE_TRACKING_URL,
    'bangho': SOICOS_BANGHO_TRACKING_URL,
    'yoins': SOICOS_YOINS_TRACKING_URL,
    'dafiti': SOICOS_DAFITI_TRACKING_URL,
}


def get_tracker_link(url, store):
    """Get tracker link."""
    tracker_url = STORE_URL_MAP[store].format(
        urllib.parse.quote_plus(url)
    )

    return tracker_url
