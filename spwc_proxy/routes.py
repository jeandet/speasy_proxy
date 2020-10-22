def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route('get_data', '/get_data')
    config.add_route('get_cache_entries', '/get_cache_entries')
