"""
Brovey pansharpening combines lower resolution color imagery and higher resolution
greyscale imagery to "sharpen" the color imagery, making it appear more detailed.

- https://github.com/mapbox/rio-pansharpen/blob/master/docs/pansharpening_methods.rst
- https://pro.arcgis.com/en/pro-app/latest/help/analysis/raster-functions/fundamentals-of-pan-sharpening-pro.htm  # noqa
- https://matplotlib.org/stable/tutorials/images.html
"""

import math
import sys

import numpy as np
from PIL import Image
from skimage import exposure


def create_greyscale(image: Image.Image) -> np.ndarray:
    image_data = np.asarray(image)
    return np.dot(image_data[..., :3], [1 / 3, 1 / 3, 1 / 3])


def create_lowres(image: Image.Image, resize_factor: int = 4) -> np.ndarray:
    resize_dimensions = int(image.size[0] / resize_factor), int(
        image.size[1] / resize_factor
    )
    resized = image.resize(resize_dimensions)
    return np.asarray(resized)


def setup() -> tuple[np.ndarray, np.ndarray]:
    original_image = Image.open("assets/tabby_cats.png")
    greyscale_band = create_greyscale(original_image)
    lowres_data = create_lowres(original_image)
    return lowres_data, greyscale_band


def nearest(arr: np.ndarray, zoom: int = 2) -> np.ndarray:
    zoomed_dim = arr.shape[0] * zoom, arr.shape[1] * zoom
    zoomed_arr = np.zeros(zoomed_dim)

    for i in range(zoomed_dim[0]):
        for j in range(zoomed_dim[1]):
            nearest_i = math.ceil((i + 1) / zoom) - 1
            nearest_j = math.ceil((j + 1) / zoom) - 1
            zoomed_arr[i][j] = arr[nearest_i][nearest_j]

    return zoomed_arr


def brovey(lowres_data: np.ndarray, greyscale_band: np.ndarray) -> np.ndarray:
    red_band, green_band, blue_band = (
        lowres_data[:, :, 0],
        lowres_data[:, :, 1],
        lowres_data[:, :, 2],
    )
    resize_factor = int(greyscale_band.shape[0] / red_band.shape[0])
    resized_red, resized_green, resized_blue = (
        nearest(red_band, resize_factor),
        nearest(green_band, resize_factor),
        nearest(blue_band, resize_factor),
    )
    new_red, new_green, new_blue = brovey_ratios(
        resized_red, resized_green, resized_blue, greyscale_band
    )
    clipped_red, clipped_green, clipped_blue = (
        np.clip(new_red, 0, 255),
        np.clip(new_green, 0, 255),
        np.clip(new_blue, 0, 255),
    )
    pansharpened = np.dstack((clipped_red, clipped_green, clipped_blue))
    return pansharpened


def brovey_ratios(
    red_band: np.ndarray,
    green_band: np.ndarray,
    blue_band: np.ndarray,
    greyscale_band: np.ndarray,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    for band in [red_band, green_band, blue_band]:
        mask_zeros(band)  # avoid division by zero

    normalization_factor = greyscale_band / (red_band + green_band + blue_band)
    red_out = red_band * normalization_factor
    green_out = green_band * normalization_factor
    blue_out = blue_band * normalization_factor
    return (
        red_out.astype(np.uint8),
        green_out.astype(np.uint8),
        blue_out.astype(np.uint8),
    )


def mask_zeros(arr: np.ndarray, replace_val: float = 1 / sys.maxsize) -> None:
    zero_mask = np.where(arr == 0)
    arr[zero_mask] = replace_val


def adjust_exposure(pansharpened: np.ndarray, lowres_data: np.ndarray) -> np.ndarray:
    # adjust exposure slightly depending on deviation from the lowres data
    if np.mean(pansharpened) < np.mean(lowres_data):
        return exposure.adjust_gamma(pansharpened, gamma=0.9)  # brighten
    else:
        return exposure.adjust_gamma(pansharpened, gamma=1.1)  # darken


if __name__ == "__main__":
    lowres_data, greyscale_band = setup()
    pansharpened = brovey(lowres_data, greyscale_band)
    adjusted = adjust_exposure(pansharpened, lowres_data)

    # save
    import matplotlib.image

    matplotlib.image.imsave("assets/tabby_cats__lowres.png", lowres_data)
    matplotlib.image.imsave(
        "assets/tabby_cats__greyscale.png", greyscale_band, cmap="gray"
    )
    matplotlib.image.imsave("assets/tabby_cats__pansharpened.png", adjusted)
