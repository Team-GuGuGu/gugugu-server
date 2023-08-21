import re

def meal_parser(menu: str):
    menu, allergy = meal_edit(menu)
    allergy = meal_allergy_to_string(meal_allergy(str(allergy)))
    print(menu)
    print(allergy)
    return (menu, allergy)

def meal_edit(menu: str):
    allergy = []
    regex = re.compile(r'\(([\d.]+)\)')
    
    text = ""
    for match in regex.findall(menu):
        allergy.append(match)
    
    text = regex.sub('', menu).strip()
    text = text.split("<br/>")
    
    return (text, allergy)

def remove_duplicates_sorted(input_list):
    return sorted(set(input_list))

def meal_allergy(menu: str):
    replaceList = menu.replace("[", "").replace("]", "").replace("(", "").replace(")", "").replace(".", ",").replace(" ", "").split(",")
    allergyList = list(map(lambda i: int(i.replace("'", "")), filter(lambda i: i != "'", replaceList)))
    sortList = remove_duplicates_sorted(allergyList)
    return sortList

def meal_allergy_to_string(data: list):
    text = ""
    for i in data:
        if i == 1:
            text += "①난류(가금류) "
        elif i == 2:
            text += "②우유 "
        elif i == 3:
            text += "③메밀 "
        elif i == 4:
            text += "④땅콩 "
        elif i == 5:
            text += "⑤대두 "
        elif i == 6:
            text += "⑥밀 "
        elif i == 7:
            text += "⑦고등어 "
        elif i == 8:
            text += "⑧게 "
        elif i == 9:
            text += "⑨새우 "
        elif i == 10:
            text += "⑩돼지고기 "
        elif i == 11:
            text += "⑪복숭아 "
        elif i == 12:
            text += "⑫토마토 "
        elif i == 13:
            text += "⑬아황산류 "
        elif i == 14:
            text += "⑭호두 "
        elif i == 15:
            text += "⑮닭고기 "
        elif i == 16:
            text += "⑯쇠고기 "
        elif i == 17:
            text += "⑰오징어 "
        elif i == 18:
            text += "⑱조개류(굴, 전복, 홍합)"
    return text