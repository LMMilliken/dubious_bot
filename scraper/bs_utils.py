def get_text_divs(data):
    return [
        tag for tag in 
        data.find_all(
            lambda tag: tag.name == 'div' and 'text-align:' in tag.get('style', '')
            )
        ]

def get_outer_divs(data):
    return [
        get_text_divs(tag) for tag in
        data.find_all(
            (lambda tag: tag.name == 'div' and len(get_text_divs(tag)) > 0),
            recursive = False
        )
    ]

def get_spans(data):
    outers = [
        get_outer_divs(tag) for tag in
        data.find_all(
            lambda tag: tag.name == 'span' and len(get_outer_divs(tag)) > 0
        )
    ]
    return outers

def get_text(tag):
    if isinstance(tag, list):
        return '\n'.join([t.text for t in tag])
    else:
        return '\n' + tag.text

def get_posts(data):
    spans = get_spans(data)
    posts = [
        '\n'.join([get_text(tag) for tag in post])
        for post in spans
    ]
    return posts