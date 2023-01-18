import numpy
import PIL.Image

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
    #numpy.savetxt("output.txt", data, fmt='%d')
    a1 = getPercentage(a1)
    a2 = getPercentage(a2)
    a3 = getPercentage(a3)
    a4 = getPercentage(a4)
    a5 = getPercentage(a5, rows*columns)
    #print("a1={}, a2={}, a3={}, a4={}, a5={}".format(a1, a2, a3, a4, a5))
    return [a1, a2, a3, a4, a5]

def getPercentage(num, den = 120*120):
    return num/den*100

def main():
    all = element = data1 = data2 = data3 = []
    for m in range(4):
        a0 = a1 = a2 = a3 = a4 = 0
        for n in range(4):
            filename = str(m) + str(n) + ".png"
            features = getFeatures('c://wj//test//knn//training//' + filename)
            a0 = a0 + features[0]
            a1 = a1 + features[1]
            a2 = a2 + features[2]
            a3 = a3 + features[3]
            a4 = a4 + features[4]
        all.append([round(a0,2), round(a1,2), round(a2,2), round(a3,2), round(a4,2)])
    
    testdata = getFeatures('c://wj//test//knn//test//4.png')
    for m in range(numpy.shape(testdata)[0]):
        testdata[m] = round(testdata[m]*4, 2)
    test(all, testdata)

def test(all, obj):
    #print(numpy.shape(all))
    #print(all)
    #print(numpy.shape(obj))
    #print(obj)
    result = diffs = diff = []
    sum = 0
    for m in range(4):
        diff = []
        for n in range(5):
            sum = sum + all[m][n] - obj[m]
        result.append(round(sum,2))
        sum = 0

    print(result)
    type = 0
    min = 100
    for m in range(4):
        if min > abs(result[m]):
            type = m
            min = result[m]

    #print(type,  abs(min))
    print("This image is " + str(type) + ".")
main()