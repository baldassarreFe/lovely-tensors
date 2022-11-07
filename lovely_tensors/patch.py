# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/10_patch.ipynb.

# %% auto 0
__all__ = ['monkey_patch']

# %% ../nbs/10_patch.ipynb 3
import torch
from fastcore.foundation import patch_to
import matplotlib.pyplot as plt

from .repr_str import StrProxy
from .repr_rgb import RGBProxy
from .repr_plt import PlotProxy
from .repr_chans import ChanProxy

# %% ../nbs/10_patch.ipynb 4
def monkey_patch(cls=torch.Tensor):
    "Monkey-patch lovely features into `cls`" 

    @patch_to(cls)
    def __repr__(self: torch.Tensor, *, tensor_contents=None):        
        return str(StrProxy(self))

    # Plain - the old behavior
    @patch_to(cls, as_prop=True)
    def p(self: torch.Tensor, *, tensor_contents=None):
        return StrProxy(self, plain=True)

    # Verbose - print both stats and plain values
    @patch_to(cls, as_prop=True)
    def v(self: torch.Tensor, *, tensor_contents=None):
        return StrProxy(self, verbose=True)

    @patch_to(cls, as_prop=True)
    def deeper(self: torch.Tensor):
        return StrProxy(self, depth=1)

    @patch_to(cls, as_prop=True)
    def rgb(t: torch.Tensor):
        return RGBProxy(t)
    
    @patch_to(cls, as_prop=True)
    def chans(t: torch.Tensor):
        return ChanProxy(t)

    @patch_to(cls, as_prop=True)
    def plt(t: torch.Tensor):
        return PlotProxy(t)
