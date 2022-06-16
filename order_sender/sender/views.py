from django.shortcuts import render
import mariadb
from django.contrib import messages


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
        is_connected = 1
    except mariadb.Error as e:
        is_connected = 0
        messages.error(request, f"Error connecting to the database: {e}")
        return render(request, 'index.html')

    if is_connected == 1:
        # overall orders
        cursor  = conn.cursor() 
        cursor.execute("SELECT COUNT(order_id) FROM svst_order")
        overall_orders = cursor.fetchall()
        html_overall_orders = overall_orders[0][0]
        # unique distributors
        cursor.execute("SELECT DISTINCT import_batch FROM svst_product")
        distributors = cursor.fetchall()
        distrubutor_list = []

        for distributor in distributors:
            fixed_dist = distributor[0].split()[0].replace('LT', '').replace('LV', '')
            distrubutor_list.append(fixed_dist) if fixed_dist not in distrubutor_list else distrubutor_list

        context = {
            'html_overall_orders': html_overall_orders,
            'is_connected': int(is_connected),
            'distributors': distrubutor_list,
        }

        conn.close()
        return render(request, 'index.html', context)

def processing_list(request):
    try:
        conn = mariadb.connect(
            host="127.0.0.1",
            port=3307,
            user="root",
            password="",
            database="ptu1_data_base"
            )
        is_connected = 1
    except mariadb.Error as e:
        is_connected = 0
        messages.error(request, f"Error connecting to the database: {e}")
        return render(request, 'index.html')

    if is_connected == 1:
        cursor  = conn.cursor() 
        cursor.execute("SELECT * FROM `svst_order` WHERE order_status_id = 2")
        overall_processing = cursor.fetchall()
        # order_id = overall_processing[0]
        # email = overall_processing[10]
        # phone = overall_processing[11]
        # adress = overall_processing[17]
        # name = overall_processing[29]
        # surname = overall_processing[30]
        # city = overall_processing[39]
        # comment = overall_processing[44]

        context = {
            'overall_processing': overall_processing,
            'is_connected': int(is_connected),
            # 'order_id': order_id,
            # 'email': email,
            # 'phone': phone,
            # 'adress': adress,
            # 'name': name,
            # 'surname': surname,
            # 'city': city,
            # 'comment': comment,
        }

        conn.close()
        return render(request, 'processing.html', context)

def completed_list(request):
    return render(request, 'completed.html')

def hole_list(request):
    return render(request, 'hole.html')



# class ProcessingList(generic.ListView):
#     model = NonExsitent
#     context_object_name = 'processing'
#     template_name = 'processing.html'

#     def get_context_data(self):
#         try:
#             conn = mariadb.connect(
#                 host="127.0.0.1",
#                 port=3307,
#                 user="root",
#                 password="",
#                 database="ptu1_data_base"
#                 )
#             cursor  = conn.cursor() 
#             cursor.execute("SELECT * FROM `svst_order` WHERE order_status_id = 2")
#             overall_processing = cursor.fetchall()
#             conn.close()
#         except mariadb.Error as e:
#             message = f"Error connecting to the database: {e}"

#         return self.overall_processing