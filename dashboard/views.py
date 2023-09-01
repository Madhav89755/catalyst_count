from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.db.models import Max, Min
from django.http import JsonResponse
from rest_framework import status
from .models import *
import pandas as pd
import sys
import threading
import time
import os
import io

# Create your views here.

@csrf_exempt
@login_required(login_url='login_page')
def upload_data(request):
    if request.method == 'POST':
        # save the uploaded file here
        uploaded_file = request.FILES.get('image')
        response_message = ""
        flag=0
        try:
            # to upload the file to the database
            filesUploadModelObj = uploadedCsvFile()
            filesUploadModelObj.title = "NA"
            filesUploadModelObj.uploaded_file = uploaded_file
            filesUploadModelObj.save()
            # response_message = "File Uploaded Successfully"

            def upload_chunk_data(chunk):
                # this function is called by the threads to read the files and upload data inside them chunk by chunk
                chunk = chunk.rename(columns={
                    'Unnamed: 0':'unique_number',
                    'name':'company_name',
                    'year founded': 'year_founded', 
                    'size range': 'size_range',
                    'linkedin url': 'linkedin_url',
                    'current employee estimate': 'current_employee_estimate',
                    'total employee estimate': 'total_employee_estimate'
                })
                chunk[['city', 'state', 'country_2']] = chunk['locality'].str.split(',', expand=True)
                chunk.drop(columns="country_2", inplace=True)
                chunk['year_founded'].fillna(value = 0, inplace=True)                
                instances = [companiesModel(
                    unique_number = row['unique_number'],
                    company_name = str(row['company_name']).title(),
                    domain = row['domain'],
                    year_founded = row['year_founded'],
                    industry = str(row['industry']).title(),
                    size_range = row['size_range'],
                    locality = str(row['locality']).title(),
                    city = str(row['city']).title(),
                    state = str(row['state']).title(),
                    country = str(row['country']).title(),
                    linkedin_url = row['linkedin_url'],
                    current_employee_estimate = row['current_employee_estimate'],
                    total_employee_estimate = row['total_employee_estimate']
                ) for index, row in chunk.iterrows()]
                companiesModel.objects.bulk_create(instances)

            parent_df=pd.read_csv(filesUploadModelObj.uploaded_file, iterator=True, chunksize=100000)
            threads = []
            for chunk in parent_df:
                if flag ==0:
                    modelColumnNames=[
                        "name",
                        "domain",
                        "year founded",
                        "industry",
                        "size range",
                        "locality",
                        "country",
                        "linkedin url",
                        "current employee estimate",
                        "total employee estimate"
                    ]
                    all_elements_exist = all(item in chunk.columns for item in modelColumnNames)
                    if all_elements_exist == False:
                        flag=1
                        raise TypeError("Uploaded CSV file does not contain the following columns please check: name, domain ,year founded, industry, size range, locality, country,linkedin url, current employee estimate, total employee estimate")


                # Create multiple threads
                thread = threading.Thread(target=upload_chunk_data, args=(chunk,))
                threads.append(thread)

            # Start the threads
            for thread in threads:
                thread.start()

            # Wait for all threads to finish
            for thread in threads:
                thread.join()
            
            response_message = "Data uploaded successfully"
            print("All threads finished")

        except TypeError:
            time.sleep(7)
            response_message = "Uploaded CSV file does not contain the following columns please check: name, domain ,year founded, industry, size range, locality, country, linkedin url, current employee estimate, total employee estimate"
        except Exception as e:
            print(e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno
            print("Exception type: ", exception_type)
            print("File name: ", filename)
            print("Line number: ", line_number)
            response_message = "An error Occurred. Please Try Again"
        finally:
            print("Finally")
            # file_path = filesUploadModelObj.uploaded_file.path
            # # Delete the file if it exists
            # if os.path.exists(file_path):
            #     os.remove(file_path)
            # filesUploadModelObj.delete()
        print(response_message)
        return JsonResponse({'message':response_message})
    return render(request, 'upload_data.html')

@login_required(login_url='login_page')
def query_builder(request):
    companiesModelObj = companiesModel.objects.all()
    context = {}
    context['city'] = companiesModelObj.values_list('city', flat=True).distinct()
    context['state'] = companiesModelObj.values_list('state', flat=True).distinct()
    context['countryList'] = companiesModelObj.values_list('country', flat=True).distinct()
    context['industry'] = companiesModelObj.values_list('industry', flat=True).distinct()
    context['year_founded'] = companiesModelObj.values_list('year_founded', flat=True).distinct()


    max_value = companiesModelObj.aggregate(max_value=Max('total_employee_estimate'))['max_value']
    min_value = companiesModelObj.aggregate(min_value=Min('total_employee_estimate'))['min_value']
    print("Maximum value:", max_value)    
    print("Minimum value:", min_value)
    return render(request, 'query_builder.html', context)

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def query_api(request):
    status_code = status.HTTP_200_OK
    if request.method=='POST':
        try:
            company_name = request.POST.get('company_name')
            year_founded = request.POST.get('year_founded')
            industry = request.POST.get('industry')
            city = request.POST.get('city')
            state = request.POST.get('state')
            country = request.POST.get('country')
            total_employee_estimate = request.POST.get('total_employee_estimate')

            companiesModelObj = companiesModel.objects.all()

            if total_employee_estimate!="NA":
                companiesModelObj = companiesModelObj.filter(total_employee_estimate = total_employee_estimate)
            if company_name not in ["NA",'', None]:
                companiesModelObj = companiesModelObj.filter(company_name__in = company_name)
            if industry!="NA":
                companiesModelObj = companiesModelObj.filter(industry__in = industry)
            if city != "NA":
                companiesModelObj = companiesModelObj.filter(city__in = city)
            if state != "NA":
                companiesModelObj = companiesModelObj.filter(state__in = state)
            if country != "NA":
                companiesModelObj = companiesModelObj.filter(country__in = country)
            if year_founded!="NA" and type(year_founded)=='int':
                companiesModelObj = companiesModelObj.filter(year_founded = year_founded)

            context={"message":f"There are {companiesModelObj.count()} object for the records"}
        except Exception as e:
            print("Error ",e)
            exception_type, exception_object, exception_traceback = sys.exc_info()
            filename = exception_traceback.tb_frame.f_code.co_filename
            line_number = exception_traceback.tb_lineno
            print("Exception type: ", exception_type)
            print("File name: ", filename)
            print("Line number: ", line_number)
            status_code = status.HTTP_400_BAD_REQUEST
            context={"message":"An error occurred"}
    return Response(context,status=status_code)