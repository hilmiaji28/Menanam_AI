import ee

ee.Initialize(project="menanam-ai")

# Cirebon
point = ee.Geometry.Point([108.56, -6.73])

image = (
    ee.ImageCollection("COPERNICUS/S2_SR_HARMONIZED")
    .filterBounds(point)
    .filterDate("2025-01-01", "2025-06-01")
    .sort("CLOUDY_PIXEL_PERCENTAGE")
    .first()
)

print(image.getInfo()["id"])

ndvi = image.normalizedDifference(
    ["B8", "B4"]
).rename("NDVI")

value = ndvi.reduceRegion(
    reducer=ee.Reducer.mean(),
    geometry=point.buffer(500),
    scale=10
)

print(value.getInfo())