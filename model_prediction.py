import os
import io
import sys
import json
import spacy



input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')


def main(input_json):

    output_json = input_json.copy()
    
    model_name = input_json['model']['name']
    model_lang = input_json['model']['locale']
    
                                          
    if f'{model_name}_{model_lang}' in os.listdir('.'):
        nlp = spacy.load(f'./{model_name}_{model_lang}')
    else:
        return
        
    if "ner" in nlp.pipe_names:
        ner = nlp.get_pipe("ner")
    else:
        return
                
    for i in range(len(input_json['data'])):
        text = input_json['data'][i]['text']
        entities = list()
        doc = nlp(text)                   
        
        start_index = 0
        for ent in doc.ents:                                    
            start_pos = text.index(ent.text, start_index)
            end_pos = text.index(ent.text, start_index)+len(ent.text)-1
            
            res_tmp = {}
            res_tmp['type'] = ent.label_
            res_tmp['pos'] = [start_pos, end_pos]
            entities.append(res_tmp)
            
            start_index = end_pos
        
        output_json['data'][i]['entities'] = entities
        

    return output_json



if __name__=='__main__':
    
    input_json = None
    for line in input_stream:
        input_json = json.loads(line)    
        
        output = main(input_json)
        
        output_json = json.dumps(output, ensure_ascii=False).encode('utf-8')
        sys.stdout.buffer.write(output_json)
        print()