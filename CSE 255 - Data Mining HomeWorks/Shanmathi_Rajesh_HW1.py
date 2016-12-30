# Name:Shanmathi Rajesh
# Email:shrajesh@eng.ucsd.edu

from pyspark import SparkContext
sc = SparkContext()

import re
textRDD = sc.newAPIHadoopFile('/data/Moby-Dick.txt',
                              'org.apache.hadoop.mapreduce.lib.input.TextInputFormat',
                              'org.apache.hadoop.io.LongWritable',
                              'org.apache.hadoop.io.Text',
                               conf={'textinputformat.record.delimiter': "\r\n\r\n"}).map(lambda x: x[1])
 
sentences = textRDD.flatMap(lambda x: x.split(". "))
 

regex=r"[^a-zA-Z\d]"
formatted_sentences = sentences.map(lambda x:re.sub(regex," ",x))
formatted_sentences = formatted_sentences.map(lambda x: re.sub("\s+"," ",x)).filter(lambda x:x!="")\
                                         .map(lambda word: word.lower())\
                                         .map(lambda x:x.split())                     
 

def printOutput(n,freq_ngramRDD):
    top=freq_ngramRDD.take(5)
    print '\n============ %d most frequent %d-grams'%(5,n)
    print '\nindex\tcount\tngram'
    for i in range(5):
        print '%d.\t%d: \t"%s"'%(i+1,top[i][0],' '.join(top[i][1]))

for n in range(1,6):
    # Put your logic for generating the sorted n-gram RDD here and store it in freq_ngramRDD variable
    freq_ngramRDD = formatted_sentences.flatMap(lambda x:zip(*[x[i:] for i in range(n)]))\
                                       .map(lambda word:(word,1))\
                                       .reduceByKey(lambda x,y:x+y)\
                                       .map(lambda x:(x[1],x[0]))\
                                       .sortByKey(False)
 
    printOutput(n,freq_ngramRDD)
