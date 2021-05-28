def parse_timestamp(timestamp):
    return ' '.join(timestamp.split('.')[0].split('T')[::-1])