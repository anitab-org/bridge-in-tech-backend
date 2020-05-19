from enum import Enum, unique
# from sqlalchemy import Enum
# from sqlalchemy.dialects.postgresql import ENUM

@unique
class ProgramStatus(Enum):
    DRAFT = "Draft"
    OPEN = "Open"
    IN_PROGRESS = "In_Progress"
    COMPLETED = "Completed"
    CLOSED = "Closed"

    def programStatus(self):
        return list(map(str, self))

@unique
class OrganizationStatus(Enum):
    DRAFT = "Draft"
    PUBLISH = "Publish"
    ARCHIVED = "Archived"

    def OrganizationStatus(self):
        return list(map(str, self))

@unique
class Gender(Enum):
    FEMALE = "Female"
    MALE = "Male"
    OTHER = "Other"
    DECLINED = "Prefer not to say"
    NOT_APPLICABLE = "Not Applicable"

    def gender(self):
        return list(map(str, self))

@unique
class Age(Enum):
    UNDER_18 = "Under 18"
    AGE_18_TO_20 = "Between 18 to 20 yo"
    AGE_21_TO_24 = "Between 21 to 24 yo"
    AGE_25_TO_34 = "Between 25 to 34 yo"
    AGE_35_TO_44 = "Between 35 to 44 yo"
    AGE_45_TO_54 = "Between 45 to 54 yo"
    AGE_55_TO_64 = "Between 55 to 64 yo"
    ABOVE_65_YO = "Above 65 yo"
    DECLINED = "Prefer not to say"
    NOT_APPLICABLE = "Not Applicable"

    def age(self):
        return list(map(str, self))

@unique
class Ethnicity(Enum):
    AFRICAN_AMERICAN = "African-American/Black"
    CAUCASIAN = "Caucasian/White"
    HISPANIC = "Hispanic/Latinx"
    NATIVE_AMERICAN = "Native American/Alaska Native/First Nations"
    MIDDLE_EASTERN = "Middle Eastern/North African (MENA)"
    ASIAN = "Asian"
    OTHER = "Other"
    DECLINED = "Prefer not to say"
    NOT_APPLICABLE = "Not Applicable"

    def ethnicity(self):
        return list(map(str, self))

@unique
class SexualOrientation(Enum):
    HETEROSEXUAL = "Heterosexual/Straight"
    LGBTIA = "LGBTIA+"
    OTHER = "Other"
    DECLINED = "Prefer not to say"
    NOT_APPLICABLE = "Not Applicable"

    def sexualOrientation(self):
        return list(map(str, self))

@unique
class Religion(Enum):
    CHRISTIANITY = "Christianity"
    JUDAISM = "Judaism"
    ISLAM = "Islam"
    HINDUISM = "Hinduism"
    BUDDHISM = "Buddhism"
    OTHER = "Other"
    DECLINED = "Prefer not to say"
    NOT_APPLICABLE = "Not Applicable"

    def religion(self):
        return list(map(str, self))

@unique
class PhysicalAbility(Enum):
    WITH_DISABILITY = "With/had limited physical ability (or with/had some type of physical disability/ies)"
    WITHOUT_DISABILITY = "Without/have no limitation to physical ability/ies"
    DECLINED = "Prefer not to say"
    NOT_APPLICABLE = "Not Applicable"

    def physicalAbility(self):
        return list(map(str, self))

@unique
class MentalAbility(Enum):
    WITH_DISORDER = "With/previously had some type of mental disorders"
    WITHOUT_DISORDER = "Without/have no mental disorders"
    DECLINED = "Prefer not to say"
    NOT_APPLICABLE = "Not Applicable"

    def mentalAbility(self):
        return list(map(str, self))

@unique
class SocioEconomic(Enum):
    UPPER = "Upper class/Elite"
    UPPER_MIDDLE = "Upper Middle class (or High-level Professionals/white collars e.g. enginers/accountants/lawyers/architects/managers/directors"
    LOWER_MIDDLE = "Lower Middle class (e.g. blue collars in skilled trades/Paralegals/Bank tellers/Sales/Clerical-Admin/other support workers)"
    WORKING = "Working class (e.g. craft workers, factory labourers, restaurant/delivery services workers"
    BELOW_POVERTY = "Underclass, working but with wages under poverty line, receiving Social Benefit from Government"
    DECLINED = "Prefer not to say"
    NOT_APPLICABLE = "Not Applicable"

    def socioEconomic(self):
        return list(map(str, self))

@unique
class HighestEducation(Enum):
    BELOW_HIGH_SCHOOL = "Have/did not completed High School"
    HIGH_SCHOOL = "High School Diploma"
    ASSOCIATE = "Associate Degree"
    BACHELOR = "Bachelor's Degree"
    MASTER = "Master's Degree"
    PHD = "PhD or other Doctorate Degrees"
    OTHER = "Other"
    DECLINED = "Prefer not to say"
    NOT_APPLICABLE = "Not Applicable"

    def highestEducation(self):
        return list(map(str, self))

@unique
class YearsOfExperience(Enum):
    UNDER_ONE = "Less than a year"
    UP_TO_3 = "Up to 3 years"
    UP_TO_5 = "Up to 5 years"
    UP_TO_10 = "Up to 10 year"
    OVER_10 = "Over 10 years of experience"
    DECLINED = "Prefer not to say"
    NOT_APPLICABLE = "Not Applicable"

    def yearsOfExperience(self):
        return list(map(str, self))

@unique
class ContactType(Enum):
    FACE_TO_FACE = "Face-to-face"
    REMOTE = "Remote"
    BOTH = "Both Remote and Face-to-face"
    
    def contactType(self):
        return list(map(str, self))

@unique
class Zone(Enum):
    LOCAL = "Local",
    NATIONAL = "National",
    GLOBAL = "Global",

    def zone(self):
        return list(map(str, self))

@unique
class Timezone(Enum):
    CAPE_VERDE_TIME = "UTC-01:00/Cape Verde Time"
    NEWFOUNDLAND_STANDARD_TIME = "UTC-03:30/NewFoundland_Standard_Time"
    ATLANTTIC_STANDARD_TIME = "UTC-04:00/Atlantic Standard Time"
    EASTERN_STANDARD_TIME = "UTC-05:00/Eastern Standard Time"
    CENTRAL_STANDARD_TIME = "UTC-06:00/Central Standard Time"
    MOUNTAIN_STANDARD_TIME = "UTC-07:00/Mountain Standard Time"
    PACIFIC_STANDARD_TIME = "UTC-08:00/Pacific Standard Time"
    ALASKA_STANDARD_TIME = "UTC-09:00/Alaska Standard Time"
    HAWAII_ALEUTIAN_STANDARD_TIME = "UTC-10:00/Hawaii-Aleutian Standard Time"
    SAMOA_STANDARD_TIME = "UTC-11:00/Samoa Standard Time"
    GREENWICH_MEAN_TIME = "UTC+00:00/Greenwich Mean Time and Western European Time"
    CENTRAL_EUROPEAN_TIME = "UTC+01:00/Central European Time"
    WEST_AFRICA_TIME = "UTC+01:00/West Africa Time"
    EASTERN_EUROPEAN_TIME = "UTC+02:00/Eastern European Time"
    CENTRAL_SOUTH_AFRICA_TIME = "UTC+02:00/Central and South Africa Standard Time"
    EAST_AFRICA_TIME = "UTC+03:00/East Africa Time"
    MOSKOW_TIME = "UTC+03:00/Moskow Time"
    CHARLIE_TIME = "UTC+03:00/Charlie Time - Middle East Time"
    DELTA_TIME = "UTC+04:00/Delta Time - Middle East Time"
    INDIA_STANDARD_TIME = "UTC+05:30/India Standard Time"
    CHINA_STANDARD_TIME = "UTC+08:00/China Standard TIme"
    AUSTRALIAN_WESTERN_STANDARD_TIME = "UTC+08:00/Australian Western Standard Time"
    AUSTRALIAN_CENTRAL_SOUTH_STANDARD_TIME = "UTC+09:30/Australian Central and South Standard Time"
    AUSTRALIAN_EASTERN_STANDARD_TIME = "UTC+10:00/Australian Eastern Standard Time"
    NEW_ZEALAND_STANDARD_TIME = "UTC+12:00/New Zealand Standard Time"



    def timezone(self):
        return list(map(str, self))
