import random

import faker.providers
from django.core.management.base import BaseCommand
from faker import Faker, providers
from crm_project.models import Member, Work


def generateCandidate(fake):
    fullName = fake.name() # make fake name
    fullName = fullName.split()
    fName = fullName[0]
    lName = fullName[1]

    desPos = random.choice(position)  # make desired position random
    email = fake.ascii_free_email()
    country = fake.country()
    education = random.choice(list_of_educs)
    phoneNumb = fake.phone_number()

    try:
        mId = Member.objects.latest('id').id + 1
    except:
        print("heeh")
        mId = 0

    # part with generation data used for generation of work too

    jobsBefore = random.randint(1, 10)
    yearsOfExp = random.randint(jobsBefore // 2, jobsBefore * 2)

    Member.objects.create(firstname=fName, lastname=lName, phone=phoneNumb,
                          email=email, country=country, id=mId,
                          education=education, desired_position=desPos,
                          amount_of_workplaces=jobsBefore, total_years_of_exp=yearsOfExp)

    generateWork(fake, mId, jobsBefore, yearsOfExp)


def generateWork(fake, candidateId, jobsBefore, yearsOfExp):
    yearsWorkedTotal = yearsOfExp
    yearsWorkedAtMoment = 0
    for i in range(jobsBefore):
        companyName = random.choice(company)
        if (yearsWorkedTotal <= jobsBefore):
            years = 0.5
        else:
            years = random.randint(1, yearsWorkedTotal // 2)
        yearsWorkedAtMoment += years;
        yearsWorkedTotal -= years

        sphere = fake.bs()
        salary = yearsWorkedAtMoment * random.randint(850, 1200)
        level = yearsWorkedAtMoment // 2

        try:
            wId = Work.objects.latest('id').id + 1
        except:
            print("damn boy try worked")
            wId = 0


        Work.objects.create(id=wId, mId=Member.objects.get(id=candidateId),
                            company_name=companyName, reference=random.randint(0, 1),
                            years=years, salary=salary, level=level)


class Command(BaseCommand):
    help = "Command information"

    def handle(self, *args, **kwargs):
        fake = Faker()

        for i in range(20):
            generateCandidate(fake)

        checkMembers = Member.objects.all().count()
        self.stdout.write(self.style.SUCCESS(f"Number of MEMBERS: {checkMembers}"))
        self.stdout.write(Member.objects.all().values_list("id"))
        self.stdout.write(Work.objects.all().values_list("id"))


position = [
    "Python Developer",
    "Mobile Applications Developer",
    "Information Systems Security",
    "Database Developer",
    "Artificial Intelligence Engineer",
    "Full - Stack Developer",
    "DevOps Engineer",
    "Data Scientist",
    "Software Test Engineer",
    "Kotlin Developer",
    "Front-end Developer",
    "Ruby on Rails developer"
]
list_of_educs = [
    "Associate Degree",
    "Bachelor's Degree",
    "Master's Degree",
    "Doctoral Degree",
    "None"
]
company = [
    "Walmart",
    "Amazon",
    "Apple",
    "CVS Health",
    "UnitedHealth Group",
    "Exxon Mobil",
    "Berkshire Hathaway",
    "Alphabet",
    "McKesson",
    "AmerisourceBergen",
    "GSK plc",
    "American Express",
    "Abbott Laboratories",
    "StoneX Group",
    "Oracle Corporation",
    "Coca-Cola Company",
    "General Dynamics",
    "Verizon",
    "Bank of America",
    "Microsoft",
    "Alexander & Baldwin",
    "Blue Planet Software",
    "Kamakura Corporation",
    "AGCO",
    "Beazer Homes USA",
    "EarthLink",
    "Hitachi Koki U.S.A. Ltd. and Hitachi Telecom Inc.",
    "Turner Broadcasting System",
    "Bulsatcom",
    "SAP",
    "MR TECH",
    "Mov & Comp",
    "CBT",
    "Star",
    "XYZ tribe",
    "Creatio",
    "Ciellos",
    "Codexio",
    "Tuc Tam"
]


class Provider(faker.providers.BaseProvider):
    def role(self):
        return self.random_element(position)
