from fastapi import FastAPI, HTTPException
from enum import Enum
from pydantic import BaseModel
import logging

# Initialize the logger
logger = logging.getLogger("temperature-control-api")
logger.setLevel(logging.INFO)

# Enum for zones
class Zone(str, Enum):
    LIVING_ROOM = "living_room"
    BEDROOM = "bedroom"
    KITCHEN = "kitchen"
    BATHROOM = "bathroom"
    OFFICE = "office"

# Data model for setting temperature
class TemperatureRequest(BaseModel):
    zone: Zone
    temp: int

# Initialize the FastAPI app
app = FastAPI()

# Initial temperatures for each zone
temperature_data = {
    Zone.LIVING_ROOM: 22,
    Zone.BEDROOM: 20,
    Zone.KITCHEN: 24,
    Zone.BATHROOM: 23,
    Zone.OFFICE: 21,
}

@app.get("/")
def home():
    return {"message": "Welcome to the Temperature Control API"}

@app.get("/temperature/{zone}")
def get_temperature(zone: Zone):
    """
    Get the current temperature of a specific zone.
    """
    logger.info("Fetching temperature for zone: %s", zone)
    if zone not in temperature_data:
        raise HTTPException(status_code=404, detail="Zone not found")
    temp = temperature_data[zone]
    return {"zone": zone, "temperature": f"{temp}C"}

@app.post("/temperature")
def set_temperature(request: TemperatureRequest):
    """
    Set the temperature for a specific zone.
    """
    logger.info("Setting temperature for zone: %s to %d", request.zone, request.temp)
    if request.zone not in temperature_data:
        raise HTTPException(status_code=404, detail="Zone not found")
    # Update the temperature
    temperature_data[request.zone] = request.temp
    return {"message": f"The temperature in the {request.zone} is now {request.temp}C"}
