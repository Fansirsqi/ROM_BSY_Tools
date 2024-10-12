from __future__ import print_function

import os
import sys

from utils import logger


def main(TRANSFER_LIST_FILE, NEW_DATA_FILE, OUTPUT_IMAGE_FILE):
    __version__ = '1.2'

    if sys.hexversion < 0x02070000:
        logger.error('Python 2.7 or newer is required.')
        input('Press ENTER to exit...')
        sys.exit(1)
    else:
        logger.info('sdat2img binary - version: {}\n'.format(__version__))

    def rangeset(src):
        src_set = src.split(',')
        num_set = [int(item) for item in src_set]
        if len(num_set) != num_set[0] + 1:
            logger.error('Error on parsing following data to rangeset:\n{}'.format(src))
            sys.exit(1)
        return tuple([(num_set[i], num_set[i + 1]) for i in range(1, len(num_set), 2)])

    def parse_transfer_list_file(path):
        with open(TRANSFER_LIST_FILE, 'r') as trans_list:
            version = int(trans_list.readline())
            new_blocks = int(trans_list.readline())

            if version >= 2:
                trans_list.readline()
                trans_list.readline()

            commands = []
            for line in trans_list:
                line = line.split(' ')
                cmd = line[0]
                if cmd in ['erase', 'new', 'zero']:
                    commands.append([cmd, rangeset(line[1])])
                elif not cmd[0].isdigit():
                    logger.error('Command "{}" is not valid.'.format(cmd))
                    sys.exit(1)
            return version, new_blocks, commands

    BLOCK_SIZE = 4096
    BUFFER_SIZE = 1024 * BLOCK_SIZE

    version, new_blocks, commands = parse_transfer_list_file(TRANSFER_LIST_FILE)

    if version == 1:
        logger.info('Android Lollipop 5.0 detected!\n')
    elif version == 2:
        logger.info('Android Lollipop 5.1 detected!\n')
    elif version == 3:
        logger.info('Android Marshmallow 6.x detected!\n')
    elif version == 4:
        logger.info('Android Nougat 7.x / Oreo 8.x detected!\n')
    else:
        logger.warning('Unknown Android version!\n')

    if os.path.exists(OUTPUT_IMAGE_FILE):
        logger.error('Error: the output file "{}" already exists'.format(OUTPUT_IMAGE_FILE))
        logger.error('Remove it, rename it, or choose a different file name.')
        sys.exit(1)

    with open(OUTPUT_IMAGE_FILE, 'wb') as output_img, open(NEW_DATA_FILE, 'rb') as new_data_file:
        max_file_size = max(pair[1] for command in commands for pair in command[1]) * BLOCK_SIZE

        for command in commands:
            if command[0] == 'new':
                for block in command[1]:
                    begin, end = block
                    block_count = end - begin
                    logger.info('Copying {} blocks into position {}...'.format(block_count, begin))
                    output_img.seek(begin * BLOCK_SIZE)

                    while block_count > 0:
                        read_size = min(block_count * BLOCK_SIZE, BUFFER_SIZE)
                        new_data = new_data_file.read(read_size)
                        output_img.write(new_data)
                        block_count -= read_size // BLOCK_SIZE

        if output_img.tell() < max_file_size:
            output_img.truncate(max_file_size)

    logger.success('Done! Output image: {}'.format(os.path.realpath(OUTPUT_IMAGE_FILE)))


if __name__ == '__main__':
    try:
        TRANSFER_LIST_FILE = str(sys.argv[1])
        NEW_DATA_FILE = str(sys.argv[2])
    except IndexError:
        logger.error('\nUsage: sdat2img.py <transfer_list> <system_new_file> [system_img]\n')
        logger.error('    <transfer_list>: transfer list file')
        logger.error('    <system_new_file>: system new dat file')
        logger.error('    [system_img]: output system image\n\n')
        input('Press ENTER to exit...')
        sys.exit()

    try:
        OUTPUT_IMAGE_FILE = str(sys.argv[3])
    except IndexError:
        OUTPUT_IMAGE_FILE = 'system.img'

    main(TRANSFER_LIST_FILE, NEW_DATA_FILE, OUTPUT_IMAGE_FILE)
