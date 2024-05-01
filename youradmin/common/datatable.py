from django.db.models import Q
from datetime import datetime

def get_dict_array(post, name):
    dic = {}
    for k in post.keys():
        if k.startswith(name):
            rest = k[len(name):]

            # split the string into different components
            parts = [p[:-1] for p in rest.split('[')][1:]
            id = int(parts[0])

            # add a new dictionary if it doesn't exist yet
            if id not in dic:
                dic[id] = {}

            # add the information to the dictionary
            dic[id][parts[1]] = post.get(k)
    return dic


def get_single_dict_array(post, name):
    dic = {}
    for k in post.keys():
        if k.startswith(name):
            rest = k[len(name):]

            # split the string into different components
            parts = [p[:-1] for p in rest.split('[')][1:]

            id = int(parts[0])

            # add a new dictionary if it doesn't exist yet
            if id not in dic:
                dic[id] = {}

            # add the information to the dictionary
            dic[id] = post.get(k)
    return dic


# {0: {u'column': u'0', u'dir': u'asc'}}
def build_order_args(post_data, cols):

    order_dict = get_dict_array(post_data, 'order')

    args = list()

    for key in order_dict:
        col_order_data = order_dict[key]
        col_key = col_order_data['column']
        col_sort_type = col_order_data['dir']

        # holds de object for datatable
        col_data = cols[int(col_key)]

        col_name = col_data['data']

        if 'fields.' in col_name:
            col_name = col_name.replace('fields.', '')

        if col_sort_type == 'desc':
            col_name = '-'+col_name

        args.append(col_name)

    return args

def build_search_args(post_data, cols):

    search_dict = get_single_dict_array(post_data, 'search')

    # print(search_dict)
    # print(post_data)
    # return []
    search_queries = []

    for key in search_dict:

        col_search_string = search_dict[key]
        datatable_column_config = cols[int(key)]

        if 'skipSearch' in datatable_column_config:
            continue

        col_name = datatable_column_config['data']

        if 'fields.' in col_name:
            col_name = col_name.replace('fields.', '')

        search_type = 'icontains'
        if 'searchType' in datatable_column_config:
            search_type = datatable_column_config['searchType']

        kwargs = {}

        # date range logic
        # (start_date, end_date)
        if search_type == 'range':
            linked_range = datatable_column_config['linked_range']

            try:

                startdate_object = datetime.strptime(col_search_string, '%Y-%m-%d')
                enddate_object = datetime.strptime(search_dict[int(linked_range)], '%Y-%m-%d')
            except:
                continue
            col_search_string = (startdate_object, enddate_object)

        kwargs[col_name+"__"+search_type] = col_search_string



        search_queries.append(Q(**kwargs))

        # queries.append(Q(first_name__icontains=firstname))

    return search_queries