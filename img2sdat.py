#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ====================================================
#          FILE: img2sdat.py
#          AUTHORS: xpirt - luxi78 - howellzhu
#          DATE: 2018-05-25 12:19:12 CEST
# ====================================================

import os
import sys
import argparse
import tempfile
import blockimgdiff
import sparse_img

__version__ = '1.7'


def main(input_image, outdir='.', version=4, prefix='system'):
    if sys.hexversion < 0x02070000:
        print('Python 2.7 or newer is required.', file=sys.stderr)
        sys.exit(1)

    # Create output directory
    output_dir = os.path.join(outdir, prefix)
    os.makedirs(output_dir, exist_ok=True)

    # Process the sparse image
    print(f'Processing input image: {input_image} with Android version: {version}')
    with tempfile.NamedTemporaryFile() as temp_file:
        image = sparse_img.SparseImage(input_image, temp_file.name, '0')

        # Generate output files
        block_diff = blockimgdiff.BlockImageDiff(image, None, version)
        block_diff.Compute(output_dir)

    print(f'Done! Output files are located in: {output_dir}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert .img file to Android .dat format with transfer list')
    parser.add_argument('input_image', help='Input image file path')
    parser.add_argument('--outdir', default='.', help='Output directory for generated files')
    parser.add_argument('--version', type=int, choices=[1, 2, 3, 4], default=4, help='Android version: 1=Lollipop 5.0, 2=Lollipop 5.1, 3=Marshmallow 6.0, 4=Nougat 7.0/7.1/8.0/8.1')
    parser.add_argument('--prefix', default='system', help="Prefix for output files (default: 'system')")
    args = parser.parse_args()
    main(args.input_image, args.outdir, args.version, args.prefix)
