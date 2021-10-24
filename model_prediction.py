import os
import io
import sys
import json
import spacy
from collections import defaultdict


input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')


def main(input_json):

    output_json = input_json.copy()

    model_name = input_json['model']['name']
    model_lang = input_json['model']['locale']


    if f'{model_name}_{model_lang}' in os.listdir('.'):
        nlp = spacy.load(f'./{model_name}_{model_lang}')

    if "ner" in nlp.pipe_names:
        ner = nlp.get_pipe("ner")


    for i in range(len(input_json['data'])):
        text = input_json['data'][i]['text']
        entities = list()
        doc = nlp(text)

        beams = nlp.entity.beam_parse([ doc ], beam_width = 16, beam_density = 0.0001)
        entity_scores = defaultdict(float)
        for beam in beams:
            for score, ents in nlp.entity.moves.get_beam_parses(beam):
                for start, end, label in ents:
                    entity_scores[(str(doc[start:end]), label)] += score

        start_index = 0
        for ent in doc.ents:
            start_pos = text.index(ent.text, start_index)
            end_pos = text.index(ent.text, start_index)+len(ent.text)-1

            res_tmp = {}
            res_tmp['type'] = ent.label_
            res_tmp['pos'] = [start_pos, end_pos]
            res_tmp['score'] = round(entity_scores[(ent.text, ent.label_)], 5)
            entities.append(res_tmp)

            start_index = end_pos

        output_json['data'][i]['entities'] = entities
        

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