import requests
import uvicorn
from mcp.server.fastmcp import FastMCP

OPENWEATHER_API_KEY = "bf378e4a4db796edb04f652486bf3929"

mcp = FastMCP("Weather MCP")

@mcp.tool()
def get_coordinates(city: str):
    url = (
        "http://api.openweathermap.org/geo/1.0/direct"
        f"?q={city}&limit=1&appid={OPENWEATHER_API_KEY}"
    )
    response = requests.get(url).json()

    if not response:
        raise ValueError(f"Unknown city '{city}'")

    return {"lat": response[0]["lat"], "lng": response[0]["lon"]}

@mcp.tool()
def get_weather(lat, lng):
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lng}&units=metric&appid={OPENWEATHER_API_KEY}"
    )
    data = requests.get(url).json()

    if "main" not in data:
        raise RuntimeError(f"Weather API error: {data}")

    return {
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "description": data["weather"][0]["description"],
    }

@mcp.tool()
def get_city_weather(city: str):
    coords = get_coordinates(city)
    return get_weather(coords["lat"], coords["lng"])

app = mcp.sse_app()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
