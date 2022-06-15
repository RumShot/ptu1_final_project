from django.shortcuts import render
import mariadb


def data_base(request):
    # conection to MariaDB
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
        # orders overall
        cursor  = conn.cursor() 
        cursor.execute("SELECT COUNT(order_id) FROM svst_order")
        overall_orders = cursor.fetchall()
        print(overall_orders)
        html_overall_orders = overall_orders[0][0]
        # unique distributors
        cursor.execute("SELECT DISTINCT import_batch FROM svst_product")
        distributors = cursor.fetchall()
        distrubutor_list = []
        for distributor in distributors:
            fixed_dist = distributor[0].split()[0].replace('LT', '').replace('LV', '')
            distrubutor_list.append(fixed_dist) if fixed_dist not in distrubutor_list else distrubutor_list

            context = {
            'message': message,
            'html_overall_orders': html_overall_orders,
            'is_connected': int(is_connected),
            'distributors': distrubutor_list,
        }
        conn.close()
        
    else:
        context = {
            'message': message,
        }

    return render(request, 'index.html', context)
