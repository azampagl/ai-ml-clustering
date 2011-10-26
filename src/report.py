"""
"""
import commands

INPUT = "../data/news/news-topics.txt"

OUTPUT = "tmp"

results = {'k-means': {},
           'bi-k-means-size': {},
           'bi-k-means-sim': {},
           'agg-ist': {},
           'agg-cst': {},
           'agg-upgma': {},
           'agg-upgma-k-means': {},
            }

# Vary i
MAX_K = 11
for k in range(1, MAX_K):
    for algo in results:
        
        cmd = "python main.py" + \
            " -t \"" + INPUT + "\"" + \
            " -a \"" + algo + "\"" + \
            " -k " + str(k) + \
            " -i 4" + \
            " -o " + OUTPUT + \
            " -r " + OUTPUT
        
        #print(cmd)
        results[algo][k] = commands.getstatusoutput(cmd)[1].split("\t")

for index in range(4):
    output = "ITER\t" + "\t".join(results.keys()) + "\n"
    for k in range(1, MAX_K):
        output += str(k) + "\t"
        for algo, result in results.items():
            output += result[k][index] + "\t"
        output += "\n"
    print(output)
    print("")