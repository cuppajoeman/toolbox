from PIL import Image
from mandelbrot import MandelbrotSet
from viewport import Viewport
import tqdm

rx = 16
ry = 9
rx = 1
ry = 5

make_y_depend_on_x = True

if make_y_depend_on_x:
    aspect_ratio = ry/rx
    horizontal_pixel_count = 2040
    vertical_pixel_count = int(horizontal_pixel_count * aspect_ratio)
else:
    aspect_ratio = rx/ry
    # increasing the resolution makes the image clearer
    vertical_pixel_count = 2040
    horizontal_pixel_count = int(vertical_pixel_count * aspect_ratio)


center = -0.7435 + 0.1314j
zoom = 200

center = 2.613577e-1 + -2.018128e-3j
zoom =3.354786e+3

# this increases the amount of color banding there would be
mandelbrot_detail_level = 9
# increasing this makes things that we thought unstable (white), become more stable and so this darkens the image,
# if this value were set to infinity, the entire image black, and set to 0 entirely white
escape_radius = 1000

# suppose that c = 1, then on each iteration z_n equals the number of iterations

max_iterations = 2**mandelbrot_detail_level

mandelbrot_set = MandelbrotSet(max_iterations=max_iterations, escape_radius=escape_radius)
image = Image.new(mode="L", size=(horizontal_pixel_count, vertical_pixel_count))

for pixel in tqdm.tqdm(Viewport(image, center=center, zoom=zoom)):
    c = complex(pixel)
    instability = 1 - mandelbrot_set.stability(c, smooth=True)
    pixel.color = int(instability * 255)

image.save(f'renders/mandelbrot_centered_at_{center}_zoomed_at_{zoom}x_with_resolution_{(horizontal_pixel_count, vertical_pixel_count)}px_escape_radius_set_to_{escape_radius}_with_max_iterations_of_{max_iterations}.png')
