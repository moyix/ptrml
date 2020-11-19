This is a silly litltle example of using a DNN to recognize pointers.
Training and validation data are collected using the `mm_train.py` and
`mm_valid.py` scripts, which use
[PyPanda](https://github.com/panda-re/panda/tree/master/panda/python) to
collect examples of pointers and non-pointers.

The script `nn.py` uses Tensorflow to train a neural network and then
validate its accuracy. To train:

```
python nn.py train
```

To validate:

```
python nn.py valid
```

Sample training and validation data are included in the files
`train_neg.txt.gz`, `train_pos.txt.gz`, `valid_neg.txt.gz`, and
`valid_pos.txt.gz`.

Depending on how much GPU memory you have, you may need to adjust the
`BATCH_SIZE` parameter in `nn.py`.
