#find dates that are in both john hopkins and kaggle datasets
#function that converts the date format from kaggle to johnhopkins and vise versa
def convert_date(date): 
    #johnhopkins is in format 1/22/20
    #kaggle is in format 2020-01-22

    #bool that flags which type of date the input is
    johnHopkinsFlag = False
    for letter in date:
        #date format is johnhopkins
        if letter == '/':
            johnHopkinsFlag = True
            break
        #date format is kaggle
        if letter == '-':
            break
    
    #convert from johnhopkins -> kaggle format
    if johnHopkinsFlag:
        firstSlash =  date.find('/')
        secondSlash = date.find('/', firstSlash + 1)
        month = date[0:firstSlash]
        if len(month) == 1:
            month = "0" + month
        day = date[firstSlash + 1:secondSlash]
        if len(day) == 1:
            day = "0" + day
        year = "20" + date[secondSlash + 1:]
        outputDate = year + "-" + month + "-" + day
    #convert from kaggle -> john hopkins
    else:
        firstHyphen =  date.find('-')
        secondHyphen = date.find('-', firstHyphen + 1)
        year = date[0:firstHyphen]
        year = year[2:]
        month = date[firstHyphen + 1:secondHyphen]
        if month[0] == "0":
            month = month[1]
        day = date[secondHyphen + 1:]
        if day[0] == "0":
            day = day[1]
        outputDate = month + "/" + day + "/" + year

    return outputDate

def compare_dates(date1,date2):
    if date1.__eq__(convert_date(date2)):
        return True
    return False
    
#run tests if this is the main file
if __name__ == "__main__":
    testKaggleStrings = ["2020-01-22","2021-04-08","2020-12-05","2021-10-15"]
    testJohnHopkinsStrings = ["1/22/20","4/8/21", "12/5/20", "10/15/21"]

    for testKaggleString in testKaggleStrings:
        print(testKaggleString)
        print(convert_date(testKaggleString))

    print("----------------------")

    for testJohnHopkinsString in testJohnHopkinsStrings:
        print(testJohnHopkinsString)
        print(convert_date(testJohnHopkinsString))
    
    print("----------------------")

    indexCtr = 0
    for testKaggleString in testKaggleStrings:
        print(compare_dates(testKaggleString,testJohnHopkinsStrings[indexCtr]))
        indexCtr += 1
