def parse_distance_matrix_result(response):
    parsed_dict = {
        "destination" : {
            "name": response['destination_addresses'][0],
            "gps_coordinates": response["rows"][0]["elements"][0]["destination"]
        },
        "origin" : {
            "name": response['origin_addresses'][0],
            "gps_coordinates": response["rows"][0]["elements"][0]["origin"]
        },
        "in_m" : response["rows"][0]["elements"][0]["distance"]["value"],
        "in_s" : response["rows"][0]["elements"][0]["duration"]["value"],
    }
    return parsed_dict


def parse_distance_matrices(response):
    lst_all_busses = []
    destination_addresses = response["destination_addresses"]
    origin_address = response["origin_addresses"][0]  # 0 because there will always be 1 origin per request
    data_response = response["rows"][0]["elements"]

    for each_resp in range(len(data_response)):
        try:
            dict_to_append = {
                "destination": {
                    "name": destination_addresses[each_resp],
                    "gps_coordinates": data_response[each_resp]["destination"]
                },
                "origin": {
                    "name": origin_address,
                    "gps_coordinates": data_response[each_resp]["origin"]
                },
                "in_m": data_response[each_resp]["distance"]["value"],
                "in_s": data_response[each_resp]["duration"]["value"],
            }
            lst_all_busses.append(dict_to_append)
        except Exception:
            dict_to_append = {
                "destination": {
                    "name": destination_addresses[each_resp],
                    "gps_coordinates": data_response[each_resp]["destination"]
                },
                "origin": {
                    "name": origin_address,
                    "gps_coordinates": data_response[each_resp]["origin"]
                },
                "in_m": 0,
                "in_s": 0,
            }
            lst_all_busses.append(dict_to_append)

    return lst_all_busses

