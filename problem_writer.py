from ai_planner import *


class problem_writer():

    initEnvironment = "(:init "
    initDistribution = "(:init "
    objectsEnvironment = "(:objects o - outside "
    objectsDistribution = "(:objects "
    goalDistribution = "(:goal (and "

    def finishObjects(self):
        self.objectsEnvironment += (")")
        self.objectsDistribution += (")")

    def finishInit(self):
        self.initEnvironment += (") ")
        self.initDistribution += (") ")

    def finishGoal(self):
        self.goalDistribution += ")) "


    def setTables(self, count):
        for i in range(1,count+1):
            self.objectsEnvironment += ("t" + str(i) + " ")
        self.objectsEnvironment += ("- table ")

    def setRooms(self, count):
        for i in range(1,int(count)+1):
            self.objectsEnvironment += ("r" + str(i) + " ")
            self.objectsDistribution += ("r" + str(i) + " ")
        self.objectsEnvironment += ("- room ")
        self.objectsDistribution += ("- room ")

    def setPersons(self, count):
        for i in range(1,int(count)+1):
            self.objectsDistribution += ("p" + str(i) + " ")
            self.goalDistribution += ("(not(new-person p" +str(i) + ")) ")
        self.objectsDistribution += ("- person ")

    def setChairs(self, count):
        for i in range(1,count+1):
            self.objectsDistribution += ("c" + str(i) + " ")
        self.objectsDistribution += ("- chair ")

    def setTemp(self, temp, room):
        if(temp == "low"):
            self.initEnvironment += ("(lowTemp r" + str(room) + ") ")
        elif(temp == "mid"):
            self.initEnvironment += ("(midTemp r" + str(room) + ") ")
        elif (temp == "high"):
            self.initEnvironment += ("(highTemp r" + str(room) + ") ")

    def setHum(self, hum, room):
        if(hum == "low"):
            self.initEnvironment += ("(lowHum r" + str(room) + ") ")
        elif(hum == "mid"):
            self.initEnvironment += ("(midHum r" + str(room) + ") ")
        elif (hum == "high"):
            self.initEnvironment += ("(highHum r" + str(room) + ") ")

    def setOutsideHum(self, hum, room):
        if(hum == "lower"):
            self.initEnvironment += ("(lowerOutsideHum r" + str(room) + ") ")
        elif(hum == "higher"):
            self.initEnvironment += ("(higherOutsideHum r" + str(room) + ") ")

    def setOutsideTemp(self, temp, room):
        if(temp == "lower"):
            self.initEnvironment += ("(lowerOutsideTemp r" + str(room) + ") ")
        elif(temp == "higher"):
            self.initEnvironment += ("(higherOutsideTemp r" + str(room) + ") ")

    def setHighCO2(self, room):
        self.initEnvironment += ("(highCO2 r" + str(room) + ") ")

    def setBadWeather(self):
        self.initEnvironment += ("(badWeather o) ")

    def setLowLight(self, room):
        self.initEnvironment += ("(lowLight r" + str(room) + ") ")

    def setLowLightOutside(self):
        self.initEnvironment += ("(lowlightOutside o) ")

    def setLoudSound(self, table):
        self.initEnvironment += ("(loudSound t" + str(table) + ") ")

    def setPresence(self, room):
        self.initEnvironment += ("(presenceInRoom r" + str(room) + ") ")

    def setWindowOpen(self,room):
        self.initEnvironment += ("(windowOpen r" + str(room) + ") ")

    def setClimateOn(self,room):
        self.initEnvironment += ("(climateOn r" + str(room) + ") ")

    def setLightOn(self,room):
        self.initEnvironment += ("(lightOn r" + str(room) + ") ")



    def setNewPerson(self,person):
        self.initDistribution += ("(new-person p" + str(person) + ") ")

    def setFreeChair(self,chair, room):
        self.initDistribution += ("(free-chair c" + str(chair) + " r" + str(room) + ") ")

    def setOnePersonMoreInRoom(self,room):
        self.initDistribution += ("(one-more-person-in-room r" + str(room) + ") ")

    def setTwoPersonMoreInRoom(self, room):
        self.initDistribution += ("(two-more-person-in-room r" + str(room) + ") ")

    def setThreePersonMoreInRoom(self, room):
        self.initDistribution += ("(three-more-person-in-room r" + str(room) + ") ")


if __name__ == '__main__':
    """
     Main here is used for  testing the problem_writer component
    """
    writer = problem_writer()
    writer.setTemp("high", 1)
    writer.setHum("mid", 1)
    writer.setPresence(1)
    writer.setLowLight(1)
    writer.setOutsideTemp("lower",1)
    writer.setTemp("high", 2)
    writer.setHum("mid", 2)
    writer.setPresence(2)
    writer.setLowLight(2)
    writer.setOutsideTemp("lower", 2)
    writer.setTemp("high", 3)
    writer.setHum("mid", 3)
    writer.setPresence(3)
    writer.setLowLight(3)
    writer.setOutsideTemp("lower", 3)

    writer.setRooms(3)
    writer.setOutside()

    writer.finishInit()
    writer.finishObjects()
    print(writer.initEnvironment)
    print(writer.objectsEnvironment)
    update_problem_file_objects("slios_environment_problem", writer.objectsEnvironment)
    update_problem_file_init("slios_environment_problem", writer.initEnvironment)
    plan_name, plan = get_plan('slios_environment_domain', 'slios_environment_problem')
    print(plan_to_list(plan=plan))

    writer = problem_writer()
    writer.setPersons(2)
    writer.setNewPerson(1)
    writer.setNewPerson(2)

    writer.setChairs(3)
    writer.setFreeChair(1,1)
    writer.setFreeChair(2,2)

    writer.setRooms(2)
    writer.setOnePersonMoreInRoom(1)

    writer.finishInit()
    writer.finishObjects()
    print(writer.initEnvironment)
    print(writer.objectsEnvironment)
    update_problem_file_objects("slios_distribution_problem", writer.objectsDistribution)
    update_problem_file_init("slios_distribution_problem", writer.initDistribution)
    plan_name, plan = get_plan('slios_distribution_domain', 'slios_distribution_problem')
    print(plan_to_list(plan=plan))
