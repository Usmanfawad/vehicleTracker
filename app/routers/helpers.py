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