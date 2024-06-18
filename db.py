import json

with open("sklad.json", 'r') as sr:
    sklad = json.load(sr)


def add_pair_load(data: dict):
    if data["brand"] in sklad:
        if data["name"] in sklad[data["brand"]]:
            for size in data["sizes"]:
                if size in sklad[data["brand"]][data["name"]]["sizes"]:
                    sklad[data["brand"]][data["name"]]["sizes"][size] = int(data["sizes"][size]) + int(sklad[data["brand"]][data["name"]]["sizes"][size])
                else:
                    sklad[data["brand"]][data["name"]]["sizes"][size] = data["sizes"][size]
        else:
            sklad[data["brand"]][data["name"]] = {"photo": data["photo"], "price": data["price"], "sizes": data["sizes"]}
    else:
        sklad[data["brand"]] = {data["name"]: {"photo": data["photo"], "price": data["price"], "sizes": data["sizes"]}}
    with open("sklad.json", 'w') as sw:
        json.dump(sklad, sw)

