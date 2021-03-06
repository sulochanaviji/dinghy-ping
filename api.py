import responder
import requests
import asyncio

api = responder.API(title="Dinghy Ping", version="1.0", openapi="3.0.0", docs_route="/docs")

@api.route("/dinghy")
def dinghy_html(req, resp):
    resp.content = api.template('ping_input.html')

@api.route("/dinghy/ping/domains")
async def ping_multiple_domains(req, resp):
    """
    Async process to test multiple domains and return JSON with results
    Post request data example
    {
      "domains": [
        {
          "protocol": "https",
          "domain": "google.com"
        },
        {
          "protocol": "https",
          "domain": "microsoft.com"
        }
      ]
    }

    Return results
    {
      "domains": [
        {
          "protocol": "https",
          "domain": "google.com",
          "domain_response_code": "200",
          "domain_response_time_ms": "30.0ms"
          " 
        },
        {
          "protocol": "https",
          "domain": "microsoft.com"
          "domain_response_code": "200",
          "domain_response_time_ms": "200.1ms"
        }
      ]
    }
    """

    results = []

    def build_domain_results(protocol, request_domain, results):
        domain_response_code, domain_response_text, domain_response_time_ms = _process_request(protocol, request_domain, req.params) 
        results.append({ 
            "protocol": protocol,
            "domain": request_domain,
            "domain_response_code": domain_response_code,
            "domain_response_time_ms": domain_response_time_ms
        })
    
    def gather_results(data): 
        for domain in data['domains']:
            protocol = domain['protocol']
            request_domain = domain['domain']
            build_domain_results(protocol, request_domain, results)

    resp.media = {"domains_response_results": results, "wait": gather_results(await req.media())}

@api.route("/dinghy/ping/{protocol}/{domain}")
def domain_response_html(req, resp, *, protocol, domain):
    """
    API endpoint for sending a request to a domain via user specified protocol
    response containts status_code, body text and response_time_ms
    """

    domain_response_code, domain_response_text, domain_response_time_ms = _process_request(protocol, domain, req.params)

    resp.content = api.template(
            'ping_response.html',
            domain=domain,
            domain_response_code=domain_response_code,
            domain_response_text=domain_response_text,
            domain_response_time_ms=domain_response_time_ms
    )

def _process_request(protocol, domain, params):
    """
    Internal method to run request process, takes protocol and domain for input
    """
    
    r = requests.get(f'{protocol}://{domain}', params=params)

    domain_response_code = r.status_code
    domain_response_text = r.text
    domain_response_time_ms = r.elapsed.microseconds / 1000

    return domain_response_code, domain_response_text, domain_response_time_ms

if __name__ == '__main__':
    api.run(address="0.0.0.0", port=80, debug=True)
