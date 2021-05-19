import os
import click
import sys

OUTPUT_ENCODING = "UTF-8"

def combine_path(input_path, output_file_name, file_name_suffix):
    if os.path.isdir(input_path):
        with click.progressbar(os.listdir(input_path), label='Info: Converting the files') as bar:
            for f in bar:
                pathname = os.path.join(input_path, f)
                if os.path.isdir(pathname):
                    combine_path(pathname,output_file_name)
                elif pathname.endswith(file_name_suffix):
                    combine_file(pathname, output_file_name)


def combine_file(input_file_name, output_file_name):

    with open(input_file_name, 'r', encoding=OUTPUT_ENCODING) as input_file, open(output_file_name, 'a', encoding=OUTPUT_ENCODING) as output_file:
        print('combining '+input_file_name)
        for each_line in input_file:
            if not each_line.startswith('#'):
                output_file.write(each_line)
        output_file.write('\n')


if __name__ == '__main__':
    # 可以讲一个文件夹及其子文件夹下的所有文本文件的内容合并到一个文件中
    if len(sys.argv) >= 4:
        output_file_name = sys.argv[3] #'output/lmc.conll'
        # os.remove(output_file_name)
        combine_path(sys.argv[1],output_file_name,sys.argv[2])
    else:
        print('usage: python combine_files.py input_dir file_name_suffix(.conll) output_file_name')