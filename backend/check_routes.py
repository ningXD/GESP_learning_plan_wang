from app import app

print('Routes:')
for rule in app.url_map.iter_rules():
    print(f'{rule}')
