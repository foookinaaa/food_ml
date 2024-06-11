import requests

url = "http://127.0.0.1:8000/api/predict/"
data = {
    "tree_dbh": 22,
    "curb_loc": 1,
    "steward": 0,
    "guards": 0,
    "sidewalk": 1,
    "problems": 1,
    "root_stone": 0,
    "root_grate": 0,
    "root_other": 0,
    "trunk_wire": 0,
    "trnk_light": 0,
    "trnk_other": 0,
    "brch_light": 1,
    "brch_shoe": 0,
    "brch_other": 0,
    "spc_common": "green ash",
    "zip_city": "Ozone Park",
    "borough": "Queens",
    "user_type": "NYC Parks Staff",
}

response = requests.post(url, json=data)
print(response.json())
