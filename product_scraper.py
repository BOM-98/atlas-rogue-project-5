import requests
from bs4 import BeautifulSoup

baseurl = "https://www.mywardrobehq.com/"

headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15'
}

response = requests.get('https://cloan.uk/category/view-all', headers=headers)
# r = requests.get('https://cloan.uk/category/view-all')

if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all 'a' tags with a 'href' attribute within product listings
    product_links = [a['href'] for a in soup.find_all('a')]

    # Print all the product links
    for link in product_links:
        print(link)
else:
    print('Failed to retrieve the webpage')


# soup = BeautifulSoup(r.content, 'lxml')

# productlist = soup.find_all('a')

# print(productlist)

# productlinks = []

# for item in productlist:
#     for link in item.find_all('a', href=True):
#         productlinks.append(baseurl + link['href'])
#         print(link['href'])