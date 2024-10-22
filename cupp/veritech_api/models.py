from django.db import models
from django.utils import timezone


# General table
class General(models.Model):
    employeeid = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    employeecode = models.CharField(max_length=10, null=True, blank=True)
    originname = models.CharField(max_length=50, null=True, blank=True)
    urag = models.CharField(max_length=50, null=True, blank=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    stateregnumber = models.CharField(max_length=50, null=True, blank=True)
    dateofbirth = models.DateField(null=True, blank=True)
    employeephone = models.CharField(max_length=20, null=True, blank=True)
    postaddress = models.EmailField(null=True, blank=True)
    educationlevel = models.CharField(max_length=50, null=True, blank=True)
    maritalstatus = models.CharField(max_length=50, null=True, blank=True)
    nooffamilymember = models.IntegerField(null=True, blank=True)
    noofchildren = models.IntegerField(null=True, blank=True)
    departmentname = models.CharField(max_length=50, null=True, blank=True)
    positionname = models.CharField(max_length=100, null=True, blank=True)
    insuredtypename = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically update on every save


# Address table
class Address(models.Model):
    employeeid = models.CharField(max_length=20, null=True, blank=True)
    addresstypename = models.CharField(max_length=100, null=True, blank=True)
    cityname = models.CharField(max_length=50, null=True, blank=True)
    districtname = models.CharField(max_length=50, null=True, blank=True)
    streetname = models.CharField(max_length=100, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Bank table
class Bank(models.Model):
    employeeid = models.CharField(max_length=20, null=True, blank=True)
    bankname = models.CharField(max_length=100, null=True, blank=True)
    bankaccountnumber = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Experience table
class Experience(models.Model):
    employeeid = models.CharField(max_length=20, null=True, blank=True)
    organizationname = models.CharField(max_length=100, null=True, blank=True)
    departmentname = models.CharField(max_length=100, null=True, blank=True)
    positionname = models.CharField(max_length=100, null=True, blank=True)
    startdate = models.DateField(null=True, blank=True)
    enddate = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Education table
class Education(models.Model):
    employeeid = models.CharField(max_length=20, null=True, blank=True)
    edutype = models.CharField(max_length=100, null=True, blank=True)
    edulevel = models.CharField(max_length=100, null=True, blank=True)
    startyearid = models.CharField(max_length=4, null=True, blank=True)
    endyearid = models.CharField(max_length=4, null=True, blank=True)
    countryname = models.CharField(max_length=50, null=True, blank=True)
    cityname = models.CharField(max_length=50, null=True, blank=True)
    schoolname = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Attitude table for Punishment/Reward
class Attitude(models.Model):
    employeeid = models.CharField(max_length=20, null=True, blank=True)
    punishment = models.CharField(max_length=100, null=True, blank=True)
    punishmentdate = models.DateField(null=True, blank=True)
    punishmenttypeid = models.CharField(max_length=100, null=True, blank=True)
    rewardtypename = models.CharField(max_length=100, null=True, blank=True)
    rewardname = models.CharField(max_length=100, null=True, blank=True)
    rewarddate = models.DateField(null=True, blank=True)
    organizationname = models.CharField(max_length=100, null=True, blank=True)
    rectorshipnumber = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Family table
class Family(models.Model):
    employeeid = models.CharField(max_length=20, null=True, blank=True)
    relationshipname = models.CharField(max_length=50, null=True, blank=True)
    firstname = models.CharField(max_length=50, null=True, blank=True)
    lastname = models.CharField(max_length=50, null=True, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    workname = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


# Skills table for language, talent, skills, hrmexam
class Skills(models.Model):
    employeeid = models.CharField(max_length=20, null=True, blank=True)
    skillname = models.CharField(max_length=100, null=True, blank=True)
    examname = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
