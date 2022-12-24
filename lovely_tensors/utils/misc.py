# AUTOGENERATED! DO NOT EDIT! File to edit: ../../nbs/03b_utils.misc.ipynb.

# %% auto 0
__all__ = ['to_numpy']

# %% ../../nbs/03b_utils.misc.ipynb 5
import numpy as np
import torch

# %% ../../nbs/03b_utils.misc.ipynb 6
def to_numpy(t: torch.Tensor) -> np.ndarray:
    t = t.detach().cpu()
    if t.dtype is torch.bfloat16: t = t.to(torch.float32)
    return t.numpy()
