from django.shortcuts import render
import mariadb
from os.path import join
import os
from django.core.paginator import Paginator


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
        is_connected = 1

        return command_return, is_connected

    except mariadb.Error as e:
        is_connected = 0
        messages = f"Error connecting to the database: {e}"

        return messages, is_connected

def data_base(request):
    sql_command = "SELECT COUNT(order_id) FROM svst_order"
    overall_orders = database_connection(sql_command)

    sql_command = "SELECT DISTINCT import_batch FROM svst_product"
    distributors = database_connection(sql_command)
    inner_dist = distributors[0]
    distrubutor_list = []

    for distributor in inner_dist:
        fixed_dist = distributor[0].replace('LT', '').replace('LV', '').split()[0]
        distrubutor_list.append(fixed_dist) if fixed_dist.split()[0] not in distrubutor_list else distrubutor_list

    sql_command = "SELECT COUNT(order_status_id) FROM svst_order WHERE order_status_id = 2"
    processing_count = database_connection(sql_command)

    sql_command = "SELECT COUNT(order_status_id) FROM svst_order WHERE order_status_id = 3"
    shipped_count = database_connection(sql_command)

    sql_command = "SELECT COUNT(order_status_id) FROM svst_order WHERE order_status_id = 5"
    completed_count = database_connection(sql_command)

    sql_command = "SELECT COUNT(order_status_id) FROM svst_order WHERE order_status_id NOT IN (2, 3, 5)"
    unprocessed_count = database_connection(sql_command)

    context = {
        'overall_orders': overall_orders[0],
        'distributors': distrubutor_list,
        'processing_count': processing_count[0],
        'shipped_count': shipped_count[0],
        'completed_count': completed_count[0],
        'unprocessed_count': unprocessed_count[0],
        }

    return render(request, 'index.html', context)


def processing_list(request):
    sql_command = "SELECT * FROM `svst_order` WHERE order_status_id = 2 ORDER BY date_added DESC"
    overall_processing = database_connection(sql_command)

    paginator = Paginator(overall_processing[0], 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'overall_processing': overall_processing[0],
        'page': page,
        }

    return render(request, 'processing.html', context)


def shipped_list(request):
    sql_command = "SELECT * FROM `svst_order` WHERE order_status_id = 3 ORDER BY date_added DESC"
    overall_shipped = database_connection(sql_command)

    context = {
        'overall_shipped': overall_shipped[0],
        }

    return render(request, 'shipped.html', context)


def completed_list(request):
    sql_command = "SELECT * FROM `svst_order` WHERE order_status_id = 5 ORDER BY date_added DESC"
    overall_complete = database_connection(sql_command)

    context = {
        'overall_complete': overall_complete[0],
        }

    return render(request, 'completed.html', context)


def hole_list(request):
    sql_command = "SELECT * FROM `svst_order` WHERE order_status_id NOT IN (2, 3, 5) ORDER BY date_added DESC"
    overall_hole = database_connection(sql_command)

    context = {
        'overall_hole': overall_hole[0],
        }

    return render(request, 'hole.html', context)


def log_list(request):
    logs = 'sender/static/'
    files = os.listdir(join(logs, 'logs'))

    context = {
        'files': [join('logs/', file) for file in files],
        }

    return render(request, 'logs.html', context)