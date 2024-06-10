from flask import make_response


# This function will build a response for a CORS preflight request
# (I'm using it in the cross_origin_db decorator)
def _build_cors_preflight_response():
    response = make_response()
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

# This function will add the CORS headers to the actual response
def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
