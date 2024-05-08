python3 process.py /Rules/data/LungCancer.nt /Rules/data/LungCancer.tsv
java -Xmx16g -jar /Rules/amie3.jar -const /Rules/data/LungCancer.tsv > /Rules/data/LungCancer.txt
python3 genRules.py /Rules/data/LungCancer.txt /result/LungCancer-rules.csv