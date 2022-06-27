from django.shortcuts import render 
import mariadb
from django.contrib import messages
from os.path import join
import os


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
        # unique distributors
        cursor.execute("SELECT DISTINCT import_batch FROM svst_product")
        distributors = cursor.fetchall()
        distrubutor_list = []

        for distributor in distributors:
            fixed_dist = distributor[0].split()[0].replace('LT', '').replace('LV', '')
            distrubutor_list.append(fixed_dist) if fixed_dist not in distrubutor_list else distrubutor_list
        # processing count
        cursor.execute("SELECT COUNT(order_status_id) FROM svst_order WHERE order_status_id = 2")
        processing_count = cursor.fetchall()

        cursor.execute("SELECT COUNT(order_status_id) FROM svst_order WHERE order_status_id = 3")
        shipped_count = cursor.fetchall()

        cursor.execute("SELECT COUNT(order_status_id) FROM svst_order WHERE order_status_id = 5")
        completed_count = cursor.fetchall()

        cursor.execute("SELECT COUNT(order_status_id) FROM svst_order WHERE order_status_id NOT IN (2, 3, 5)")
        unprocessed_count = cursor.fetchall()

        context = {
            'overall_orders': overall_orders,
            'is_connected': int(is_connected),
            'distributors': distrubutor_list,
            'processing_count': processing_count,
            'shipped_count': shipped_count,
            'completed_count': completed_count,
            'unprocessed_count': unprocessed_count,
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
        cursor.execute("SELECT * FROM `svst_order` WHERE order_status_id = 2 ORDER BY date_added DESC")
        overall_processing = cursor.fetchall()

        context = {
            'overall_processing': overall_processing,
            'is_connected': int(is_connected),
        }

        conn.close()
        return render(request, 'processing.html', context)

def shipped_list(request):
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
        cursor.execute("SELECT * FROM `svst_order` WHERE order_status_id = 3 ORDER BY date_added DESC")
        overall_processing = cursor.fetchall()

        context = {
            'overall_processing': overall_processing,
            'is_connected': int(is_connected),
        }

        conn.close()
        return render(request, 'processing.html', context)


def completed_list(request):
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
        cursor.execute("SELECT * FROM `svst_order` WHERE order_status_id = 5 ORDER BY date_added DESC")
        overall_processing = cursor.fetchall()

        context = {
            'overall_processing': overall_processing,
            'is_connected': int(is_connected),
        }

        conn.close()
        return render(request, 'completed.html', context)

def hole_list(request):
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
        cursor = conn.cursor() 
        cursor.execute("SELECT * FROM `svst_order` WHERE order_status_id NOT IN (2, 3, 5) ORDER BY date_added DESC")
        overall_processing = cursor.fetchall()

        context = {
            'overall_processing': overall_processing,
            'is_connected': int(is_connected),
        }

        conn.close()
        return render(request, 'hole.html', context)

def log_list(request):
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
        return render(request, 'logs.html')

    logs = 'sender/static/'
    files = os.listdir(join(logs, 'logs'))
    context = {'files': [join('logs/', file) for file in files],
               'is_connected': int(is_connected), 
                }
    return render(request, 'logs.html', context)
