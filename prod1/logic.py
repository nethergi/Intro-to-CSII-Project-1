from PyQt6.QtWidgets import *
from os import path
import csv


def clear(obj, fullReset=False):
    """Clears the window of all values"""
    obj.idEdit.setText('')
    obj.writeinEdit.setText('')
    obj.outputLabel.setText("")

    obj.voteTotalLabel1a.setText('')
    obj.voteTotalLabel2a.setText('')
    obj.voteTotalLabel3a.setText('')
    obj.voteTotalLabel4a.setText('')
    obj.voteTotalLabelOtherA.setText('')

    obj.voteTotalLabel1b.setText('')
    obj.voteTotalLabel2b.setText('')
    obj.voteTotalLabel3b.setText('')
    obj.voteTotalLabel4b.setText('')
    obj.voteTotalLabelOtherB.setText('')

    obj.janeRadio.setChecked(False)
    obj.johnRadio.setChecked(False)

def vote(obj):
    """Casts user's vote. Disallows duplicates, non-number IDs, and IDs <= 0"""
    #Creates file if one does not exist
    if not path.exists('votes.csv'):
        with open('votes.csv', 'a') as v:
            pass
    
    id = str(obj.idEdit.text())

    #decides whether to throw an error
    with open('votes.csv', 'r') as raw:
        voteRead = csv.reader(raw)
        try:
            for line in voteRead:
                if id == line[0]:
                    obj.outputLabel.setStyleSheet("color: red;")
                    obj.outputLabel.setText('ALREADY VOTED')
                    return
                elif not id.isdigit():
                    obj.outputLabel.setStyleSheet("color: red;")
                    obj.outputLabel.setText('INVALID ID: Please use only numbers')
                    return
                elif int(id) <= 0:
                    obj.outputLabel.setStyleSheet("color: red;")
                    obj.outputLabel.setText('INVALID ID: IDs must be positive and above 0')
                    return
        except IndexError:
            pass
        
        #Collects Vote
    with open('votes.csv', 'a', newline='') as raw:
        voteWrite = csv.writer(raw)

        if not obj.writeinEdit.text().strip() == '':
            voteWrite.writerow([id, obj.writeinEdit.text().strip().lower()])
        elif obj.janeRadio.isChecked():
            voteWrite.writerow([id, 'jane'])
        elif obj.johnRadio.isChecked():
            voteWrite.writerow([id, 'john'])
        else:
            obj.outputLabel.setStyleSheet("color: red;")
            obj.outputLabel.setText('Select or write-in a vote')
            return

    clear(obj)

    obj.outputLabel.setStyleSheet("color: green;")
    obj.outputLabel.setText('Vote successful!')
            



def voteTotal(obj):
    """Calculates the total votes and percentages"""
    if path.exists('votes.csv'): #Only runs if file exists
        voteCount = {}

        with open('votes.csv', 'r') as raw:
            voteRead = csv.reader(raw)
            tmp = next(voteRead)
            voteCount.update({tmp[1]:1})

            #iterates through votes to tally them
            try:
                for line in voteRead:
                    key = list(voteCount.keys())
                    for i in range(len(key)):
                        if line[1] == key[i]:
                            voteCount[line[1]] += 1
                        elif voteCount.get(line[1]) == None:
                            voteCount.update({line[1]: 1})
                        else:
                            pass
            except IndexError:
                pass
        
        print(voteCount)
        voteCount = dict(sorted(voteCount.items(), key=lambda item: item[1], reverse=True)) #sorts dict

        totalVotes = sum(list(voteCount.values()))

        i = 0
        #displays values
        for key, value in voteCount.items():
            match i:
                case 0:
                    obj.voteTotalLabel1a.setText(key)
                    obj.voteTotalLabel1b.setText(f'{value}  -  {round(value/totalVotes *100, 2)}%')
                case 1:
                    obj.voteTotalLabel2a.setText(key)
                    obj.voteTotalLabel2b.setText(f'{value}  -  {round(value/totalVotes *100, 2)}%')
                case 2:
                    obj.voteTotalLabel3a.setText(key)
                    obj.voteTotalLabel3b.setText(f'{value}  -  {round(value/totalVotes *100, 2)}%')
                case 3:
                    obj.voteTotalLabel4a.setText(key)
                    obj.voteTotalLabel4b.setText(f'{value}  -  {round(value/totalVotes *100, 2)}%')
                case 4:
                    obj.voteTotalLabelOtherA.setText('Other')
                    obj.voteTotalLabelOtherB.setText(f'{sum(list(voteCount.values())[i:])} - {round(sum(list(voteCount.values())[i:])/totalVotes *100, 2)}%')
                    break
            i += 1

            

    else:
        clear(obj)
        obj.outputLabel.setStyleSheet("color: orange;")
        obj.outputLabel.setText('No votes cast')