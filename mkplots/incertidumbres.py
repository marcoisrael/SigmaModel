#!/usr/bin/python3

def fix(x, dx):
    before, after = str(dx).split(".")
    i = 0
    val = 0
    for d in after:
        i += 1
        if d != "0":
            val = round(float(d + "." + after[i:]))
            break
    y = round(x, i)
    if i > len(str(y).split(".")[1]):
        y = f"{y}{'0'*(i-len(str(y).split('.')[1]))}"
    return f"{y}({val})"
    
class measure:
  def __init__(self, x, dx):
    self.value = x
    self.error = dx
  def print(self):
    print(fix(self.value,self.error))
  def __add__(self, y):
    return measure(self.value+y.value, self.error+y.error)
  def __sub__(self, y):
    return measure(self.value-y.value, self.error+y.error)
  def __mul__(self, y):
    return measure(self.value*y.value, self.value*y.error+y.value*self.error)
  def __truediv__(self,y):
    return measure(self.value/y.value, (self.value*y.error+y.value*self.error)/y.value**2)


  
  