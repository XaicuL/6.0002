numCasesPerYear = 36000
numYears = 3
stateSize = 10000
communitySize = 10
numCommunities = stateSize // communitySize
numTrials = 100
numGreater = 0

for t in range(numTrials):
    locs = [0] * numCommunities
    for i in range(numYears * numCasesPerYear):
        locs[random.choice(range(numCommunities))] += 1
    if locs[111] >= 143:
        numGreater += 1

prob = round(numGreater / numTrials, 4)
print('Est. probability of region 111 having\nat least 143 cases =', prob)

anyRegion = 0
for trial in range(numTrials):
    locs = [0] * numCommunities
    for i in range(numYears * numCasesPerYear):
        locs[random.choice(range(numCommunities))] += 1
    if max(locs) >= 143:
        anyRegion += 1

print(anyRegion)
aProb = round(anyRegion / numTrials, 4)
print('Est. probability of some region having\nat least 143 cases =', aProb)