import json
import requests
from django.http import JsonResponse
from .models import Employee, EmployeeAddress, EmployeeBank, EmployeeWorkExperience, EmployeeFamily
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def save_employee_data(request):
    if request.method == 'POST':
        # Assuming data is sent as a JSON body
        data = json.loads(request.body.decode('utf-8'))

        for key, employee_data in data.items():
            # Create or get the employee object
            employee, created = Employee.objects.update_or_create(
                employee_id=employee_data['employeeid'],
                defaults={
                    'gender': employee_data.get('gender'),
                    'employee_code': employee_data.get('employeecode'),
                    'origin_name': employee_data.get('originname', ''),
                    'urag': employee_data.get('urag', ''),
                    'first_name': employee_data['firstname'],
                    'last_name': employee_data['lastname'],
                    'state_reg_number': employee_data['stateregnumber'],
                    'date_of_birth': employee_data['dateofbirth'],
                    'employee_phone': employee_data['employeephone'],
                    'post_address': employee_data.get('postaddress', ''),
                    'education_level': employee_data.get('educationlevel', ''),
                    'marital_status': employee_data.get('maritalstatus', ''),
                    'no_of_family_members': employee_data.get('nooffamilymember', None),
                    'no_of_children': employee_data.get('noofchildren', None),
                    'department_name': employee_data['departmentname'],
                    'position_name': employee_data['positionname'],
                    'insured_type_name': employee_data['insuredtypename'],
                }
            )

            # Saving employee addresses
            if 'empaddress' in employee_data:
                for _, address_data in employee_data['empaddress'].items():
                    EmployeeAddress.objects.update_or_create(
                        employee=employee,
                        address_type_name=address_data['addresstypename'],
                        defaults={
                            'city_name': address_data['cityname'],
                            'district_name': address_data['districtname'],
                            'street_name': address_data['streetname'],
                            'address': address_data['address'],
                        }
                    )

            # Saving employee bank details
            if 'empbank' in employee_data:
                for _, bank_data in employee_data['empbank'].items():
                    EmployeeBank.objects.update_or_create(
                        employee=employee,
                        bank_name=bank_data['bankname'],
                        defaults={'bank_account_number': bank_data['bankaccountnumber']}
                    )

            # Saving work experience
            if 'empworkexp' in employee_data:
                for _, workexp_data in employee_data['empworkexp'].items():
                    EmployeeWorkExperience.objects.update_or_create(
                        employee=employee,
                        organization_name=workexp_data['organizationname'],
                        defaults={
                            'department_name': workexp_data['departmentname'],
                            'position_name': workexp_data['positionname'],
                            'start_date': workexp_data['startdate'],
                            'end_date': workexp_data.get('enddate', None),
                        }
                    )

            # Saving family members
            if 'empfamily' in employee_data:
                for _, family_data in employee_data['empfamily'].items():
                    EmployeeFamily.objects.update_or_create(
                        employee=employee,
                        relationship_name=family_data['relationshipname'],
                        defaults={
                            'first_name': family_data['firstname'],
                            'last_name': family_data['lastname'],
                            'birth_date': family_data['birthdate'],
                            'mobile': family_data['mobile'],
                            'work_name': family_data.get('workname', '')
                        }
                    )

        # After saving the employee data, make the external POST request
        url = "http://10.10.90.22:8080/erp-services/RestWS/runJson"
        request_body = {
            "request": {
                "username": "cu_hr",
                "password": "123",
                "command": "cuHrEmpInfoDv_004V2",
                "parameters": {
                    "criteria": {
                        "id": {
                            "0": {
                                "operator": "=",
                                "operand": "1"
                            }
                        }
                    }
                }
            }
        }

        try:
            response = requests.post(url, json=request_body)

            # Check if the response status is OK (200) and contains content
            if response.status_code == 200:
                # Check if the response contains JSON data
                try:
                    response_data = response.json()
                    return JsonResponse({
                        'message': 'Data saved successfully and external API call succeeded.',
                        'api_response': response_data
                    })
                except json.JSONDecodeError:
                    return JsonResponse({
                        'message': 'Data saved successfully, but external API returned invalid JSON.',
                        'api_response': response.text  # Return raw response content for debugging
                    }, status=500)
            else:
                return JsonResponse({
                    'message': 'Data saved successfully, but external API call failed with status code: ' + str(
                        response.status_code),
                    'api_response': response.text  # Include the raw response for debugging
                }, status=500)

        except requests.exceptions.RequestException as e:
            return JsonResponse({
                'message': 'Data saved successfully, but external API call encountered an error.',
                'error': str(e)
            }, status=500)
