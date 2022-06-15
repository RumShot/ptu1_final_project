import mariadb
    

def elko_check_changes():
    try:
        conn = mariadb.connect(
            host="127.0.0.1",
            port=3307,
            user="root",
            password="",
            database="ptu1_data_base"
            )
        message = "connected to database :)"
        is_connected = 1
    except mariadb.Error as e:
        is_connected = 0
        message = f"Error connecting to the database: {e}"

    if is_connected == 1:
        cursor  = conn.cursor() 
        cursor.execute("SELECT * FROM svst_order INNER JOIN svst_order_product ON svst_order.order_id = svst_order_product.order_id INNER JOIN svst_product ON svst_order_product.product_id = svst_product.product_id WHERE svst_product.import_batch LIKE '%Elko%' AND svst_order.order_status_id = 2")
        all_details = cursor.fetchall()
        conn.close()
    else:
        print("Mistake")
    return all_details


def elko_generate_order():
    data_received = elko_check_changes()
    if data_received != []:
        for sigle_data_received in data_received:
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
            json_message = {
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
                "sum": "" + elko_price + "",
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
                    "quantity": "" + elko_quantity + "",
                    "currency": "EUR",
                    "price": "" + elko_price + "",
                    "sum": "" + elko_price_total + "",
                    "vat": 21,
                    "quantityRequested": "" + elko_quantity + "",
                    "clientNote": "" + elko_user_comment + ""
                    }
                ],
                "deliveryInstructions": "test",
                "transportation": "true",
                "fastest": "true",
                "orderIfAllAvailable": "true",
                "type": "string",
                "id": "" + elko_product_id + ""
                }
            print(json_message)
    else:
        print("No data received")

elko_generate_order()