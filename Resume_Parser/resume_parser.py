import re
import spacy
from spacy.matcher import Matcher
import datefinder
from date_extractor import extract_dates

nlp = spacy.load("TrainedResumeModel")

def extract_mobile_number(text):
    pattern = re.compile(r'([+(]?\d+[)\-]?[ \t\r\f\v]*[(]?\d{2,}[()\-]?[ \t\r\f\v]*\d{2,}[()\-]?[ \t\r\f\v]*\d*[ \t\r\f\v]*\d*[ \t\r\f\v]*)')
    phone=pattern.findall(text)
    phone = [re.sub(r'[,.]', '', el) for el in phone if len(re.sub(r'[()\-.,\s+]', '', el))>9]
    phone = [re.sub(r'\D$', '', el).strip() for el in phone]

    if phone:
        number = ''.join(phone[0])
        if len(number) < 10:
            return "Not Found"
        else:
            return number

def get_email(text):
     finalemail=""
     pattern = re.compile(r'\S*@\S*')
     matches = pattern.findall(text)
     if matches:
         firstemail=matches[0]
         if len(matches)>1:
             if(matches[0]!=matches[1]):
                finalemail=matches[0]+" "+matches[1]
                return finalemail
             elif(matches[0]==matches[1]):

                return matches[0]
             else:
                 return "Not Found"
         elif(len(matches)!=-1):
              return firstemail
         else:
             return "Not Found"
     else:
         return "Not Found"

def name_extractor(text,nlp):
    doc = nlp(text)
    Name=""
    FirstName=""
    LastName=""
    name=""
    if doc.ents!=():
        for ent in doc.ents:
            if ent.label_=="Name":
                Name=ent.text
                if Name:
                    data=Name.split()
                    size=len(data)
                    if size==3:
                        FirstName=data[0]
                        LastName=data[2]
                        break
                    elif size==2:
                        FirstName=data[0]
                        LastName=data[1]
                        break
                    else:
                        FirstName=data[0]
                        break
        if Name:
             return Name,FirstName,LastName
        else:
            return "","",""
    else:
        return "","",""

def get_Gender(text):
    if text !="":
        data=text.split()
        for i in data:
            name=data[0]
            name.lower()
            break
        list=['a','i']
        gen=name[-1]
        for temp in list:
            if gen==temp:
                result="female"
                break
            else:
                result="male"
        if result:
            return result
        else:
            return ""
    else:
        return ""

def extract_skills(resume_text,nlp):
    doc = nlp(resume_text)
    skills=[]
    temp=""
    for ent in doc.ents:
        if ent.label_=="Skills":
            temp=ent.text
            skills.append(temp)
    if skills:
        return skills
    else:
        return ""


def extract_Education(text,nlp):
    doc = nlp(text)
    Education=[]
    temp=""
    for ent in doc.ents:
        if ent.label_=="Education":
            temp=ent.text
            Education.append(temp)
    if Education:
        return Education
    else:
        return ""

def extract_Company(text,nlp):
    doc = nlp(text)
    Company=[]
    temp=""
    for ent in doc.ents:
        if ent.label_=="Company":
            temp=ent.text
            Company.append(temp)
    if Company:
        return Company
    else:
        return ""

def extract_JobRole(text,nlp):
    doc = nlp(text)
    Role=[]
    for ent in doc.ents:
        if ent.label_=="Role":
            temp=ent.text
            Role.append(temp)
    if Role:
        return Role
    else:
        return ""

def extract_experience(text,nlp):
    doc = nlp(text)
    Experience=""
    for ent in doc.ents:
        if ent.label_=="Experience":
            Experience=ent.text
    if Experience:
        return Experience
    else:
        return ""

def extract_Nationality(text,nlp):
    doc=nlp(text)
    Nationality=""
    for ent in doc.ents:
        if ent.label_=="Nationality":
            Nationality=ent.text
    if Nationality:
        return Nationality
    else:
        return ""

def extract_Marital(text,nlp):
    doc=nlp(text)
    Marital=""
    for ent in doc.ents:
        if ent.label_=="Marital":
            Marital=ent.text
    if Marital:
        return Marital
    else:
        return ""

def extract_institution(text,nlp):
    doc = nlp(text)
    Institution=[]
    temp=" "
    for ent in doc.ents:
        if ent.label_=="Institution":
            temp=ent.text
            Institution.append(temp)
    if Institution:

        return Institution
    else:
        return ""

def extact_AddressDet(text):
    pattern= re.compile(r'([0-9]{6}|[0-9]{3}\s[0-9]{3})')
    pincode=pattern.findall(text)
    Address=[]
    pincode = [re.sub(r'[,.]', '', el) for el in pincode if len(re.sub(r'[()\-.,\s+]', '', el))==6]
    if pincode:
        pincode=pincode[0]
    if pincode:
        nomi = pgeocode.Nominatim('in')
        a=nomi.query_postal_code(pincode)
        state_name=a.loc['state_name']
        Address.append(state_name)
        city=a.loc['community_name']
        Address.append(city)
        return Address

def extract_Passport(text,nlp):
    doc=nlp(text)
    PassportNo=""
    temp=" "
    for ent in doc.ents:
        if ent.label_=="PassportNo":
            PassportNo=ent.text
    if PassportNo:
        return PassportNo
    else:
        return ""

def extract_DOB(text):
    Dob=""
    rawdata=""
    textSplit=text.splitlines()
    count=len(textSplit)
    i=0
    for data in textSplit:
        pattern=re.compile('Date of Birth|dob|DOB|D.O.B|d.o.b|date of birth|Date of birth|dateofbirth|DATE OF BIRTH|Date of Birth')
        temp=pattern.findall(data)
        i=i+1
        if len(temp)!=0:
            rawdata=data
            if i<count:
                rawdata=rawdata+""+textSplit[i]
                final=count-i
                if final>=2:
                    rawdata=rawdata+""+textSplit[i+1]
                    rawdata=rawdata.replace("?","")
                    rawdata=" ".join(rawdata.split())
                    break
    if rawdata != "":
        matches=datefinder.find_dates(rawdata)
        month=""
        day=""
        for match in matches:
            Dob=match
            tempmonth=len(str(Dob.month))
            tempday=len(str(Dob.day))
            if tempmonth!=2:
                month=str(0)+str(Dob.month)
            else:
                month=str(Dob.month)

            if tempday!=2:
                day=str(0)+str(Dob.day)
            else:
                day=str(Dob.day)

            Dob=day+"."+ month +"."+str(Dob.year)
            break

        if Dob=="":
            date=extract_dates(rawdata)
            for match in date:
                Dob=match
                Dob=str(Dob.day)+"-"+str(Dob.month)+"-"+str(Dob.year)
                break
        return Dob
    else:
        return ""

def Resume_Path(extracted_text):
    if (extracted_text!=""):
        Mobile_Number=extract_mobile_number(extracted_text)
        Email=get_email(extracted_text)
        Name,FirstName,LastName=name_extractor(extracted_text,nlp)
        Role=extract_JobRole(extracted_text,nlp)
        Company=extract_Company(extracted_text,nlp)
        education=extract_Education(extracted_text,nlp)
        skills=extract_skills(extracted_text,nlp)
        Experience=extract_experience(extracted_text,nlp)
        Gender=get_Gender(Name)
        Institution=extract_institution(extracted_text,nlp)
        Marital=extract_Marital(extracted_text,nlp)
        Nationality=extract_Nationality(extracted_text,nlp)
        PassportNo=extract_Passport(extracted_text,nlp)
        DateofBirth=extract_DOB(extracted_text)
        return Name,FirstName,LastName,Email,Mobile_Number,skills,Gender,Role,Company,education,Experience,Institution,Marital,Nationality,PassportNo,DateofBirth
    else:
        return "unable to process resume"
