import requests,bs4,time,smtplib,time,datetime

countryDict = {
    "Country": "",
    "Total Cases": "",
    "New Cases": "",
    "Total Deaths": "",
    "New Deaths": "",
    "Total Recovered": "",
    "Active Cases": "",
    "Serious Critical": "",
    "Total Cases in 1M pop": "",
    "Deaths in 1M pop": "",
    "Total Tests": "",
    "Tests in 1M pop": "",
    "Population": ""
}


def CoronaWorld(country):
    #grab number,name,deaths from country
    corona_live_count = requests.get('https://www.worldometers.info/coronavirus/')
    corona_live_count.raise_for_status()

    soup = bs4.BeautifulSoup (corona_live_count.text, 'html.parser')    

    table = soup.find('table',{'class':'table'})

    table_rows = table.findAll('tr')

    current_stats = open(r'C:\MyPythonScripts\CoronaMacedoniaUpdater\CurrentStats.txt','w')
    
    change = False #a flag for comparing previous with new statistics
    for tr in table_rows:
        td = tr.findAll('td')
        row = [i.text for i in td]
        for sublist in row:
            if str(country) in sublist:
                column=0
                for key,header in countryDict.items():
                    if header!=row[column]:
                        change = True
                    column+=1
                column=0      
                for header in countryDict.keys():   
                    if change == True:
                        countryDict[header]=row[column]
                        column+=1
                        

    column=0
    Final_String = ''
    for key,item in countryDict.items():
        Final_String+=(key+': '+item+'\n')

        #failed code that I may comeback in the future
        #It's purpose was to compare the numbers in a txt file and if there were changes to replace them with new
        '''if (column >=1 and column <= 7):
            number = int(lines[column])
            number_of_people = item
            if number_of_people == ' ':
                number_of_people = 0
            else:
                number_of_people = int(item.strip().replace(',','').replace('+',''))
            #print(f"{number_of_people} <= {number}")

            if (column >= 1) and (number <= number_of_people): ''' 
        current_stats.write(key + ': ' + str(item.strip())+'\n')

        column+=1
        
    global your_email,password, sendto, nologin #makeglobalvariables of password and emails to feed into the SendMail function
    
    current_stats.close()
    if change == True and nologin == False:
        print('\n'+Final_String)
        SendMail(Final_String,your_email,password,sendto)
    elif change == True and nologin == True:
        print('\n'+Final_String)
    else:
        print('No change in Stats!')
        

def SendMail(chunk,your_email,password,sendto):
    #send mail to info you entered 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(your_email,password)
    subject = ('Corona Virus Stats about country!')

    msg = f'Subject : {subject}\n\n{chunk}\nMessage has been sent on:{datetime.datetime.now()}'
    server.sendmail(
        your_email,
        sendto,
        msg
        )
    server.quit()
    print('Message Delivered Succesfully')

nologin = True
yesno = input('Do you want to login? (yes/no)\n')
if yesno.lower() == 'y'  or yesno.lower() =='yes':
    your_email = input('What\'s you email: ')
    password = input('What\'s you app-password: ')
    sendto = input('Send these stats to: ')
    nologin=False

country = input('\nCheck Live Stats on People infected by Corona by Country:\n')

while True:
    CoronaWorld(country)
    time.sleep(1800)  # recheck after 30 minutes
