import secrets

diceRoller = lambda D: secrets.randbelow(D) + 1 
oneDFour = lambda: diceRoller(4)
oneDSix = lambda: diceRoller(6)

class Horse:
    def __init__(self, name, innatePower, nutrition, training, jockey):
        self.name = name
        self.innatePower = innatePower
        self.nutrition = nutrition
        self.training = training
        self.jockey = jockey
        
    def getPowerForRace(self):
        return self.innatePower + self.nutrition + self.training + self.jockey

def loadHorseNames():
    with open("./horseNames.txt") as horseNameFile:
        lines = horseNameFile.readlines()
        horseNames = [line.strip() for line in lines]
        return horseNames

def _horseNameGenerator():
    names = loadHorseNames()
    previousNames = set()
    while True:
        name = secrets.choice(names)
        if name in previousNames:
            iterator = 1
            iteratorName = f"{name} {iterator}"
            while iteratorName in previousNames:
                iterator += 1
            previousNames.add(iteratorName)
            yield iteratorName
        else:
            yield name

horseNameGenerator = _horseNameGenerator()

def generateHorseName():
    return next(horseNameGenerator)

def generateHorsePower():
    threeDFour = [oneDFour() for _ in range(3)]
    threeDFour.sort()
    return sum(threeDFour[1:])

def generateHorse():
    name = generateHorseName()
    innatePower = generateHorsePower()
    nutrition = oneDFour()
    training = oneDFour()
    jockey = oneDFour()
    return Horse(name, innatePower, nutrition, training, jockey)

def generateHorsesForRace():
    return [generateHorse() for _ in range(8)]

def runRace(horses):
    raceResult = [(horse, horse.getPowerForRace() + oneDSix()) for horse in horses]
    raceResult.sort(key = lambda horseResultTuple: horseResultTuple[1])
    raceWinnerPower = raceResult[-1][1]
    return secrets.choice([horse for (horse, result) in raceResult if result == raceWinnerPower])

iterationsNumber = 10000
housePayoutStake = 0.95
houseKnows = lambda: oneDFour() > 2

def simulateRace(horses, gnosticismFunction):
    simulatedRacesWinners = {horse.name: 0 for horse in horses}
    for _ in range(iterationsNumber):
        knownHorsePowers = []
        for horse in horses:
            #House doesn't know details about the horses exactly
            #Assumed 50% chance they know the exact details on any given topic
            #Otherwise they guess (i.e. random)
            innatePower = horse.innatePower if gnosticismFunction() else generateHorsePower()
            nutrition = horse.nutrition if gnosticismFunction() else oneDFour()
            training = horse.training if gnosticismFunction() else oneDFour()
            jockey = horse.jockey if gnosticismFunction() else oneDFour()
            knownHorsePowers.append(Horse(horse.name, innatePower, nutrition, training, jockey))
        predictedWinner = runRace(knownHorsePowers)
        simulatedRacesWinners[predictedWinner.name] += 1
    return {K: V/iterationsNumber for K, V in simulatedRacesWinners.items()}
    
def calculateHouseBettingOdds(probabilityDict):
    return {K: int(1/V) for K, V in probabilityDict.items()}

def printBettingTable(horses, bettingOdds, houseProbabilites, trueProbabilities):
    print("HORSE BETTING TABLE")
    print(f"{'Name':<15}| Power | Nutr | Train | Jock | Sabotage? | Total | Odds")
    for horse in horses:
        print(f"{horse.name:<15}|{horse.innatePower:^7}|{horse.nutrition:^6}|{horse.training:^7}|{horse.jockey:^6}|{'No':^11}|{horse.getPowerForRace():^7}| {bettingOdds[horse.name]:^6.01f}|{houseProbabilites[horse.name]:^6.02f}|{trueProbabilities[horse.name]:^6.02f}|")
    print("\n")
    print(f"{'Total':<15}|{'':<57}|{sum(houseProbabilites.values()):^6}|{sum(trueProbabilities.values()):^6}|")
    print("\n\n")
    print("------ PLAYER BETTING TABLE HERE --------")
    print(f"{'Name':<15}| Odds")
    for horse in horses:
        print(f"{horse.name:<15}| {bettingOdds[horse.name]:.01f}")

def runTheThing():
    horses = generateHorsesForRace()
    houseSimulationProbabilities = simulateRace(horses, houseKnows)
    bettingOdds = calculateHouseBettingOdds(houseSimulationProbabilities)
    trueProbabilities = simulateRace(horses, lambda: True)
    printBettingTable(horses, bettingOdds, houseSimulationProbabilities, trueProbabilities)

runTheThing()