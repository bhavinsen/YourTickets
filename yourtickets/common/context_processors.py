from yourtickets.common import utils

def lc(request):
    return {"lc": utils.getCurrentLanguage(request)}

def langs(request):
    return {"langs": utils.getLanguagesList()}
