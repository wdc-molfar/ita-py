# NER-Annotation-Tool
NN based tool for data labeling of ukrainian texts for resolving NER task

### Examples of training scripts launch:
```
python model_training.py --model_name NER_UA --data_string "{\"У Львові розшукали зниклу школярку із Києва\": {\"entities\": [[2, 8, \"LOC\"]]}, \"14-річна мешканка Рудок Віолетта Єрмілова, яка зникла 10 грудня, була оголошена у національний розшук.\": {\"entities\": [[24, 41, \"PERS\"], [18, 23, \"LOC\"]]}}"
```
or
```
python model_training.py --model_name NER_UA --data_json train_data.json
```

#### Output should be like:
```
Train sample: 
	У Львові розшукали зниклу школярку із Києва
Entities:
	Львові, type = LOC

Train sample: 
	14-річна мешканка Рудок Віолетта Єрмілова, яка зникла 10 грудня, була оголошена у національний розшук.
Entities:
	Віолетта Єрмілова, type = PERS
	Рудок, type = LOC

Model NER_UA created

Iteration number:    0, loss = 21.5999972820
Iteration number:    1, loss = 21.1185176373
Iteration number:    2, loss = 20.2205410004
Iteration number:    3, loss = 18.8637704849
Iteration number:    4, loss = 16.4918403625
Iteration number:    5, loss = 13.9438774586
Iteration number:    6, loss = 9.8551077843
Iteration number:    7, loss = 6.6367459297
Iteration number:    8, loss = 4.8364996612
Iteration number:    9, loss = 4.5791020095
Iteration number:   10, loss = 4.8024854185
Iteration number:   11, loss = 4.7205195627
Iteration number:   12, loss = 4.9006442177
Iteration number:   13, loss = 4.1077750155
Iteration number:   14, loss = 3.2992876860
Iteration number:   15, loss = 2.6126790247
Iteration number:   16, loss = 1.9446569378
Iteration number:   17, loss = 6.3731961697
Iteration number:   18, loss = 3.1941776201
Iteration number:   19, loss = 3.4279961262
Iteration number:   20, loss = 2.9323397995
Iteration number:   21, loss = 2.8161391181
Iteration number:   22, loss = 2.9287119741
Iteration number:   23, loss = 2.4261903624
Iteration number:   24, loss = 1.4259722400
Iteration number:   25, loss = 1.1705083202
Iteration number:   26, loss = 1.1216225238
Iteration number:   27, loss = 2.3020652494
Iteration number:   28, loss = 1.7874184919
Iteration number:   29, loss = 0.9552937168
Iteration number:   30, loss = 1.3786115739
Iteration number:   31, loss = 1.4386676249
Iteration number:   32, loss = 0.9713124277
Iteration number:   33, loss = 0.6563476904
Iteration number:   34, loss = 0.4957005480
Iteration number:   35, loss = 0.2736193652
Iteration number:   36, loss = 0.2334939833
Iteration number:   37, loss = 0.0588329191
Iteration number:   38, loss = 0.0435542848
Iteration number:   39, loss = 0.0059659734
Iteration number:   40, loss = 0.0015818090
Iteration number:   41, loss = 0.0070119408
Iteration number:   42, loss = 0.0000748051
Iteration number:   43, loss = 0.0034642793
Iteration number:   44, loss = 0.0000357370
Iteration number:   45, loss = 0.0005713936
Iteration number:   46, loss = 0.0008861053
Iteration number:   47, loss = 0.0008187483
Iteration number:   48, loss = 0.0000530142
Iteration number:   49, loss = 0.0000006418

Model Saved
```

### Examples of prediction scripts launch:
```
python model_prediction.py --model_name NER_UA --data_string "13 жовтня у Львові у Києві"
```
or
```
python model_prediction.py --model_name NER_UA --data_file test_data.txt
```
#### Output should be like:
```
Model NER_UA loaded

Input text:
13 жовтня у Львові у Києві
Tokens [('13', ''), ('жовтня', ''), ('у', ''), ('Львові', 'LOC'), ('у', ''), ('Києві', '')]
Entities [('Львові', 'LOC')]
```
### Examples of evaluation scripts launch:
```
python model_evaluation.py --model_name NER_UA --data_string "{\"У Львові розшукали зниклу школярку із Києва\": {\"entities\": [[2, 8, \"LOC\"]]}, \"14-річна мешканка Рудок Віолетта Єрмілова, яка зникла 10 грудня, була оголошена у національний розшук.\": {\"entities\": [[24, 41, \"PERS\"], [18, 23, \"LOC\"]]}}"
```
or
```
python model_evaluation.py --model_name NER_UA --data_json train_data.json
```
#### Output should be like:
```
Model NER_UA loaded

{'LOC': {'p': 100.0, 'r': 100.0, 'f': 100.0}, 'PERS': {'p': 100.0, 'r': 100.0, 'f': 100.0}}
```

