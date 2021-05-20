# Brat and CoNLL Converter

## Description

该程序支持从brat格式与conll标准格式之间的双向转换。两种格式中均包含词、词性、句法标签、父结点四种信息。

关于brat标注工具及其格式可以参见[here](http://brat.nlplab.org/standoff.html).

使用时请安装python3.7。（请注意，brat的运行需要python2.7，两者需要运行在不同的虚拟环境中。）


## Using the tool

### Installation/安装

首先，需要安装pip和git [here](https://pip.pypa.io/en/stable/installing/).

首次安装时，使用git clone命令下载软件包并安装 

```
git clone https://github.com/qiulikun/brat_and_conll_converter.git
cd brat_and_conll_converter
pip install .
```

已安装的情况下，如果需要更新代码，可以使用如下命令(请确保当前终端位于brat_and_conll_converter目录下)重新拉取代码并安装：

```
git pull origin
pip install .
```

### Execution/执行，brat向conll的转换

从brat向conll的转换，可以基于以下命令:

如果输入是一个文件夹:

```
brat2conll -i data
```

如果输入是一个文件:

```
brat2conll -i data/input_file_name.ann
```

如果在处理过程中希望程序打印更多信息，可以加上 (-v):
```
brat2conll -i data/tibetan/lmc -v
```

### Execution/执行，文件合并

如果需要将多个文件合并，可以使用以下命令(data/tibetan/lmc为待合并的文件所处的目录 .conll为待合并的文件的扩展名/文件名后缀 output/lmc.conll为输出文件名)，将目录下以.conll为扩展名的文件并输入到一个文件中：
```
python utils/combine_files.py data/tibetan/lmc .conll output/lmc.conll
```

### Execution/执行，从conll格式到brat格式的转换

如果需要将一个文件中conll格式的数据（通常是自动句法分析器的输出结果）转换到brat格式（以供放到brat环境中进行人工标注），可以使用以下命令(output/brat为输出的brat格式文件将要存放的目录， output/lmc.conll为conll格式的文件名即输入文件名)：
```
python conll2brat/conll092brat.py -o output/brat output/lmc.conll
```

To view all the possible options, use the --help option like this:
```
brat2conll --help
```

If you don't use any arguments, it will prompt for the input file path as follows:
```
$ brat2conll
Input path: data
Info: Converting the files  [####################################]  100%
```
