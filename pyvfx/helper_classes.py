
# altered list class that has an upper limit on
# amount of data 
class LimitedList(list):
    limit = 0
    def __init__(self, iterable: list, limit: int):
        super().__init__([item for item in iterable])
        self.limit = limit
    def __setitem__(self, index, item):
        super().__setitem__(index, item)
    def insert(self, index, item):
        super().insert(index, item)
    def append(self, item):
        super().append(item)
        if (super().__len__() > self.limit):
            super().pop(0)
    def extend(self, other):
        if isinstance(other, type(self)):
            super().extend(other)
        else:
            super().extend([item for item in other])
    
# implementation of Juce smoothed value class
# used for when we want values to not jump around too much
class AveragedValue():
    target_value = 0
    def __init__(self, length):
        self.buffer = LimitedList([], length)
    def get_avg(self):
        if len(self.buffer) == 0:
            return 0
        return sum(self.buffer) / len(self.buffer)
    def append(self, data):
        if isinstance(data, int) or isinstance(data, float):
            self.buffer.append(data)
            return self.get_avg()
        else:
            raise RuntimeError("add only int or float as value")
    def __repr__(self):
        return str(self.get_avg())

class SmoothedValue():
    ramp_length = 0
    current_ramp_step = 0
    current_step_size = 0
    current_value = 0
    def __init__(self, length: int, current_value):
        self.ramp_length = length
        self.current_value = current_value
    def set_target(self, target):
        self.target_value = target
        self.current_ramp_step = 0
    def get_target(self):
        return self.target_value
    def get_next(self):
        try:
            test = self.target_value
        except:
            raise RuntimeError("must first set target value")
        if self.current_ramp_step == 0:
            self.current_step_size = (self.target_value - self.current_value)/self.ramp_length
            self.current_ramp_step += 1
            self.current_value += self.current_step_size
            return self.current_value
        elif self.current_ramp_step == self.ramp_length:
            return self.current_value
        else:
            self.current_ramp_step += 1
            self.current_value += self.current_step_size
            return self.current_value
    def __repr__(self):
        return str(self.current_value)
