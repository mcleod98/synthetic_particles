

def check_yaml(config: dict) -> dict:
    conf = {'xdim': int(config['xdim']),
        'ydim': int(config['ydim']),
        'mean_r': float(config['mean_r']), 
        'mean_aspect': float(config['mean_aspect']),
        'mean_n': float(config['mean_n']), 
        'sd_r': float(config['sd_r']), 
        'sd_aspect': float(config['sd_aspect']), 
        'sd_n': float(config['sd_n']), 
        'min_offset': float(config['min_offset']), 
        'gutters': (int(config['gutters'][0]), int(config['gutters'][1])),
        'mean_theta': float(config.get('mean_theta', 0)),
        'sd_theta': float(config.get('sd_theta', 0)),
        'n_dist': config.get('n_dist', []),
    }
    return conf