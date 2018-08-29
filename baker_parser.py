#!/usr/bin/env python3

import pdb
import json
import os
import os.path


# files = ["653-3.txt", "461-2.txt", "3240-2.txt", "6604-18.txt", "271-22.txt", "2264-3.txt", "3956-1.txt", "4416-1.txt", "5424-7.txt", "5026-1.txt", "7262-4.txt", "4205-2.txt", "20-3.txt", "2125-12.txt", "14-23.txt", "205-20.txt", "3151-3.txt", "2397-9.txt", "836-9.txt", "4866-3.txt", "1523-5.txt", "6506-2.txt", "286-24.txt", "2642-9.txt", "5989-1.txt", "2298-3.txt", "5989-2.txt", "5023-2.txt", "109-32.txt", "598-1.txt", "2970-5.txt", "4184-7.txt", "802-12.txt", "1261-5.txt", "18-6.txt", "68-8.txt", "4990-1.txt", "3431-12.txt", "901-30.txt", "4532-8.txt", "198-14.txt", "1882-6.txt", "1137-10.txt", "14-12.txt", "2151-9.txt", "3853-4.txt", "4472-4.txt", "6712-3.txt", "1770-4.txt", "24-30.txt", "783-14.txt", "4210-11.txt", "2785-1.txt", "3886-3.txt", "1069-1.txt", "6248-1.txt", "5077-6.txt", "6653-2.txt", "6195-5.txt", "1281-6.txt", "2162-2.txt", "5361-10.txt", "6320-7.txt", "6087-2.txt", "1180-17.txt", "3-9.txt", "4696-3.txt", "2924-6.txt", "2206-1.txt", "3755-1.txt", "6293-10.txt", "5029-6.txt", "836-11.txt", "1310-3.txt", "73-26.txt", "6568-5.txt", "4074-3.txt", "182-1.txt", "1805-2.txt", "2073-11.txt", "777-9.txt", "987-10.txt", "5213-1.txt", "106-1.txt", "3618-13.txt", "2619-2.txt", "2421-3.txt", "1730-2.txt", "3632-10.txt", "5365-7.txt", "6927-12.txt", "1590-3.txt", "2266-6.txt", "507-1.txt", "5438-9.txt", "1858-2.txt", "4810-9.txt", "5807-2.txt", "5089-2.txt", "3843-1.txt", "1349-3.txt", "2066-4.txt", "5825-3.txt", "1565-8.txt", "1614-8.txt", "2764-14.txt", "1758-18.txt", "4083-3.txt", "318-5.txt", "4391-8.txt", "1676-2.txt", "3831-2.txt", "1640-3.txt", "463-2.txt", "5950-2.txt", "4076-2.txt", "4596-6.txt", "109-16.txt", "6718-4.txt", "2996-9.txt", "6932-3.txt", "7133-11.txt", "2472-6.txt", "5926-6.txt", "5632-4.txt", "3550-2.txt", "5750-4.txt", "2826-5.txt", "3982-2.txt", "1009-5.txt", "4702-6.txt", "81-6.txt", "2340-13.txt", "5546-6.txt", "1434-10.txt", "4927-1.txt", "2943-1.txt", "583-18.txt", "1642-6.txt", "6983-3.txt", "1638-5.txt", "321-10.txt", "5895-5.txt", "414-37.txt", "907-9.txt", "718-5.txt", "4992-3.txt", "166-4.txt", "4971-15.txt", "841-5.txt", "2162-7.txt", "2951-1.txt", "6863-5.txt", "2517-6.txt", "2839-2.txt", "3306-8.txt", "2736-7.txt", "220-15.txt", "36-27.txt", "6060-3.txt", "5698-2.txt", "401-6.txt", "3704-7.txt", "1425-2.txt", "2549-3.txt", "5484-21.txt", "914-14.txt", "1144-5.txt", "3230-10.txt", "692-5.txt", "2178-16.txt", "1300-4.txt", "132-13.txt", "54-17.txt", "741-10.txt", "697-1.txt", "4956-6.txt", "1116-12.txt", "1925-5.txt", "1199-3.txt", "344-7.txt", "1046-1.txt", "305-9.txt", "6839-2.txt", "1729-10.txt", "6327-3.txt", "1250-5.txt", "1194-13.txt", "1006-6.txt", "492-2.txt", "3331-8.txt", "493-8.txt", "2155-9.txt", "2018-1.txt", "2276-9.txt", "159-5.txt", "6299-10.txt", "6403-6.txt", "2386-13.txt", "5533-9.txt", "6586-3.txt", "2816-6.txt", "5449-8.txt", "3350-1.txt", "2755-3.txt", "1897-1.txt", "4925-1.txt", "4609-5.txt", "406-15.txt", "3584-3.txt", "22-14.txt", "3932-2.txt", "6148-1.txt", "1551-2.txt", "4945-2.txt", "480-12.txt", "627-15.txt", "7205-4.txt", "5857-4.txt", "3962-17.txt", "432-6.txt", "4151-1.txt", "4652-6.txt", "5818-4.txt", "982-19.txt", "116-5.txt", "872-4.txt", "431-13.txt", "1199-25.txt", "6719-7.txt", "6231-7.txt", "5005-3.txt", "3044-4.txt", "5173-11.txt", "5087-3.txt", "5951-2.txt", "277-14.txt", "3593-2.txt", "2828-3.txt", "414-32.txt", "2899-2.txt", "2386-10.txt", "6599-15.txt", "2150-2.txt", "56-25.txt", "4693-1.txt", "407-12.txt", "2192-7.txt", "14-40.txt", "2261-2.txt", "608-1.txt", "6121-3.txt", "5222-1.txt", "4298-1.txt", "4041-10.txt", "676-10.txt", "2874-8.txt", "1733-18.txt", "6667-3.txt", "4520-6.txt", "5927-19.txt", "5913-6.txt", "3083-5.txt", "6381-8.txt", "36-6.txt", "470-21.txt", "289-21.txt", "1016-1.txt", "3773-24.txt", "361-6.txt", "2703-4.txt", "2463-2.txt", "5157-9.txt", "5141-8.txt", "6785-11.txt", "2007-2.txt", "4009-7.txt", "538-7.txt", "810-3.txt", "2265-18.txt", "1678-8.txt", "3769-4.txt", "2550-23.txt", "3676-5.txt", "3157-1.txt", "6619-9.txt", "956-9.txt", "32-2.txt", "6505-3.txt", "2893-5.txt", "2889-14.txt", "202-2.txt", "4719-4.txt", "831-5.txt", "2265-17.txt", "4012-3.txt", "1266-5.txt", "6600-6.txt", "1569-7.txt", "205-33.txt", "5355-4.txt", "2970-8.txt", "3326-8.txt", "1556-15.txt", "428-3.txt", "1147-4.txt", "6968-2.txt", "1322-11.txt", "4977-6.txt", "470-17.txt", "1865-2.txt", "6415-9.txt", "2674-3.txt", "5483-4.txt", "5387-9.txt", "1125-13.txt", "1636-3.txt", "5600-4.txt", "7088-7.txt", "1958-12.txt", "2509-8.txt", "1371-6.txt", "227-9.txt", "39-9.txt", "2843-3.txt", "5358-3.txt", "5023-7.txt", "2145-11.txt", "3422-36.txt", "582-6.txt", "2040-5.txt", "1635-5.txt", "1411-24.txt", "4281-2.txt", "592-8.txt", "6767-2.txt", "1927-5.txt", "3962-10.txt", "741-5.txt", "3246-2.txt", "2494-4.txt", "3547-11.txt", "4656-2.txt", "1498-14.txt", "4839-4.txt", "100-22.txt", "1078-8.txt", "1071-1.txt", "1733-13.txt", "6273-2.txt", "109-22.txt", "379-13.txt", "2721-9.txt", "6528-4.txt", "449-3.txt", "4208-5.txt", "1740-2.txt", "6400-8.txt", "2375-11.txt", "626-9.txt", "65-48.txt", "3911-2.txt", "6681-8.txt", "397-11.txt", "2239-17.txt", "3095-4.txt", "1186-2.txt", "456-22.txt", "5705-6.txt", "412-10.txt", "6988-6.txt", "492-6.txt", "3698-7.txt", "4077-11.txt", "175-3.txt", "1909-1.txt", "138-3.txt", "5527-6.txt", "1943-6.txt", "1321-8.txt", "4386-6.txt", "1122-3.txt", "1545-3.txt", "3490-8.txt", "444-1.txt", "3546-4.txt", "1960-3.txt", "3734-9.txt", "1979-4.txt", "3205-6.txt", "1583-4.txt", "2647-1.txt", "4928-3.txt", "1039-2.txt", "1549-1.txt", "2610-5.txt", "6379-1.txt", "1474-15.txt", "1486-11.txt", "2704-1.txt", "3180-11.txt", "2155-4.txt", "6561-4.txt", "7291-3.txt", "3877-3.txt", "753-3.txt", "3583-6.txt", "4053-8.txt", "280-17.txt", "711-3.txt", "151-5.txt", "4167-1.txt", "4808-3.txt", "2472-3.txt", "5830-21.txt", "7140-8.txt", "4219-1.txt", "4157-2.txt", "545-6.txt", "2493-9.txt", "290-12.txt", "728-2.txt", "592-18.txt", "1818-5.txt", "450-8.txt", "3-16.txt", "1861-3.txt", "6541-5.txt", "6431-4.txt", "6992-11.txt", "5145-5.txt", "336-11.txt", "6963-4.txt", "2340-1.txt", "2506-1.txt", "2260-2.txt", "3662-1.txt", "7135-1.txt", "150-12.txt", "1817-5.txt", "2887-5.txt", "648-12.txt", "50-10.txt", "2404-6.txt", "758-5.txt", "4581-1.txt", "2712-8.txt", "2300-2.txt", "1512-11.txt", "109-15.txt", "1841-1.txt", "2527-4.txt", "536-3.txt", "1083-7.txt", "2729-2.txt", "1398-4.txt", "1750-1.txt", "131-12.txt", "3678-5.txt", "2917-2.txt", "3121-5.txt", "6349-2.txt", "1605-1.txt", "6185-5.txt", "986-6.txt", "2827-7.txt", "6725-1.txt", "7297-9.txt", "7263-2.txt", "6469-1.txt", "407-8.txt", "341-1.txt", "2748-3.txt", "3542-3.txt", "2465-4.txt", "4058-2.txt", "6859-5.txt", "2614-4.txt", "109-33.txt", "1750-4.txt", "5577-2.txt", "3160-6.txt", "904-8.txt", "712-12.txt", "1390-12.txt", "3326-9.txt", "5495-5.txt", "5777-3.txt", "5707-5.txt", "2412-8.txt", "1540-3.txt", "6607-5.txt", "3587-5.txt", "1325-1.txt", "230-18.txt", "5292-4.txt", "6799-2.txt", "256-8.txt", "5016-5.txt", "4756-15.txt", "1366-6.txt", "3074-3.txt", "65-1.txt", "5903-3.txt", "5310-1.txt", "647-2.txt", "2600-1.txt", "4910-1.txt", "3296-3.txt", "4861-4.txt", "369-6.txt", "56-8.txt", "2865-1.txt", "5008-1.txt", "2924-7.txt", "7082-12.txt", "2996-4.txt", "3391-5.txt", "983-9.txt", "3-42.txt", "3749-4.txt", "126-14.txt", "4950-6.txt", "695-8.txt", "6487-8.txt", "3791-2.txt", "6367-1.txt", "5759-1.txt", "2783-3.txt", "1750-6.txt", "6309-2.txt", "897-4.txt", "6375-5.txt", "7234-3.txt", "5720-16.txt", "5050-4.txt", "6891-5.txt", "3968-1.txt", "3646-3.txt", "1130-14.txt", "560-2.txt", "1125-31.txt", "3318-7.txt", "6078-6.txt", "741-13.txt", "1338-6.txt", "4561-2.txt", "4430-7.txt", "1898-15.txt", "2666-4.txt", "4397-1.txt", "2110-1.txt", "5550-1.txt", "3925-2.txt", "349-13.txt", "3569-2.txt", "4513-2.txt", "155-5.txt", "6605-1.txt", "3234-3.txt", "701-3.txt", "6812-2.txt", "2-16.txt", "3094-5.txt", "6431-3.txt", "5973-3.txt", "1811-1.txt", "4612-4.txt", "6142-2.txt", "1615-12.txt", "362-7.txt", "4855-5.txt", "5877-2.txt", "1379-7.txt", "6378-5.txt", "2621-1.txt", "4674-1.txt", "2881-8.txt", "3229-3.txt", "1825-56.txt", "3443-1.txt", "390-7.txt", "6944-1.txt", "3543-3.txt", "6671-2.txt", "309-7.txt", "1995-6.txt", "4010-12.txt", "693-1.txt", "4290-8.txt", "956-2.txt", "6801-10.txt", "598-9.txt", "324-6.txt", "4186-6.txt", "133-6.txt", "2214-1.txt", "1506-1.txt", "2229-3.txt", "4578-3.txt", "1409-2.txt", "265-12.txt", "2096-4.txt", "5965-1.txt", "2435-5.txt", "2340-9.txt", "6574-4.txt", "333-20.txt", "1645-3.txt", "510-27.txt", "1558-9.txt", "1943-11.txt", "3916-5.txt", "3391-1.txt", "4316-2.txt", "1672-3.txt", "5040-16.txt", "923-13.txt", "3430-3.txt", "2132-7.txt", "5884-4.txt", "314-13.txt", "6415-2.txt", "2282-2.txt", "6404-3.txt", "781-7.txt", "3422-17.txt", "5562-4.txt"]


CODE_SNIPPETS_PATH = "/home/benyamin/Projects/thesis/src/code_snippets/"
BAKER_RESULTS_PATH = "/home/benyamin/Projects/Baker/java-snippet-parser/results/"
primitives = {"int", "Integer", "double", "Double","boolean", "Boolean", "char", "Character", "byte", "Byte", "short", "Short", "long", "Long", "float", "Float"}

def get_json_obj(baker_output_file):
    json_str = baker_output_file.read().replace('""', '"')
    return json.loads(json_str)


def obj_stats(obj):
    if type(obj["api_elements"]) is list:
        return len(obj["api_elements"])

    return 1

def analyze_obj(obj):
    res = {}
    if type(obj["api_elements"]) is list:
        for api in obj["api_elements"]:
            actual = []
            for el in api["elements"]:
                if el not in primitives and not el.startswith("java."):
                    actual.append(el)

            res[api["name"]] = actual
            
    else:
        print(obj)
        actual = []
        for el in obj["api_elements"]:
            if el not in primitives and not el.startswith("java."):
                actual.append(el)

        res[obj["api_elements"]["name"]] = actual

    return res

primitive = {"int", "double", "byte", "float", "char", "long", "short"}


def parse_baker(joutput):
    precise = []
    results = []
    # print(joutput)
    if type(joutput["api_elements"]) == list:
        for el in joutput["api_elements"]:
            # if el["precision"] == 1:
            #     print(el)

            if el["precision"] == "1" and not el["name"] in primitive:
                precise.append(el["elements"][0])

    else:
        if joutput["api_elements"]["precision"] == 1 and not joutput["api_elements"]["name"] in primitive:
            precise.append(joutput["api_elements"]["elements"][0])



    if len(precise) == 0:
        return None

    print("precise: " + precise.__str__())

    all_built_in = True

    for item in precise:
        if not item.startswith("java."):
            all_built_in = False
            break

    if all_built_in:
        results = precise

    else:
        for item in precise:
            if not item.startswith("java."):
                results.append(item)

    # pdb.set_trace()

    return results




def baker():
    items = []
    for file in files:
            # print()
            with open("code_snippets/" + file) as f:
                for i, l in enumerate(f):
                    pass

            items.append({
                "name": file,
                "size": os.path.getsize("code_snippets/" + file),
            })


    items = sorted(items, key=lambda item: item['size'])

    for item in items: 
        json_name = "baker_results/" + item["name"] + ".json"
        if os.path.isfile(json_name):
            with open(json_name) as json_file:
                json_str = json_file.read().replace('""', '"')
                json_data = json.loads(json_str)
                total = 0
                if len(json_data["api_elements"]) == 0:
                    print("-1")
                    continue

                if type(json_data["api_elements"]) is list:

                    for el in json_data["api_elements"]:
                        total += len(el["elements"])

                    print(total/len(json_data["api_elements"]))

                else:
                    print(len(json_data["api_elements"]["elements"]))
        else:
            print("Error")


def analyze_results():

    counter = 0
    total = 0

    files = os.listdir(CODE_SNIPPETS_PATH)

    for file in files:
        json_name = file + ".json"
        json_path = BAKER_RESULTS_PATH + json_name
        # print("Checking file: " + json_name)
        if os.path.exists(json_path):
            with open(json_path) as json_file:
                obj = get_json_obj(json_file)
                results = parse_baker(obj)

                if results:
                    counter += 1
                    print(results)

                total += 1


            # pdb.set_trace()

    print(counter)
    print(total)


if __name__=="__main__":
    # baker()
    analyze_results()