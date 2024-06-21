import json

with open("sklad.json", 'r') as sr:
    sklad = json.load(sr)


def add_pair_load(data: dict):
    if data["brand"] in sklad:
        if data["name"] in (x["name"] for x in sklad[data["brand"]]):
            i = max(j for j in range(len(sklad[data["brand"]])) if sklad[data["brand"]][j]["name"] == data["name"])
            sklad[data["brand"]][i]["sizes"] = sorted(set(sklad[data["brand"]][i]["sizes"] + data["sizes"]))
        else:
            sklad[data["brand"]].append({"name": data["name"], "photo": data["photo"], "price": data["price"], "sizes": data["sizes"]})
    else:
        sklad[data["brand"]] = [{"name": data["name"], "photo": data["photo"], "price": data["price"], "sizes": data["sizes"]}]
    with open("sklad.json", 'w') as sw:
        json.dump(sklad, sw)
