def asp_args(resp):
    ''' Parse "__xx" arguments (such as __VIEWSTATE) from HtmlResponse
    '''
    ret = {}
    for tag in resp.css('input'):
        name = tag.xpath('./@name').extract_first()
        value = tag.xpath('./@value').extract_first()
        if name and name.startswith('__'):
            ret.update({name: value})
    return ret
