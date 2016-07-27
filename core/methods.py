# START Custom Global Methods Settings
def standardResponse(data=[], errors=[], **kwargs):
    return {"data":data, "errors":errors}

def pagination(page):
    if page:
        page = int(page)
        items_per_page = 5
        offset = (page - 1) * items_per_page
        limit = page * items_per_page
        return ( offset, limit )
    else:
        return False
# END Custom Global Methods Settings