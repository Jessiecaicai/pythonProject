from __future__ import print_function
import torch
# x=torch.tensor([5.5,3])
# x = x.new_ones(5,3,dtype=torch.double)
# print(x)
# x=torch.randn_like(x,dtype=torch.float)
# print(x)
# print(x.size())
# print(x[: , 1])
# x = torch.rand(1)
# print(x)
# print(x.item())
x = torch.ones(2,2,requires_grad=True)
print(x)