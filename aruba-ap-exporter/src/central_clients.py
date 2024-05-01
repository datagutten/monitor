import time

from prometheus_client import generate_latest, Summary, Gauge, CollectorRegistry, REGISTRY
from central import ArubaCentral
from pycentral.monitoring import Sites
from prometheus_client import start_http_server, Summary

central = ArubaCentral('token')

s = Sites()

aps = central.command_helper('/monitoring/v2/aps')
# clients = central.command_helper('/monitoring/v1/clients/wireless', limit=1000)
sites = s.get_sites(central)
pass

prefix = 'aruba_'
SITE_CLIENTS = Gauge(prefix + 'site_clients', 'Site clients', {'site_name': 'Site name'})
REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')


@REQUEST_TIME.time()
def get_site_clients():
    print('Get site clients')
    for site in sites['msg']['sites']:
        print(site['site_name'])
        clients = central.command_helper('/monitoring/v1/clients/wireless', limit=1000, site=site['site_name'])
        SITE_CLIENTS.labels(site_name=site['site_name']).set(clients['count'])


if __name__ == '__main__':
    # Start up the server to expose the metrics.
    start_http_server(8000)
    while True:
        get_site_clients()
        time.sleep(60*5)
