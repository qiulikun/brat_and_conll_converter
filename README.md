# Brat and CoNLL Converter

## Description

该程序支持从brat格式与conll标准格式之间的双向转换。两种格式中均包含词、词性、句法标签、父结点四种信息。

关于brat标注工具及其格式可以参见[here](http://brat.nlplab.org/standoff.html).

使用时请安装python3.7。（请注意，brat的运行需要python2.7，两者需要运行在不同的虚拟环境中。）


## Using the tool

### Installation

首先，需要安装pip和git [here](https://pip.pypa.io/en/stable/installing/).

之后，基于git下载软件包

```
git clone https://github.com/cdli-gh/brat_to_cdli_conll_converter.git
cd brat_to_cdli_conll_converter
pip install .
```

### Execution

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

如果需要将多个文件合并，可以使用以下命令：
```
python utils/combine_files.py data/tibetan/lmc .conll output/lmc.conll
```

如果需要将一个文件中conll格式的数据（通常是自动句法分析器的输出结果）转换到brat格式（以供放到brat环境中进行人工标注），可以使用以下命令：
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
```# brat-conll-converter
