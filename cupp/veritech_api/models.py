from django.db import models


class Employee(models.Model):
    employee_id = models.CharField(max_length=50)
    gender = models.CharField(max_length=50)
    employee_code = models.CharField(max_length=50)
    origin_name = models.CharField(max_length=100, blank=True)
    urag = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    state_reg_number = models.CharField(max_length=20)
    date_of_birth = models.DateField()
    employee_phone = models.CharField(max_length=20)
    post_address = models.CharField(max_length=255, blank=True)
    education_level = models.CharField(max_length=50, blank=True)
    marital_status = models.CharField(max_length=50, blank=True)
    no_of_family_members = models.IntegerField(null=True, blank=True)
    no_of_children = models.IntegerField(null=True, blank=True)
    department_name = models.CharField(max_length=255)
    position_name = models.CharField(max_length=255)
    insured_type_name = models.CharField(max_length=255)


class EmployeeAddress(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='addresses')
    address_type_name = models.CharField(max_length=255)
    city_name = models.CharField(max_length=255)
    district_name = models.CharField(max_length=255)
    street_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)


class EmployeeBank(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='banks')
    bank_name = models.CharField(max_length=255)
    bank_account_number = models.CharField(max_length=50)


class EmployeeWorkExperience(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='work_experiences')
    organization_name = models.CharField(max_length=255)
    department_name = models.CharField(max_length=255)
    position_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)


class EmployeeFamily(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='family_members')
    relationship_name = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    mobile = models.CharField(max_length=20)
    work_name = models.CharField(max_length=255, blank=True)
