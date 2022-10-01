from PIL import Image
import argparse
import numpy as np
import os
import glob


IN_COLOURS = {
    'red': np.array([220, 60, 60]),
    'green': np.array([60, 220, 60]),
    'blue': np.array([60, 60, 220]),
    'yellow': np.array([220, 220, 60]),
    'magenta': np.array([220, 60, 220]),
    'cyan': np.array([60, 220, 220]),
    'white': np.array([255, 255, 255]),
    'black': np.array([0, 0, 0]),
}

OUT_COLOURS = {
    'red': np.array([170, 80, 80]),
    'green': np.array([80, 170, 80]),
    'blue': np.array([80, 80, 170]),
    'yellow': np.array([170, 170, 80]),
    'magenta': np.array([170, 80, 170]),
    'cyan': np.array([80, 170, 170]),
    'white': np.array([255, 255, 255]),
    'black': np.array([0, 0, 0]),
}


def euclidean_distance(x, y):
    return np.sqrt(np.sum((x - y) ** 2))


def gaussian_disturbance(x, sigma):
    ret = np.random.normal(x, sigma)
    ret = np.clip(ret, 0, 255)
    return ret


def smooth_colour(colour_dct):
    new_colour_dct = {}
    for (i, j) in colour_dct:
        cols_to_avg = [colour_dct[(i, j)]]
        if (i-1, j) in colour_dct:
            cols_to_avg.append(colour_dct[(i-1, j)])
        if (i+1, j) in colour_dct:
            cols_to_avg.append(colour_dct[(i+1, j)])
        if (i, j-1) in colour_dct:
            cols_to_avg.append(colour_dct[(i, j-1)])
        if (i, j+1) in colour_dct:
            cols_to_avg.append(colour_dct[(i, j+1)])
        new_col = np.mean(cols_to_avg, axis=0)
        assert all([0 <= x <= 255 for x in new_col])
        new_colour_dct[(i, j)] = new_col
    return new_colour_dct


def main(args):
    if args.in_fn is not None:
        in_fns = [os.path.join(args.in_root, args.in_fn)]
    else:
        in_fns = glob.glob(os.path.join(args.in_root, f'*.{args.img_format}'))

    if not os.path.exists(args.out_root):
        os.makedirs(args.out_root)

    for in_fn in in_fns:
        inf_name_lst = os.path.basename(in_fn).split('.')
        inf_name, inf_type = '.'.join(inf_name_lst[:-1]), inf_name_lst[-1]
        out_fn = os.path.join(args.out_root, f'{inf_name}_{args.out_suff}.{inf_type}')
        print(f'Processing {in_fn}, saving to {out_fn}')
        image = Image.open(in_fn).convert('RGB')
        pixels = image.load()
        min_dist = 1000000
        changed_pixels = {}
        for i in range(image.size[0]):
            for j in range(image.size[1]):
                curr_dist = euclidean_distance(np.array(pixels[i, j]), np.array(IN_COLOURS[args.src_col]))
                if curr_dist < args.thres:
                    tmp = OUT_COLOURS[args.dst_col] - OUT_COLOURS[args.src_col] + np.array(pixels[i, j])
                    tmp = gaussian_disturbance(tmp, args.sigma)
                    changed_pixels[(i, j)] = np.array([int(tmp[0]), int(tmp[1]), int(tmp[2])])
                min_dist = min(min_dist, curr_dist)

        print(f"min_dist: {min_dist}")

        for ite in range(args.smooth_iter):
            changed_pixels = smooth_colour(changed_pixels)

        for i in range(image.size[0]):
            for j in range(image.size[1]):
                if (i, j) in changed_pixels:
                    tup = tuple(int(x) for x in changed_pixels[(i, j)])
                    pixels[i, j] = tup

        image.save(out_fn)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--in_root', type=str, default='images_in',
                        help='root directory for input images, always set this to the correct value.')
    parser.add_argument('--out_root', type=str, default='images_out',
                        help='root directory for storing output images, always set this to the correct value.')
    parser.add_argument('--in_fn', type=str, default=None,
                        help='Optional, if set, only process this file in the input directory.')
    parser.add_argument('--img_format', type=str, default='png', help='image format, e.g. png, jpg, jpeg, etc.')
    parser.add_argument('--src_col', type=str, default='red', help='source colour, e.g. white, black, etc.')
    parser.add_argument('--dst_col', type=str, default='green', help='destination colour, e.g. white, black, etc.')
    parser.add_argument('--thres', type=float, default=100.0, help='threshold for colour distance.')
    parser.add_argument('--sigma', type=float, default=10.0, help='sigma for gaussian disturbance.')
    parser.add_argument('--smooth_iter', type=int, default=3,
                        help='number of iterations to smooth the changed colours in each pixel with its neighbours.')

    args = parser.parse_args()
    args.out_suff = f'{args.src_col}2{args.dst_col}'

    main(args)

