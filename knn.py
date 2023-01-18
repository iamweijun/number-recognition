import numpy
import PIL.Image
import copy
import os

def getFeatures(filename):
    file_zero=PIL.Image.open(filename)
    array_zero=numpy.array(file_zero)
    a1 = a2 = a3 = a4 = a5 = 0
    rows = array_zero.shape[0]
    columns = array_zero.shape[1]
    data = []
    for m in range(rows):
        tmp = [0]*columns
        for n in range(columns):
            if array_zero[m][n][0] > 240:
                tmp[n] = 0
            else:
                tmp[n] = 1
            a5 = a5 + tmp[n]
            if m < rows/2 and n < columns/2:
                a1 = a1 + tmp[n]
            elif m < rows/2 and n >= columns/2:
                a2 = a2 + tmp[n]
            elif m >= rows/2 and n < columns/2:
                a3 = a3 + tmp[n]
            else:
                a4 = a4 + tmp[n]
        data.append(tmp)

    a1 = getPercentage(a1)
    a2 = getPercentage(a2)
    a3 = getPercentage(a3)
    a4 = getPercentage(a4)
    a5 = getPercentage(a5, rows*columns)
    #print("a1={}, a2={}, a3={}, a4={}, a5={}".format(a1, a2, a3, a4, a5))
    return [a1, a2, a3, a4, a5]

def getPercentage(num, den = 120*120):
    return round(num/den*100,4)

def main():
    all = []
    path = os.path.abspath('.')
    for m in range(4):
        for n in range(4):
            filename = str(m) + str(n) + ".png"
            features = getFeatures(path + '\\training\\' + filename)
            all.append(features)
    
    for m in range(4):
        allcopy = copy.deepcopy(all)
        filename = path + '\\test\\' + str(m) + '.png'
        testdata = getFeatures(filename)
        test(allcopy, testdata, filename)

def test(all, obj, filename):
    """print(numpy.shape(all))
    print(all)
    print(numpy.shape(obj))
    print(obj)"""
    results = []
    res = mysort(all, obj, 0)
    results.append(res)
    res = mysort(all, obj, 1)
    results.append(res)
    res = mysort(all, obj, 2)
    results.append(res)
    res = mysort(all, obj, 3)
    results.append(res)
    res = mysort(all, obj, 4)
    results.append(res)

    print(results)
    score = myscore(results)
    print(score)
    max = sorted(score, reverse = True)[0]
    sum = score[0] + score[1] + score[2] + score[3]
    p0 = round(score[0]/sum*100, 2)
    p1 = round(score[1]/sum*100, 2)
    p2 = round(score[2]/sum*100, 2)
    p3 = round(score[3]/sum*100, 2)
    log = getLog([p0, p1, p2, p3])
    if score[0] == max:
        print(filename + " is 0" + log)
    elif score[1] == max:
        print(filename + " is 1" + log)
    elif score[2] == max:
        print(filename + " is 2" + log)
    else:
        print(filename + " is 3" + log)

def mysort(all, obj, position):
    value = 0
    result = []
    for i in range(4):
        type = -1
        min = 100
        for m in range(16):
            if min > abs(all[m][position] - obj[position]):
                type = m
                value = all[m][position]
                min = abs(all[m][position] - obj[position])
        all[type][position] = all[type][position] * 100
        result.append(type)
        #print(type, value, min)

    return result
def getLog(data):
    p0 = ", P0 = " + str(data[0]) + "%"
    p1 = ", P1 = " + str(data[1]) + "%"
    p2 = ", P2 = " + str(data[2]) + "%"
    p3 = ", P3 = " + str(data[3]) + "%"
    return p0 + p1 + p2 + p3

def myscore(data):
    result = []
    step = 1
    zero = one = two = three = 0
    for m in range(5):
        for n in range(3):
            if n == 0:
                step = 2
            elif n == 1:
                step = 1.5
            else:
                step = 1
            if data[m][n] < 4:
                zero += step
            elif data[m][n] >= 4 and data[m][n] < 8:
                one += step
            elif data[m][n] >= 8 and data[m][n] < 12:
                two += step
            else:
                three += step
    result.append(zero)
    result.append(one)
    result.append(two)
    result.append(three)
    return result

main()