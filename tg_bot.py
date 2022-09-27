# with open("menu.json", "r") as file:
#   menu = file.read()
# print(menu)
# with open("address.json", "r") as file:
#   address = file.read()
# print(address)
import json

from environs import Env

from moltin_api import get_access_token, \
    relate_image_to_product, \
    create_flow, add_field_to_flow, create_entry_to_flow


def add_products_to_store(moltin_api_token):

    with open("menu.json", "r") as file:
      menu_json = file.read()

    menu = json.loads(menu_json)

    for product in menu:
        product_id = product['id']
        name = product['name']
        description = product['description']
        price = product['price']
        image_url = product['product_image']['url']

        relate_image_to_product(moltin_api_token,
                                product_id,
                                name,
                                description,
                                price,
                                image_url)


def add_entries_to_flow(moltin_api_token, flow_slug):

    with open("address.json", "r") as file:
      pizzeria_addresses_json = file.read()

    pizzeria_addresses = json.loads(pizzeria_addresses_json)

    for pizzeria_address in pizzeria_addresses:
        address = pizzeria_address['address']['full']
        alias = pizzeria_address['alias']
        longitude = pizzeria_address['coordinates']['lon']
        latitude = pizzeria_address['coordinates']['lat']

        create_entry_to_flow(moltin_api_token, flow_slug, address, alias,
                             longitude, latitude)


def create_flow_and_fields(moltin_api_token):
    flow_id, flow_slug = create_flow(moltin_api_token, 'Pizzeria', 'pizzeria', 'Good pizza')
    add_field_to_flow(moltin_api_token, 'Address',
                      'address',
                      'string',
                      'pizzeria address',
                      flow_id)
    add_field_to_flow(moltin_api_token, 'Alias',
                      'alias',
                      'string',
                      'pizzeria alias',
                      flow_id)
    add_field_to_flow(moltin_api_token, 'Longitude',
                      'longitude',
                      'string',
                      'pizzeria longitude',
                      flow_id)
    add_field_to_flow(moltin_api_token, 'Latitude',
                      'latitude',
                      'string',
                      'pizzeria latitude',
                      flow_id)

    return flow_slug


def main():
    env = Env()
    env.read_env()

    moltin_client_id = env.str('MOLTIN_CLIENT_ID')
    moltin_client_secret = env.str('MOLTIN_CLIENT_SECRET')

    moltin_api_token, expiration_time = get_access_token(moltin_client_id,
                                                         moltin_client_secret)
    add_products_to_store(moltin_api_token)
    flow_slug = create_flow_and_fields(moltin_api_token)
    add_entries_to_flow(moltin_api_token, flow_slug)


if __name__ == '__main__':
    main()
