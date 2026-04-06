import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Create session with retries
session = requests.Session()
retries = Retry(total=3, backoff_factor=0.1)
adapter = HTTPAdapter(max_retries=retries)
session.mount('http://', adapter)

# Get CSRF token (if needed)
login_page = session.get('http://127.0.0.1:5000/login')
print(f'Login page status: {login_page.status_code}')

# Try to login with test credentials
# First, let's see what user exists in database
login_data = {
    'username': 'testuser',
    'password': 'Test@12345'
}

response = session.post('http://127.0.0.1:5000/login', data=login_data, allow_redirects=False)
print(f'Login response status: {response.status_code}')
print(f'Location header: {response.headers.get("Location", "None")}')

# Now check if we're authenticated by visiting home page
home_page = session.get('http://127.0.0.1:5000/')
print(f'Home page status: {home_page.status_code}')

# Check for navbar items
if 'Dashboard' in home_page.text and 'Password Tool' in home_page.text:
    print('✓ Authenticated: Found Dashboard and Password Tool')
else:
    print('✗ Not authenticated or navbar not showing protected items')
    
# Show what navbar items we found
if 'Password Tool' in home_page.text:
    print('✓ Password Tool found')
if 'Dashboard' in home_page.text:
    print('✓ Dashboard found')
if 'Profile' in home_page.text:
    print('✓ Profile found')
if 'Logout' in home_page.text:
    print('✓ Logout found')
if 'Login' in home_page.text:
    print('✓ Login found')
