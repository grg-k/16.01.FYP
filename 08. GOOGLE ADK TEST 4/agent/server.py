import requests
import uvicorn
from mcp.server.fastmcp import FastMCP
 
OPENWEATHER_API_KEY = ""
 
mcp = FastMCP("Weather MCP Server")
 
@mcp.tool(
        name="get_coordinates",
        description="Get the latitude and longitude of a city given its name.",
)
def get_coordinates(city: str):
   
    url = (
        "http://api.openweathermap.org/geo/1.0/direct"
        f"?q={city}&limit=1&appid={OPENWEATHER_API_KEY}"
    )
    response = requests.get(url).json()
 
    if not response:
        raise ValueError(f"Unknown city '{city}'")
 
    return {"lat": response[0]["lat"], "lng": response[0]["lon"]}
 
@mcp.tool(
        name="get_weather",
        description="Get the current weather for given latitude and longitude.",    
)
def get_weather(lat, lng):
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lng}&units=metric&appid={OPENWEATHER_API_KEY}"
    )
    data = requests.get(url).json()
 
    if "main" not in data:
        raise RuntimeError(f"Weather API error: {data}")
    
    print("data:", data)
 
    return {
        "temperature": data["main"]["temp"],
        "feels_like": data["main"]["feels_like"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
        "description": data["weather"][0]["description"],
    }
 
@mcp.tool(
    name = "get_city_weather",
    description = "Get the current weather for a given city by name.",
)

def get_city_weather(city: str):
    coords = get_coordinates(city)
    return get_weather(coords["lat"], coords["lng"])
   
if __name__ == "__main__":
    mcp.run(transport="sse")

