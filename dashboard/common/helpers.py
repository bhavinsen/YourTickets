def get_username(request):
    f_name = request.user.first_name
    l_name = request.user.last_name
    if (f_name != "" and l_name == ""):
        return f_name
    elif (l_name != "" and f_name ==""):
        return l_name
    elif (l_name != "" and f_name != ""):
        return request.user.first_name + " " + request.user.last_name
    else:
        return request.user.username