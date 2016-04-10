# define color dictionary used for R
colsDic = {1:"red", 2:"orange", 3:"blue", 4:"forestgreen", 5: "gold", 6: "slateblue", 7: "brown", 8: "sienna", 9: "cyan", 10:"olivedrab"}

def getCategoryColorDic (category, colsDic):
    groupColorDic ={}
    for i in range(len(category)):
        groupColorDic[category[i]] = colsDic[i+1]
    print(groupColorDic)
    return groupColorDic

def getMemberColor (group, groupColorDic):
    col = [groupColorDic[x] for x in group]
    print(col[0:3])
    return col