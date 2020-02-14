import math
import sys
import re

class Min_Heap:

    def __init__(self):
        # [ [key1, value1], [key2, value2], ... ]
        self.heap = []
        self.key_massive = {}
        self.last_index = 0 # куда поставим новый элемент

    # проверка вниз
    def heapify(self, index):
        i_left = 2*index + 1
        i_right = 2*index + 2
        min = index
        if i_left < (self.last_index) and self.heap[i_left][0] < self.heap[min][0]:
            min = i_left
        if i_right < (self.last_index) and self.heap[i_right][0] < self.heap[min][0]:
            min = i_right
        if min != index:
            self.swap_nodes(index, min)
            self.heapify(min)

    # потому что замучился это писать каждый раз
    def swap_nodes(self, index1, index2):
        key1, key2 = self.heap[index1][0], self.heap[index2][0]
        # swap(self.key_massive[self.heap[i][0]], self.key_massive[self.heap[min][0]])
        temp = self.key_massive[key1]
        self.key_massive[key1] = self.key_massive[key2]
        self.key_massive[key2] = temp
        # swap(self.heap[min], self.heap[i])
        temp = self.heap[index1]
        self.heap[index1] = self.heap[index2]
        self.heap[index2] = temp

    # проверка вверх(проверка из добавления)
    def seftup(self, counter):
        while counter > 0 and self.heap[(counter - 1) // 2][0] > self.heap[counter][0]:
            self.swap_nodes(counter, (counter - 1) // 2)
            counter = (counter - 1) // 2

    # добавялем данные
    def add(self, key, value):
        if self.search(key) == -1:
            self.heap.append([key, value])
            self.key_massive[key] = self.last_index
            counter = self.last_index
            # Восстанавливаем возможное неупорядочивание
            self.seftup(counter)
            self.last_index += 1
        else:
            return -1

    # переназначение элемента
    def set(self, key, value):
        if self.search(key) != -1:
            index = self.key_massive[key]
            self.heap[index][1] = value
        else:
            return -1

    # удаляет ключ
    def delete(self, key):
        result = self.search(key)
        if result != -1:
            index, del_node = result[0], result[1]
            # если элемент удаляемый больше последнего, то идем верх
            if del_node[0] > self.heap[self.last_index - 1][0]:
                # swap del и последний
                self.swap_nodes(index, self.last_index - 1)
                self.heap.pop()
                self.key_massive.pop(key)
                self.last_index -= 1
                self.seftup(index)
                return
            # если элемент удаляемый меньше последнего - вниз
            elif del_node[0] < self.heap[self.last_index - 1][0]:
                self.swap_nodes(index, self.last_index - 1)
                self.heap.pop()
                self.key_massive.pop(key)
                self.last_index -= 1
                self.heapify(index)
                return
            # если это и есть последний элемент!
            else:
                self.heap.pop()
                self.key_massive.pop(key)
                self.last_index -= 1
                return
            return -1
        else:
            return -1

    # извлекает корень
    def extract(self):
        if self.heap[0]:
            root = self.heap[0]
            self.delete(self.heap[0][0])
            return root[0], root[1]
        else:
            return -1

    # ищет ключ:
    def search(self, key):
        if key in self.key_massive.keys():
            index = self.key_massive[key]
            return index, self.heap[index]
        else:
            return -1

    # "K V"
    def min(self):
        if self.heap[0]:
            return self.heap[0]
        else:
            return -1

    # "K V"
    def max(self):
        maxim = max(self.key_massive.keys())
        if maxim is not None:
            maxim = self.key_massive[maxim]
            return maxim, self.heap[maxim]
        else:
            return -1

    def print(self):
        if len(self.heap) == 0:
            return '_'
        height = math.floor(math.log2(self.last_index)) + 1
        nodes = [' _'] * ((1 << height) - 1)
        # к виду "[K V P]"
        for key in self.key_massive.keys():
            index = self.key_massive[key]
            nodes[index] = ' [' + str(self.heap[index][0]) + ' ' + str(self.heap[index][1]) + ' ' + str(self.heap[(index - 1) // 2][0]) + ']'
        for k in range(1, height):
            index = 1 << k
            nodes[index - 1] = '\n' + nodes[index - 1][1:]
        nodes[0] = '[' + str(self.heap[0][0]) + ' ' + str(self.heap[0][1]) + ']'
        heap_text = ''.join(nodes)
        return heap_text



def input_(input_=''):
    for line in sys.stdin:
        input_ += line + "\n"
    return input_


def process_heap(heap, input_):
    output = ''
    input_ = input_.split('\n')
    for line in input_[0:]:
        # пустая строка
        if re.match(r"^\s*$", line) is not None:
            continue
        # set
        elif re.match(r"^set\s(-?\d+)\s(.+)", line) is not None:
            try:
                line = line.split()
                if heap.set(int(line[1]), line[2]) == -1:
                    output += "error" + "\n"
            except:
                output += "error" + "\n"
                continue
        # add
        elif re.match(r"^add\s(-?\d+)\s(.+)$", line) is not None:
            try:
                line = line.split()
                if heap.add(int(line[1]), line[2]) == -1:
                    output += "error" + "\n"
            except:
                output += "error" + "\n"
                continue
        # delete
        elif re.match(r"^delete\s(-?\d+)$", line) is not None:
            try:
                line = line.split()
                result = heap.delete(int(line[1]))
                if result == -1:
                    output += "error" + "\n"
            except:
                output += "error" + "\n"
                continue
        elif re.match(r"^extract$", line) is not None:
            try:
                line = line.split()
                result = heap.extract()
                if result == -1:
                    output += "error" + "\n"
                else:
                    output += str(result[0]) + ' ' + str(result[1]) + "\n"
            except:
                output += "error" + "\n"
                continue
        # search
        elif re.match(r"^search\s(-?\d+)$", line) is not None:
            try:
                line = line.split()
                result = heap.search(int(line[1]))
                if result == -1:
                    output += '0' + "\n"
                else:
                    index, el = result[0], result[1]
                    output += '1 ' + str(index) + ' ' + str(el[1]) + "\n"
            except:
                output += "error" + "\n"
                continue
        # search Min "K V"
        elif re.match(r"^min$", line) is not None:
            try:
                el = heap.min()
                if el == -1:
                    output += "error" + "\n"
                else:
                    output += str(el[0]) + ' 0 ' + str(el[1]) + "\n"
            except:
                output += "error" + "\n"
                continue
        # search Max "K V"
        elif re.match(r"^max$", line) is not None:
            try:
                result = heap.max()
                if result == -1:
                    output += "error" + "\n"
                else:
                    index, el = result[0], result[1]
                    output += str(el[0]) + ' ' + str(index) + ' ' + str(el[1]) + "\n"
            except:
                output += "error" + "\n"
                continue
        # print
        elif re.match(r"^print$", line) is not None:
            try:
                output += str(heap.print()) + "\n"
            except:
                output += "error" + "\n"
                continue
        else:
            output += "error" + "\n"
    return output, heap


if __name__ == "__main__":
    input_ = input_()
    Heap_1 = Min_Heap()
    output, Heap_1 = process_heap(Heap_1, input_)
    print(output)
