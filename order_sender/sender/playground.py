import mariadb
import json
from datetime import datetime
import requests
import logging


today = datetime.now()
date_now = today.strftime('%y%m%d_%H_%M')

def database_connection(sql_command):
    try:
        conn = mariadb.connect(
            host="127.0.0.1",
            port=3307,
            user="root",
            password="",
            database="ptu1_data_base"
            )
        cursor  = conn.cursor()
        cursor.execute(sql_command)
        command_return = cursor.fetchall()
        conn.close()

        return command_return

    except mariadb.Error as e:
        message = f"Error connecting to the database: {e}"

        return message

# ------------ ELKO --------------------
def elko_generate_order():
    sql_command = "SELECT * FROM svst_order INNER JOIN svst_order_product ON svst_order.order_id = svst_order_product.order_id INNER JOIN svst_product ON svst_order_product.product_id = svst_product.product_id WHERE svst_product.import_batch LIKE '%Elko%' AND svst_order.order_status_id = 2"
    data_received = database_connection(sql_command)
    if data_received != []:
        for sigle_data_received in data_received:
            order_id = str(sigle_data_received[0])
            file_name = order_id+ '_ELKO_' + date_now + '.json'
            elko_email = sigle_data_received[10]
            elko_telephone = sigle_data_received[11]
            elko_name = sigle_data_received[30]
            elko_surname = sigle_data_received[31]
            elko_shipping_country = sigle_data_received[36]
            elko_shipping_postcode = sigle_data_received[35]
            elko_shipping_city = sigle_data_received[38]
            elko_shipping_address = sigle_data_received[32]
            elko_price = sigle_data_received[67]
            elko_price_total = sigle_data_received[68]
            elko_quantity = sigle_data_received[66]
            elko_product_name = sigle_data_received[64]
            elko_product_model = sigle_data_received[72]
            elko_product_id = sigle_data_received[132]
            elko_user_comment = sigle_data_received[44]
            distributor_message = {
                "shipTo": "Customer",
                "enduser": {
                    "company": "eJura",
                    "pvnNumber": "LT100013728513",
                    "contactName": "" + elko_name + " " + elko_surname + "",
                    "contactPhone": "" + elko_telephone + "",
                    "addressLine1": "" + elko_email + "",
                    "city": "" + elko_shipping_city + "",
                    "country": "" + elko_shipping_country + "",
                    "postalCode": "" + elko_shipping_postcode + "",
                    "street": "" + elko_shipping_address + "",
                    "house": "",
                    "apartment": "",
                    "isNaturalPerson": "true",
                    "customerPo": "string",
                    "contactMail": "" + elko_email + "",
                    "pickupPoint": 0
                },
                "created": 0,
                "sum": "" + str(elko_price) + "",
                "currency": "EUR",
                "createdBy": "eJura",
                "vat": 21,
                "delivery": "string",
                "lines": [
                    {
                    "id": "" + elko_product_id + "",
                    "elkoCode": "" + elko_product_id + "",
                    "manufacturerCode": "" + elko_product_model + "",
                    "productName": "" + elko_product_name + "",
                    "quantity": "" + str(elko_quantity) + "",
                    "currency": "EUR",
                    "price": "" + str(elko_price) + "",
                    "sum": "" + str(elko_price_total) + "",
                    "vat": 21,
                    "quantityRequested": "" + str(elko_quantity) + "",
                    "clientNote": "" + elko_user_comment + ""
                    }
                ],
                "deliveryInstructions": "" + elko_user_comment + "",
                "transportation": "true",
                "fastest": "true",
                "orderIfAllAvailable": "true",
                "type": "string",
                "id": "" + elko_product_id + ""
                }
            # save_json(distributor_message, file_name)
            # elko_post_request(distributor_message)
            # elko_change_status(order_id)
    else:
        print("No data received")

# JSON save 
def save_json(distributor_message, file_name):
    with open('order_sender/sender/order_messages/' + file_name, 'w+', encoding="utf-8") as json_file:
        json.dump(distributor_message,json_file)   

def elko_post_request(distributor_message):
    bearer = open("order_sender/sender/authentications/elko_bearer.txt", "r")
    url = "https://api.elko.cloud/v3.0/api/Orders"
    payload = json.dumps(distributor_message)
    headers = {'Authorization': bearer.read(),
                'Content-Type': 'application/json'
                }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)

# changing order_status_id from Processing --> Shipping
def elko_change_status(order_id):
    sql_command = "UPDATE `svst_order` SET order_status_id = 3 WHERE order_id = " + order_id
    database_connection(sql_command)


elko_generate_order()
