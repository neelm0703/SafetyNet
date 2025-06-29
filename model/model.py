import torch
import torch.nn as nn

class DiseasePredictor(nn.Module):
  def __init__(self, input_size=377, output_size=754):
    super().__init__()

    self.layers = nn.Sequential(
        nn.Linear(input_size, 512),
        nn.LeakyReLU(0.001),
        nn.BatchNorm1d(512),
        nn.Dropout(0.3),

        nn.Linear(512, 1024),
        nn.LeakyReLU(0.001),
        nn.BatchNorm1d(1024),
        nn.Dropout(0.3),

        nn.Linear(1024, 512),
        nn.LeakyReLU(0.01),
        nn.BatchNorm1d(512),
        nn.Dropout(0.3),

        nn.Linear(512, output_size)
    )

  def forward(self, X):
    return self.layers(X)