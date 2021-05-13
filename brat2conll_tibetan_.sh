brat2conll -i data/tibetan/lmc -v >log/lmc.txt
brat2conll -i data/tibetan/yzannotation1 -v >log_yzannotation1.txt
brat2conll -i data/tibetan/yzannotation-dqc1 -v >log/lmc_dqc1.txt
brat2conll -i data/tibetan/yzannotation-hjc1 -v >log/lmc_hjc1.txt
brat2conll -i data/tibetan/yzannotation-hjc2 -v >log/lmc_hjc2.txt
brat2conll -i data/tibetan/yzannotation-hjcr1 -v >log/lmc_hjcr1.txt
brat2conll -i data/tibetan/yzannotation-lmc1 -v >log/lmc_lmc1.txt
brat2conll -i data/tibetan/yzannotation-xwzm1 -v >log/lmc_xwzm1.txt

python utils/combine_files.py data/tibetan/lmc .conll output/lmc.conll
python utils/combine_files.py data/tibetan/yzannotation-dqc1 .conll output/lmc_dqc1.conll
python utils/combine_files.py data/tibetan/yzannotation-hjc1 .conll output/lmc_hjc1.conll
python utils/combine_files.py data/tibetan/yzannotation-hjc2 .conll output/lmc_hjc2.conll
python utils/combine_files.py data/tibetan/yzannotation-hjcr1 .conll output/lmc_hjcr1.conll
python utils/combine_files.py data/tibetan/yzannotation-lmc1 .conll output/lmc_lmc1.conll
python utils/combine_files.py data/tibetan/yzannotation-xwzm1 .conll output/lmc_xwzm1.conll

#python utils/combine_files.py output/tibetan_treeank_20210306/ .conll output/tibetan_treeank_20210306.conll

#python conll2brat/conll092brat.py -o output/brat ../BiaffineDParserPMT/data/tibetan/ceshi1w_tagged_conll.txt.out
