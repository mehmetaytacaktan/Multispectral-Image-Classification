import rasterio
import numpy as np
import matplotlib.pyplot as plt


def read_band(file_path):
    with rasterio.open(file_path) as src:
        return src.read(1), src.profile


def plot_image(image, title, colormap='viridis'):
    plt.figure(figsize=(10, 10))
    plt.imshow(image, cmap=colormap)
    plt.colorbar()
    plt.title(title)
    plt.show()


def plot_rgb_image(image, title):
    plt.figure(figsize=(10, 10))
    plt.imshow(image.astype(np.uint8))
    plt.title(title)
    plt.show()


def calculate_ndvi(red_band, nir_band):
    np.seterr(divide='ignore', invalid='ignore')
    ndvi = (nir_band - red_band) / (nir_band + red_band)
    ndvi[np.isnan(ndvi)] = 0  # Replace NaN values with 0
    ndvi = np.clip(ndvi, -1, 1)  # Ensure NDVI values are between -1 and 1
    return ndvi


def calculate_temperature(band_10, band_11):
    # For simplicity, this function just averages the two thermal bands
    temperature = (band_10 + band_11) / 2
    return temperature


def main():
    # File paths
    band_2_path = 'datasets/landsat_band2.TIF'  # Blue
    band_3_path = 'datasets/landsat_band3.TIF'  # Green
    band_4_path = 'datasets/landsat_band4.TIF'  # Red
    band_5_path = 'datasets/landsat_band5.TIF'  # Near Infrared
    band_6_path = 'datasets/landsat_band6.TIF'  # SWIR 1
    band_7_path = 'datasets/landsat_band7.TIF'  # SWIR 2
    band_10_path = 'datasets/landsat_band10.TIF'  # Thermal 1
    band_11_path = 'datasets/landsat_band11.TIF'  # Thermal 2

    # Reading bands
    blue_band, profile = read_band(band_2_path)
    green_band, _ = read_band(band_3_path)
    red_band, _ = read_band(band_4_path)
    nir_band, _ = read_band(band_5_path)
    swir1_band, _ = read_band(band_6_path)
    swir2_band, _ = read_band(band_7_path)
    thermal1_band, _ = read_band(band_10_path)
    thermal2_band, _ = read_band(band_11_path)

    # Normalize bands for RGB visualization
    def normalize(array):
        array_min, array_max = array.min(), array.max()
        return ((array - array_min) / (array_max - array_min) * 255).astype(np.uint8)

    red_band_norm = normalize(red_band)
    green_band_norm = normalize(green_band)
    blue_band_norm = normalize(blue_band)
    nir_band_norm = normalize(nir_band)

    # RGB Image
    rgb_image = np.dstack((red_band_norm, green_band_norm, blue_band_norm))
    plot_rgb_image(rgb_image, 'RGB Image')

    # False Color Image
    false_color_image = np.dstack((nir_band_norm, red_band_norm, green_band_norm))
    plot_rgb_image(false_color_image, 'False Color Image')

    # NDVI
    ndvi = calculate_ndvi(red_band, nir_band)
    plot_image(ndvi, 'NDVI', colormap='RdYlGn')

    # Temperature Map
    temperature = calculate_temperature(thermal1_band, thermal2_band)
    plot_image(temperature, 'Temperature Map', colormap='hot')

    # Atmospheric Correction Placeholder
    # Actual atmospheric correction would require complex algorithms and calibration data
    atmospheric_corrected = (swir1_band + swir2_band) / 2  # This is a placeholder
    plot_image(atmospheric_corrected, 'Atmospheric Correction (Placeholder)')


if __name__ == "__main__":
    main()
