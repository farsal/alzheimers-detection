# -*- coding: utf-8 -*-
"""Alzheimers_Pred.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1M9TrktFEwnH5BZgmEFVzjhncLqqtUzeo
"""

import warnings
warnings.filterwarnings('ignore')

"""# Alzherimers Detection using MRI Scans"""

from google.colab import drive
drive.mount('/content/drive')

!tar -xf "/content/drive/My Drive/AlzModel/dataset.tar.xz"

PATH = 'dataset/'

from fastai import *
from fastai.vision import *
from fastai.metrics import accuracy

tfms = get_transforms()
data = ImageDataBunch.from_folder(PATH, valid='validation', ds_tfms=tfms, bs=64, num_workers=4).normalize(imagenet_stats)

data.classes

model = cnn_learner(data, models.densenet201, metrics=accuracy, pretrained=True)

model.fit_one_cycle(5)

model.save('alzheimersv1-initial')
model.unfreeze()

model.lr_find()
model.recorder.plot(suggestion=True)

model.fit_one_cycle(25, max_lr=6.31e-07)

interp = ClassificationInterpretation.from_learner(model)
interp.plot_confusion_matrix()

interp.plot_top_losses(4, figsize=(8,8))

model.save('alzheimers')
model.export('/content/drive/My Drive/AlzModel/alzDensenet201.pt')

DRIVE_PATH = '/content/drive/My Drive/AlzModel/'

predictor = load_learner(DRIVE_PATH,'alzDensenet201.pt')

img = open_image(DRIVE_PATH+'YAL0001.jpg')
img

pred = predictor.predict(img)
pred[0]