import re
from urllib.parse import urlparse
import numpy as np

def extract_features(url: str):
    parsed_url = urlparse(url)
    hostname = parsed_url.netloc or parsed_url.path
    
    url_length = len(url)
    num_dots = url.count('.')
    has_ip = 1 if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', hostname) else 0
    num_hyphens = url.count('-')
    num_at_symbol = url.count('@')
    digits = sum(c.isdigit() for c in url)
    ratio_digits = digits / url_length if url_length > 0 else 0
    
    return np.array([[url_length, num_dots, has_ip, num_hyphens, num_at_symbol, ratio_digits]])