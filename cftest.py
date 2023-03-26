import requests

url = 'https://www.cloudflare.com/ips-v4'
r = requests.get(url)
ips = r.text.split('\n')
ips = [ip for ip in ips if ip != '']

import ipaddress

ips = [str(ip) for ip in ipaddress.ip_network(ips[0]).hosts()]

import concurrent.futures
import ping3
from tqdm import tqdm


def ping_ips(ips):
    results = {}

    def ping(ip):
        sum = 0
        count = 0
        for _ in range(4):
            latency = ping3.ping(ip, unit='ms')
            if latency:
                sum += latency
                count += 1
        if count < 2:
            pass
        else:
            results[ip] = sum / count

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        futures = []
        for ip in ips:
            futures.append(executor.submit(ping, ip))
        for _ in tqdm(concurrent.futures.as_completed(futures), total=len(ips)):
            pass

    return results


results = ping_ips(ips)

# sort based on latency
results = {k: v for k, v in sorted(results.items(), key=lambda item: item[1])}

# get the top 10
results = {k: v for k, v in list(results.items())[:10]}

for ip, latency in results.items():
    print(f'{ip} {latency}ms')


