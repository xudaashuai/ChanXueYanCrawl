import requests

req = requests.post(
    'https://m.nuomi.com/webapp/bnjs/request',
    headers='',
    data={
        'origina': 'https://chi.nuomi.com/gaiya/food/getInfo?type=31&cityId=400010000&location=0%2C0&fid=2093&pn=1&v=7.1.0&deviceType=1&compV=3.1.5&cuid=187bc228caeaacec4c0269ef5ea096a9&terminal=3&category=326&categoryName=%E7%BE%8E%E9%A3%9F&sub_category_id=0&area_type=0&parent_area_id=1&area_id=0',
        'type': 'get', 'extra': '{"compid":"cuisine-home"}'
        },

)
print(req.status_code)
print(req.content)
