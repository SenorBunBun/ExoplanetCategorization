import pymongo as mg

client = mg.MongoClient("mongodb+srv://guest:apcompscipass@projects.vur1u.mongodb.net/CompSciExoplanets?retryWrites=true&w=majority")
database = client["CompSciExoplanets"]
collection = database["CompSciExoplanets1"]
listofexoplanets = []

def collectInputs():
    global listofexoplanets
    name = input("Please enter the name of your exoplanet : ")
    listofexoplanets.append(name)
    location = input("Where is {0} located? Is it orbiting a sun or other object? [Type 'sun' or another location] : ".format(name))
    radius = int(input("What is {0}'s radius [measured in Earth radii and entered using numerals] : ".format(name)))
    period = int(input("What is {0}'s orbital period? [Measured in days] : ".format(name)))
    temp = int(input("What is {0}'s surface temperature? [Measured in kelvin] : ".format(name)))
    return [name, location, radius, period, temp]

def determineType(name, location, radius, period, temp):
    tempexoplanet = {"Name": name, "Sizetype": None, "Sizemodifer": None, "Periodtype": None, "Rouge" : None, }
    if location == "sun":
        tempexoplanet["Rouge"] = "NO"
    else:
        tempexoplanet["Rouge"] = "YES"
    if period < 10:
        tempexoplanet["Periodtype"] = "Hot"
    elif (period/360) ** (2/3) > 2.7 and temp < 170:
        tempexoplanet["Periodtype"] = "Cold"
    else:
        tempexoplanet["Periodtype"] = "Regular"
    if radius <= 2:
        tempexoplanet["Sizetype"] = "Earth"
        if radius < 0.8:
            tempexoplanet["Sizemodifer"] = "Mini"
        elif radius < 1.2:
            tempexoplanet["Sizemodifer"] = "Regular"
        elif radius <= 2:
            tempexoplanet["Sizemodifer"] = "Super"
    elif radius <= 7:
        tempexoplanet["Sizetype"] = "Neptune"
        if radius < 3.6:
            tempexoplanet["Sizemodifer"] = "Mini"
        elif radius < 4.1:
            tempexoplanet["Sizemodifer"] = "Regular"
        elif radius <= 7:
            tempexoplanet["Sizemodifer"] = "Super"
    elif radius > 7:
        tempexoplanet["Sizetype"] = "Jupiter"
        if radius < 15.4:
            tempexoplanet["Sizemodifer"] = "Regular"
        else:
            tempexoplanet["Sizemodifer"] = "Super"
    wording = {"Neptune" : "Neptunian", "Earth": "Earth", "Jupiter" : " Jupiter"}
    if tempexoplanet["Sizetype"] == tempexoplanet["Periodtype"]:
        print("{0} is a {1} {2} exoplanet.".format(name, tempexoplanet["Sizemodifer"], wording[tempexoplanet["Sizetype"]]))
    else:
        print("{0} is a {1} {2} {3} exoplanet.".format(name, tempexoplanet["Sizemodifer"], tempexoplanet["Periodtype"], wording[tempexoplanet["Sizetype"]]))
    if tempexoplanet["Rouge"] == "YES":
        print("{0} is a rouge planet orbiting around a {1}".format(name, location))
    else:
        print("{0} is not a rouge planet located, this means {0} orbits a sun(s)".format(name, location))
    print("Here are the exoplanets you added this session:")
    for name in listofexoplanets:
        print(name)
    return tempexoplanet


print("Welcome to Arsh's exoplanet classifier. By entering your exoplanet's name and other data it will automatically identify it's exoplanet's type")
while True:
    userinputs = collectInputs()
    userexoplanet = determineType(userinputs[0], userinputs[1], userinputs[2], userinputs[3], userinputs[4])
    collection.insert_one(userexoplanet)

    if input("Do you want to enter another exoplanet [Y/N]") == "Y":
        pass
    else:
        break

print("Thank you for entering all this data. This data is continously added and is not removed when you exit the program")
print("Here are the names of each exoplanet in the database so far")
for all in collection.find({}, {"_id": 0}) :
    print(all)


