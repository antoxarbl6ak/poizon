import json

with open("sklad.json", 'r') as sr:
    sklad = json.load(sr)

with open("deals.json", 'r') as dr:
    deals = json.load(dr)


async def upload(file="sklad"):
    if file == "sklad":
        with open("sklad.json", 'w') as sw:
            json.dump(sklad, sw)
    else:
        with open("deals.json", 'w') as dw:
            json.dump(deals, dw)


async def add_pair_load(data: dict):
    if data["brand"] in sklad:
        if data["name"] in (x["name"] for x in sklad[data["brand"]]):
            i = max(j for j in range(len(sklad[data["brand"]])) if sklad[data["brand"]][j]["name"] == data["name"])
            sklad[data["brand"]][i]["sizes"] = sorted(set(sklad[data["brand"]][i]["sizes"] + data["sizes"]))
        else:
            sklad[data["brand"]].append({"name": data["name"], "photo": data["photo"], "price": data["price"], "sizes": data["sizes"]})
    else:
        sklad[data["brand"]] = [{"name": data["name"], "photo": data["photo"], "price": data["price"], "sizes": data["sizes"]}]
    await upload()


async def remove_pair(product: str, sizes: str):
    for brand in sklad:
        i = max(j if sklad[brand][j]["name"] == product else -1 for j in range(len(sklad[brand])))
        if i + 1:
            if sizes == "all":
                sklad[brand].pop(i)
            elif sizes.replace(' ', '').isdigit():
                for size in sizes.split():
                    try:
                        sklad[brand][i]["sizes"].remove(size)
                    except ValueError:
                        pass
                if not len(sklad[brand][i]["sizes"]):
                    sklad[brand].pop(i)
            else:
                return "I couldn\'t find sizes:("
            if not len(sklad[brand]):
                sklad.pop(brand)
            await upload()
            return "was successfully removed"
    else:
        return "I couldn\'t find this:("


async def choose_pair(brand, i, mode):
    media = sklad[brand][i]["photo"]
    caption = f"{brand}\n{sklad[brand][i]['name']}: {sklad[brand][i]['price']}p\nsizes: {' '.join(sklad[brand][i]['sizes'])}"
    return {mode: media, "caption": caption}


async def add_deal(data):
    deals[data.pop("track")] = data
    await upload("deal")
