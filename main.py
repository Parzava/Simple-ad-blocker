from mitmproxy import http

# List of domains or keywords to block
AD_DOMAINS = [
    "ads.example.com",
    "tracker.example.com",
    "example-ad-network.com"
]

def request(flow: http.HTTPFlow) -> None:
    # Check if the request URL contains any of the ad domains
    if any(domain in flow.request.pretty_url for domain in AD_DOMAINS):
        flow.response = http.Response.make(
            204,  # No Content
            b'',  # Empty body
            {'Content-Type': 'text/plain'}
        )
        print(f"Blocked request to {flow.request.pretty_url}")

# This function is used to start the proxy server
def start():
    print("Ad blocker proxy is running...")

# Set up the proxy server to use this script
addons = [
    request
]

if __name__ == "__main__":
    from mitmproxy import proxy, options
    from mitmproxy.tools.main import mitmweb

    opts = options.Options(listen_port=8080)
    p = proxy.ProxyConfig(opts)
    m = mitmweb.Mitmweb(options=opts, proxy_config=p, addons=addons)
    m.run()
