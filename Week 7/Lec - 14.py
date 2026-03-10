def __init__(self, pClass , age, gender , survived, name):
    self.name == name
    if pClass == 2:
        self.featureVec = [1,0,age,gender]
    elif pClass == 3:
        self.featureVec = [0,1,age,gender]
    else:
        self.featureVec = [0,0,age,gender]

    self.label = survived
    self.cabinClass = pClass

### ROC ###

def buildROC(trainingSet, testSet, title, plot = True):
    model = buildModel(trainingSet, True)
    xVals, yVals = [], []
    p = 0.0
    while p <= 1.0:
        truePos, falsePos, trueNeg, falseNeg =\
            applyModel(model, testSet, 'Survived', p)
        xVals.append(1.0 - specificity(trueNeg, falsePos))
        yVals.append(sensitivity(truePos, falseNeg))
        p += 0.01
    auroc = sklearn.metrics.auc(xVals, yVals, True)
    if plot:
        # 시각화 코드 생략 (...)
        pass
    return auroc
