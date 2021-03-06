import argparse
import os
import io
import sys
import json
import spacy
from spacy.gold import GoldParse
from spacy.scorer import Scorer
import warnings
import traceback



input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')


def main(input_json):

    output_json = input_json.copy()
        
    model_name = input_json['model']['name']
    model_lang = input_json['model']['locale']       
    workDir = input_json['workDir']
    
    nlp = spacy.load(f'./{workDir}/{model_name}_{model_lang}')    
            
    ner = nlp.get_pipe("ner")
    
          
            
    data = [[input_json['data'][i]['text'], {'entities': [[x['pos'][0], x['pos'][1]+1, x['type']] for x in input_json['data'][i]['entities']]}] for i in range(len(input_json['data']))]
    
    scorer = Scorer()
    for input_, annot in data:
        doc_gold_text = nlp.make_doc(input_)
        gold = GoldParse(doc_gold_text, entities=annot['entities'])
        pred_value = nlp(input_)
        scorer.score(pred_value, gold)
       
    output_json['model']['metrics'] = scorer.scores['ents_per_type']
    
    return output_json
    
    
    
if __name__=='__main__':
    
    input_json = None
    for line in input_stream:
        
        # read json from stdin
        input_json = json.loads(line)
        
        # read file path with json - for debugging
#         with open(line[:-1], 'r', encoding='utf-8') as f:
#             input_json = json.loads(f.read())
        
        try:
            output = main(input_json)
        except BaseException as ex:            
            ex_type, ex_value, ex_traceback = sys.exc_info()            
            
            output = {"error": ''}           
            output['error'] += "Exception type : %s; \n" % ex_type.__name__
            output['error'] += "Exception message : %s\n" %ex_value
            output['error'] += "Exception traceback : %s\n" %"".join(traceback.TracebackException.from_exception(ex).format())
            
            
        output_json = json.dumps(output, ensure_ascii=False).encode('utf-8')
        sys.stdout.buffer.write(output_json)
        print()
        