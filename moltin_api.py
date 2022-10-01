import requests
from slugify import slugify


def create_product(moltin_api_token, product_id, name, description, price):
    headers = {
        'Authorization': f'Bearer {moltin_api_token}',
        'Content-Type': 'application/json',
    }

    product_slug = slugify(name)

    payload = {
        'data': {
            'type': 'product',
            'name': name,
            'slug': product_slug,
            'sku': f'{product_slug}-{product_id}',
            'description': description,
            'manage_stock': False,
            'price': [
                {
                    'amount': price*100,
                    'currency': 'RUB',
                    'includes_tax': False,
                },
            ],
            'status': 'live',
            'commodity_type': 'physical',
        },
    }

    response = requests.post('https://api.moltin.com/v2/products',
                             headers=headers,
                             json=payload)
    response.raise_for_status()
    product_id = response.json()['data']['id']
    return product_id


def upload_product_image(moltin_api_token, image_url):
    headers = {
        'Authorization': f'Bearer {moltin_api_token}',
    }

    files = {
        'file_location': (None, image_url),
    }

    response = requests.post('https://api.moltin.com/v2/files',
                             headers=headers, files=files)
    response.raise_for_status()
    image_id = response.json()['data']['id']
    return image_id


def relate_image_to_product(moltin_api_token, product_id, name, description,
                            price, image_url):

    product_id = create_product(moltin_api_token, product_id, name,
                                description, price)
    image_id = upload_product_image(moltin_api_token, image_url)

    headers = {
        'Authorization': f'Bearer {moltin_api_token}',
    }

    payload = {
        'data': {
            'type': 'main_image',
            'id': image_id,
        },
    }
    response = requests.post(
        f'https://api.moltin.com/v2/products/{product_id}/relationships/main-image',
        headers=headers,
        json=payload
    )

    response.raise_for_status()

    return response.json()


def create_flow(moltin_api_token, name, slug, description):

    headers = {
        'Authorization': f'Bearer {moltin_api_token}',
    }

    payload = {
        'data': {
            'type': 'flow',
            'name': f'{name}',
            'slug': f'{slug}',
            'description': f'{description}',
            'enabled': True,
        },
    }

    response = requests.post('https://api.moltin.com/v2/flows',
                             headers=headers, json=payload)

    response_data = response.json()['data']

    flow_id, flow_slug = response_data['id'], response_data['slug']

    return flow_id, flow_slug


def add_field_to_flow(moltin_api_token, name, slug, field_type, description,
                      flow_id, required=True, enabled=True):

    headers = {
        'Authorization': f'Bearer {moltin_api_token}',
    }

    payload = {
        'data': {
            'type': 'field',
            'name': f'{name}',
            'slug': f'{slug}',
            'field_type': f'{field_type}',
            'description': f'{description}',
            'required': required,
            'enabled': enabled,
            'relationships': {
                'flow': {
                    'data': {
                        'type': 'flow',
                        'id': f'{flow_id}',
                    },
                },
            },
        },
    }

    response = requests.post('https://api.moltin.com/v2/fields',
                             headers=headers, json=payload)
    return response.json()


def create_entry_to_flow(moltin_api_token, flow_slug, address, alias, longitude, latitude):

    headers = {
        'Authorization': f'Bearer {moltin_api_token}',
        'Content-Type': 'application/json',
    }

    payload = {
        'data': {
            'type': 'entry',
            'address': address,
            'alias': alias,
            'longitude': longitude,
            'latitude': latitude,
        }
    }

    response = requests.post(f'https://api.moltin.com/v2/flows/{flow_slug}/entries',
                             headers=headers,
                             json=payload)

    return response.json()


def add_product_to_cart(cart_id, product_id, moltin_api_token):
    headers = {
        'Authorization': f'Bearer {moltin_api_token}',
        'Content-Type': 'application/json',
        'X-MOLTIN-CURRENCY': 'RUB',
    }

    payload = {"data": {'id': product_id,
                        'type': 'cart_item',
                        'quantity': 1,
                        }
               }

    response = requests.post(f'https://api.moltin.com/v2/carts/{cart_id}/items',
                             headers=headers,
                             json=payload)
    print(response.json())
    response.raise_for_status()
    return response.json()['data']


def get_cart(chat_id, moltin_api_token):
    headers = {
        'Authorization': f'Bearer {moltin_api_token}',
    }

    response = requests.get(
        f'https://api.moltin.com/v2/carts/{chat_id}/items',
        headers=headers)
    response.raise_for_status()
    return response.json()


def get_products(moltin_api_token):
    headers = {
        'Authorization': f'Bearer {moltin_api_token}',
        'Content-Type': 'application/json',
    }

    response = requests.get('https://api.moltin.com/v2/products/',
                            headers=headers)
    response.raise_for_status()
    return response.json()['data']


def get_product(product_id, moltin_api_token):
    headers = {
        'Authorization': f'Bearer {moltin_api_token}',
    }

    response = requests.get(f'https://api.moltin.com/v2/products/{product_id}',
                            headers=headers)
    response.raise_for_status()
    return response.json()['data']


def get_image_url(image_id, moltin_api_token):
    headers = {
        'Authorization': f'Bearer {moltin_api_token}',
    }

    response = requests.get(f'https://api.moltin.com/v2/files/{image_id}',
                            headers=headers)
    response.raise_for_status()
    return response.json()['data']['link']['href']


def remove_cart_item(cart_id, product_id, moltin_api_token):
    headers = {
        'Authorization': f'Bearer {moltin_api_token}',
    }

    response = requests.delete(
        f'https://api.moltin.com/v2/carts/{cart_id}/items/{product_id}',
        headers=headers)
    response.raise_for_status()
    return response.json()['data']


def create_customer(email, moltin_api_token):
    headers = {
        'Authorization': f'Bearer {moltin_api_token}',
        'Content-Type': 'application/json',
    }

    payload = {"data": {'type': 'customer',
                        'name': 'some name',
                        "email": email,
                        "password": "mysecretpassword"
                        }
               }

    response = requests.post('https://api.moltin.com/v2/customers',
                             headers=headers,
                             json=payload)
    response.raise_for_status()
    return response.json()


def get_access_token(moltin_client_id,
                     moltin_client_secret):

    data = {
        'client_id': moltin_client_id,
        'client_secret': moltin_client_secret,
        'grant_type': 'client_credentials'
    }

    response = requests.post('https://api.moltin.com/oauth/access_token',
                             data=data)
    response.raise_for_status()
    auth_response = response.json()
    moltin_api_token = auth_response['access_token']
    expire_time = auth_response['expires_in']

    return moltin_api_token, expire_time


