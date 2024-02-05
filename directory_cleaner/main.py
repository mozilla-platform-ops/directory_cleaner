#!/usr/bin/env python3

import argparse
import toml
import textwrap

import directory_cleaner.directory_cleaner as DC

def parse_config_file(config_path):
    with open(config_path, 'r') as file:
        config = toml.load(file)
    return config

def main():
    # Create ArgumentParser object
    parser = argparse.ArgumentParser(description='Delete items in a directory while excluding certain items.',
                                           formatter_class=argparse.RawDescriptionHelpFormatter,
      epilog=textwrap.dedent('''\
         config file format (toml):

            exclusion_patterns = [
                            'directory_a',  # all files in this directory be excluded from deletion
                            'file_xyz',
                        ]                             

         '''))

    # Add command line argument for config file path
    parser.add_argument('--config', '-c', dest='config_file', type=str, required=True,
                        help='Path to the config file in INI format.')
    parser.add_argument('--dry-run', '-d', dest='dry_run', action='store_true', help="Don't delete anything, just print what would be deleted.")
    parser.add_argument('directory', type=str, help='The directory to clean.')

    # Parse command line arguments
    args = parser.parse_args()

    # Parse the config file
    config_path = args.config_file
    config = parse_config_file(config_path)

    # Print the parsed config
    for key, value in config.items():
        print(f'{key} = {value}')

if __name__ == '__main__':
    main()
