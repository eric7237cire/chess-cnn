Learning CNN by recognizing chess pieces


To Install

Install Miniconda (e:\miniconda3 for example)

```
e:\miniconda3\scripts\conda create -n tensorflow_gpuenv tensorflow-gpu

e:\miniconda3\scripts\activate tensorflow_gpuenv
```

```
e:\miniconda3\scripts\activate tensorflow_gpuenv

e:\Miniconda3\Scripts\conda list -e > requirements.txt

e:\Miniconda3\Scripts\conda env export > tensorflow_gpuenv.yml
```

check nvidia usage
```
C:\Program Files\NVIDIA Corporation\NVSMI\nvidia-smi.exe
```

open tensorboard
```
e:\miniconda3\scripts\activate tensorflow_gpuenv
tensorboard --logdir .\data\tb_logs
```


Links: https://github.com/Elucidation/tensorflow_chessbot
https://github.com/geaxgx/playing-card-detection

open jupyter
```
e:\miniconda3\scripts\activate tensorflow_gpuenv
jupyter notebook
```

Text links

https://stackoverflow.com/questions/23506105/extracting-text-opencv
https://github.com/LinxiFan/LiteOCR/blob/master/liteocr/ocr.py