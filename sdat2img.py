import os
import sys
import argparse
from Log import Log as logger

__version__ = '1.2'
BLOCK_SIZE = 4096


def rangeset(src):
    src_set = src.split(',')
    num_set = [int(item) for item in src_set]
    if len(num_set) != num_set[0] + 1:
        logger.error('Error parsing rangeset:\n{}'.format(src))
        sys.exit(1)
    return [(num_set[i], num_set[i + 1]) for i in range(1, len(num_set), 2)]


def parse_transfer_list_file(path):
    with open(path, 'r') as trans_list:
        version = int(trans_list.readline())
        new_blocks = int(trans_list.readline())

        if version >= 2:
            trans_list.readline()
            trans_list.readline()

        commands = []
        for line in trans_list:
            parts = line.split(' ')
            cmd = parts[0]
            if cmd in ['erase', 'new', 'zero']:
                commands.append((cmd, rangeset(parts[1])))
            elif not cmd[0].isdigit():
                logger.error('Invalid command "{}" in transfer list.'.format(cmd))
                sys.exit(1)
        return version, new_blocks, commands


def main(transfer_list_file, new_data_file, output_image_file, buffer_size=4096 * 1024):
    if sys.hexversion < 0x02070000:
        logger.error('Python 2.7 or newer is required.')
        sys.exit(1)

    version, new_blocks, commands = parse_transfer_list_file(transfer_list_file)
    android_versions = {1: 'Android Lollipop 5.0', 2: 'Android Lollipop 5.1', 3: 'Android Marshmallow 6.x', 4: 'Android Nougat 7.x / Oreo 8.x'}
    logger.info('{} detected!'.format(android_versions.get(version, 'Unknown Android version')))

    # if os.path.exists(output_image_file):
    #     logger.error('Output file "{}" already exists. Choose a different name or delete it.'.format(output_image_file))
    #     sys.exit(1)

    max_file_size = max(block[1] for cmd, blocks in commands for block in blocks) * BLOCK_SIZE

    with open(output_image_file, 'wb') as output_img, open(new_data_file, 'rb') as new_data:
        for cmd, blocks in commands:
            if cmd == 'new':
                for begin, end in blocks:
                    block_count = end - begin
                    output_img.seek(begin * BLOCK_SIZE)
                    while block_count > 0:
                        read_size = min(block_count * BLOCK_SIZE, buffer_size)
                        data = new_data.read(read_size)
                        output_img.write(data)
                        block_count -= read_size // BLOCK_SIZE

        if output_img.tell() < max_file_size:
            output_img.truncate(max_file_size)

    logger.success('Done! Output image: {}'.format(os.path.realpath(output_image_file)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert Android .dat/.br to .img file')
    parser.add_argument('transfer_list', help='Transfer list file path')
    parser.add_argument('new_data_file', help='System new dat file path')
    parser.add_argument('output_image', nargs='?', default='system.img', help='Output system image file name')
    parser.add_argument('--buffer-size', type=int, default=4096 * 1024, help='Buffer size in bytes (default: 4MB)')

    args = parser.parse_args()
    main(args.transfer_list, args.new_data_file, args.output_image, args.buffer_size)
