# Image Change-Colour Tool

This is a simple tool to change the colour of an image. It is written in Python 3 and uses the Pillow library.

## Usage

1. Install the Pillow library: `pip install Pillow`
2. Run the script: `python main.py`, with the following arguments:
    - `--in_root`: The root directory of the input images;
    - `--out_root`: The root directory of the output images;
    - `--in_fn`: Optional name of image within the input root directory; if not specified, all images in the input root directory will be processed;
    - `--img_format`: input format of the image (default: `png`);
    - `--src_col`: the source colour to be changed;
    - `--dst_col`: the target (destination) colour to be changed to.
    - `--thres`: the threshold distance for considering a pixel to be of the source colour (default: 100).
    - `--sigma`: the standard deviation of the Gaussian kernel for blurring the image (default: 10).
    - `--smooth_iter`: the number of iterations for smoothing the image by blending each pixel with its neighbours (default: 3).
3. The output images will be saved in the output root directory. 🍺

## Example
Changing the red colours of the image `example.png` in `images_in` directory to green, and saving the output image in `images_out` directory:
```
python change-colour.py --in_root images_in --out_root images_out --in_fn example.png --src_col red --tgt_col green
```

<figure>
<img src="./images_in/example.png" alt="Trulli" style="width:50%">
<figcaption><b>Input image before colour-changing.</b></figcaption>
</figure>

<figure>
<img src="./images_out/example_red2green.png" alt="Trulli" style="width:50%">
<figcaption><b>Output image after changing the red colours to green.</b></figcaption>
</figure>

