import requests

ip = 'ip_address'
r_id = 'relay'
state = 'type'
url = 'http://' + ip + '/update?'+r_id+'=1&state='+state
requests.request('GET', url)