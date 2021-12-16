def get_page_indices(page = 0, page_size = 25):
    # Determine the start and end of the page
    page_start = 0
    if page != None:
        page = int(page)
        page = page - 1  # Subtract one so that the first page is one and not zero
        page_start = page * page_size

    page_end = page_start + page_size
    return page_start, page_end