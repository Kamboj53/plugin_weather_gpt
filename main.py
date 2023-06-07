from flask import Flask, jsonify, request, send_from_directory
import requests
# from waitress import serve
app = Flask(__name__)

def get_weather(api_key, location_key):
    base_url = "http://dataservice.accuweather.com/currentconditions/v1/"
    endpoint = f"{location_key}?apikey={api_key}"

    try:
        response = requests.get(base_url + endpoint)
        if response.status_code == 200:
            data = response.json()
            weather_info = data[0]
            temperature = weather_info["Temperature"]["Metric"]["Value"]
            weather_text = weather_info["WeatherText"]
            return {
                "temperature": temperature,
                "weather": weather_text
            }
        else:
            return {"error": "Error occurred while retrieving weather data."}
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

@app.route('/weather', methods=['GET'])
def weather():
    api_key = "Your api key"  # Replace with your own AccuWeather API key
    location_key = request.args.get('location')  # Retrieve the 'location' query parameter

    if not location_key:
        return jsonify({"error": "Missing 'location' parameter."}), 400

    weather_data = get_weather(api_key, location_key)

    return jsonify(weather_data)

@app.route('/.well-known/ai-plugin.json')
def serve_ai_plugin():
    return send_from_directory('.', 'ai-plugin.json', mimetype = 'application/json')

@app.route('/.well-known/openapi.yaml')
def serve_openapi_yaml():
    return send_from_directory('.', 'openapi.yaml', mimetype = 'text/yaml')

if __name__ == '__main__':
    # serve(app, host="0.0.0.0", port=5000)
    app.run()




# def get_location_key(api_key, location_name):
#     base_url = "http://dataservice.accuweather.com/locations/v1/cities/search"
#     query_params = {
#         "apikey": api_key,
#         "q": location_name
#     }

#     try:
#         response = requests.get(base_url, params=query_params)
#         if response.status_code == 200:
#             data = response.json()
#             if data:
#                 location_key = data[0]["Key"]
#                 print(f"Location Key for '{location_name}': {location_key}")
#             else:
#                 print("Location not found.")
#         else:
#             print("Error occurred while retrieving location data.")
#     except requests.exceptions.RequestException as e:
#         print("Error occurred:", e)

