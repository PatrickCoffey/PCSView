#!/usr/bin/python
# -*- coding: utf-8 -*-

# PCSView - indivPerson
# ---------------------
# This is the individual client class

class Demographics(object):
    """
    Demogrpahics
    ------------
    This is a class that represents the demographics subclass of the individual person
    """
    firstName = ''
    lastName = ''
    gender = ''
    indigStatus = ''
    NOK = ''
    medicareNumber = ''
    medicareExp = ''

    def __init__(self, firstName, lastName, gender, indigStatus, NOK, medicareNumber, medicareExp):
        self.firstName = firstName
        self.lastName = lastName
        self.gender = gender
        self.indigStatus = indigStatus
        self.NOK = NOK
        self.medicareNumber = medicareNumber
        self.medicareExp = medicareExp

class NB(object):
    """
    NB
    --
    This is a class that represents the NB subclass of the individual person
    """
    provider = ''
    notes = ''
    date = ''

    def __init__(self, provider, notes, date):
        self.provider = provider
        self.notes = notes
        self.date = date

class Alert(object):
    """
    Alert
    -----
    This is a class that represents the Alert subclass of the individual person
    This is used to store the other alerts and medication allergies.
    """
    actDate = ''
    alertType = ''
    notes = ''

    def __init__(self, actDate, alertType, notes):
        self.actDate = actDate
        self.alertType = alterType
        self.notes = notes

class Issue(object):
    """
    Issue
    -----
    This is a class that represents the Issue subclass of the individual person
    This is used to store the other the problem list
    """
    diagDate = ''
    problem = ''
    onset = ''
    status = ''

    def __init__(self, diagDate, problem, onset, status):
        self.diagDate = diagDate
        self.problem = problem
        self.onset = onset
        self.status = status

class Medication(object):
    """
    Medication
    ----------
    This is a class that represents the medication subclass of the individual person
    This is used to store the other alerts and medication allergies.
    """
    name = ''
    dosageInst = ''

    def __init__(self, name, dosageInst):
        self.name = name
        self.dosageInst = dosageInst

class Recall(object):
    """
    Recall
    ------
    This is a class that represents the recall subclass of the individual person
    This is used to store the other Recalls
    """
    item = ''
    notes = ''
    dueDate = ''
    provGroup = ''

    def __init__(self, item, dueDate, provGroup, notes):
        self.item = item
        self.dueDate = dueDate
        self.provGroup = provGroup
        self.notes = notes

class Imm(object):
    """
    Medication
    ----------
    This is a class that represents the medication subclass of the individual person
    This is used to store the other alerts and medication allergies.
    """
    date = ''
    immName = ''
    prov = ''

    def __init__(self, date, immName, prov):
        self.prov = prov
        self.date = date
        self.immName = immName

class IndivPerson(object):
    """
    indivPerson
    -----------
    This is the individual client class, it represents a client.
    """
    clientID = 0
    demographics = object
    NBs = []
    drugAllergies = []
    otherAlerts = []
    risks = []
    pastHx = []
    currentProb = []
    longMed = []
    shortMed = []
    recallOverdue = []
    recall = []
    imms = []

    def __init__(self, clientID=0):
        self.clientID = clientID

    def setDemographics(self, firstName, lastName, gender, indigStatus, NOK, medicareNumber=None, medicareExp=None):
        """Pretty much mandatory, demographics are like the metadata for a client"""
        self.demographics = Demographics(firstName, lastName, gender, indigStatus, NOK, medicareNumber, medicareExp)

    def addNB(self, provider, notes, date):
        """Adds NB's to the clients file"""
        self.NBs.append(NB(provider, notes, date))

    def addDrugAllergy(self, actDate, alertType, notes):
        self.drugAllergies.append(Alert(actDate, alertType, notes))

    def addOtherAlert(self, actDate, alertType, notes):
        self.otherAlerts.append(Alert(actDate, alertType, notes))

    def addRisk(self, actDate, alertType, notes):
        self.risks.append(Alert(actDate, alertType, notes))

    def addPastHx(self, diagDate, problem, onset, status):
        self.pastHx.append(Issue(diagDate, problem, onset, status))

    def addCurrentProb(self, diagDate, problem, onset, status):
        self.currentProb.append(Issue(diagDate, problem, onset, status))

    def addLongMed(self, name, dosageInst):
        self.longMed.append(Medication(name, dosageInst))

    def addShortMed(self, name, dosageInst):
        self.shortMed.append(Medication(name, dosageInst))

    def addRecallOverdue(self, item, dueDate, provGroup, notes):
        self.recallOverdue.append(Recall(item, dueDate, provGroup, notes))

    def addRecall(self, item, dueDate, provGroup, notes):
        self.recall.append(Recall(item, dueDate, provGroup, notes))

    def addImm(self, date, immName, prov):
        self.imms.append(Imm(date, immName, prov))


if __name__=='__main__':
    test = IndivPerson(1234567)
    test.addNB('Noob, Derp', 'A whole bunch of free text cus doctors love that shit...', '1/1/2015')
    test.addImm('1/2/2015', 'Tetnus - Ouch!', 'Noob, Derp')
    test.addImm('1/3/2015', 'Tetnus - Ouch! - 2', 'Noob, Derp')
    test.addPastHx('1/5/2015', 'Cancer-Aids', 'what the hell is this?', "Confirmed")
    print(str(test.clientID))