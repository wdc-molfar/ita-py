import json
import os
import io
import sys
import spacy
import random
from spacy.util import minibatch, compounding
import warnings



warnings.filterwarnings("ignore", message=r"\[W033\]", category=UserWarning)

input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')


def main(input_json):

    output_json = input_json.copy()
        
    model_name = input_json['model']['name']
    model_lang = input_json['model']['locale']
                          
        
    if f'{model_name}_{model_lang}' in os.listdir('.'):
        nlp = spacy.load(f'./{model_name}_{model_lang}')
    else:
        nlp = spacy.blank(model_lang)
    
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    else:
        ner = nlp.get_pipe("ner") 
    
    
    [[ner.add_label(x['type']) for x in input_json['data'][i]['entities']] for i in range(len(input_json['data']))]
    
    
    n_iter = 50
    
    pipe_exceptions = ["ner", "trf_wordpiecer", "trf_tok2vec"]
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe not in pipe_exceptions]
    train_data = [[input_json['data'][i]['text'], {'entities': [[x['pos'][0], x['pos'][1]+1, x['type']] for x in input_json['data'][i]['entities']]}] for i in range(len(input_json['data']))]
        

    optimizer = nlp.begin_training() if f'{model_name}_{model_lang}' not in os.listdir('.') else nlp.resume_training()
    list_losses = list()  
    with nlp.disable_pipes(*other_pipes):        

        for itn in range(n_iter):

            random.shuffle(train_data)
            losses = {}

            batches = minibatch(train_data, size=compounding(10.0, 32.0, 1.2))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,
                    annotations,  
                    drop=0.2,  
                    losses=losses,
                    sgd=optimizer
                )
            list_losses.append(losses['ner'])
    
    nlp.to_disk(f"./{model_name}_{model_lang}")
    
    output_json['model']['losses'] = list_losses
    
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
        except Exception as e:
            print(e)
            output = input_json.copy()
            
        
        output_json = json.dumps(output, ensure_ascii=False).encode('utf-8')
        sys.stdout.buffer.write(output_json)
        print()
        