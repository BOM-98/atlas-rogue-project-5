from requests_html import HTMLSession
import json
import requests
import os

baseurl = "https://cloan.uk"
url = "https://cloan.uk/category/view-all?page=10"

headers = {
    'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 14_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15'
}

s = HTMLSession()
r = s.get(url, headers=headers)
products_data = []

r.html.render(sleep=1)
    
products = r.html.xpath('//*[@id="products-section"]', first=True)
items = len(products.absolute_links)
counter = 0

for item in products.absolute_links:
    r = s.get(item, headers=headers)
    r.html.render(sleep=1, timeout=50)
    # Assign Name
    name = r.html.find('h1', first=True).text
    # Assign Designer
    designer = r.html.find('h2', first=True).text
    # Assign Price
    price = r.html.find('p.price', first=True).text
    # Clean Price
    clean_price = price.replace('From £', '').strip()
    # Assign RRP
    rrp_element = r.html.find('p.rrp', first=True)

    if rrp_element is not None:
        rrp = rrp_element.text
        clean_rrp = rrp.replace('RRP £', '').strip()
    else:
        clean_rrp = None
    
    #Get Variants (Size, Colour, Length)
    variants = r.html.xpath('//*[@class="variation-grid"]', first=True)
    inputs = variants.find('input.options')
    
    if len(inputs) == 3:
        # Assign Size, Length and Colour
        size = inputs[0].attrs.get('placeholder', 'None')
        length = inputs[1].attrs.get('placeholder', 'None')
        colour = inputs[2].attrs.get('placeholder', 'None')
    else:
        size = 'M'
        length = 'N/A'
        colour = 'N/A'
    
    # Get Image URL
    # Find all source elements with type 'image/webp'
    source_elements = r.html.find('source[type="image/webp"]')

    image_url = None
    image_url_2x = None
    for source_element in source_elements:
        # Check if the height attribute is 750
        if source_element.attrs.get('height') == '750':
            srcset = source_element.attrs.get('srcset')
            # Split the srcset to analyze each part
            if srcset:
                srcset_parts = srcset.split(", ")
                for part in srcset_parts:
                    url, descriptor = part.split(" ", 1)
                    # Store the first URL as a fallback
                    if image_url is None:
                        image_url = url
                    # Check for 2x descriptor
                    if descriptor == "2x":
                        image_url_2x = url
                        break
                # Use 2x URL if found, else fallback to the first URL
                image_url = image_url_2x if image_url_2x else image_url
                if image_url:
                    break
            else:
                image_url = None 
    
    if image_url:
        # Download Image
        image_name = name.replace(' ', '_').replace('/', '_').replace('?', '_').replace('!', '_').replace(':', '_').replace('"', '_').replace("'", '_').replace(',', '_').replace('(', '_').replace(')', '_').replace('&', '_').replace(';', '_').replace('.', '_').replace('-', '_').replace('__', '_').lower()
        if not image_name.lower().endswith('.webp'):
                image_name += '.webp'
        folder_path = '/Users/brianomahony/Documents/software-development/Projects/atlas-rogue-project-5/product_images'
        
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
            
        response = requests.get(image_url)
        if response.status_code == 200:
            with open(os.path.join(folder_path, image_name), 'wb') as f:
                f.write(response.content)
        else:
            print('Error downloading image')
    
    # Get SKU
    script_tag = r.html.find('script[type="application/ld+json"]', first=True)
    if script_tag:
        json_data = json.loads(script_tag.text)

        # Extract the SKU
        sku = json_data.get('sku', None)
    else:
        sku = None
    
    #Get Product Category
    breadcrumb_items = r.html.find('li.breadcrumb-item a')
    category_text = breadcrumb_items[1].text
    
    categories_list = {
        "Dress": 1,
        "Top": 2,
        "Bag": 3,
        "Blazer": 4,
        "Skirt": 5,
        "Hat": 6,
        "Other": 7,
    }
    
    # Set default category to 'Other' if no match is found
    category = categories_list.get(category_text, categories_list["Other"])

    # Create Product Dictionary
    counter += 1
    product_info = {
        "pk": counter,
        "model": "products.product",
        "fields": {
            "name": name,
            "designer": designer,
            "price": clean_price,
            "rrp": clean_rrp,
            "sku": sku,
            "size": size,
            "colour": colour,
            "length": length,
            "image_url": image_url,
            "image": image_name,
            "category": category
        }
    }
    
    # Append Product Dictionary to products_data list
    products_data.append(product_info)
    print(f'Product {counter} of {items} complete')
    
    # Write products_data list to products.json
    with open('products-2.json', 'w') as json_file:
        json.dump(products_data, json_file, indent=4)