from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import *
import pandas as pd
import sys
# Create your views here.

@csrf_exempt
@login_required(login_url='login_page')
def upload_data(request):
    if request.method == 'POST':
        # save the uploaded file here
            uploaded_file = request.FILES.get('image')
        # try:
            # to upload the file to the database
            filesUploadModelObj = uploadedCsvFile()
            filesUploadModelObj.title = "NA"
            filesUploadModelObj.uploaded_file = uploaded_file
            filesUploadModelObj.save()
            response_message = "File Uploaded Successfully"

            parent_df=pd.read_csv(filesUploadModelObj.uploaded_file, iterator=True, chunksize=100000)
            for chunk in parent_df:
                chunk = chunk.rename(columns={
                    'Unnamed: 0':'unique_number',
                    'name':'company_name',
                    'year founded': 'year_founded', 
                    'size range': 'size_range',
                    'linkedin url': 'linkedin_url',
                    'current employee estimate': 'current_employee_estimate',
                    'total employee estimate': 'current_employee_estimate'
                })
                print(chunk)
                records = chunk.to_records(index=False)
                instances = [companiesModel(**record) for record in records]
                companiesModel.objects.bulk_create(instances)


                # for index, row in chunk.iterrows():

                #     companiesModelObj = companiesModel()
                #     companiesModelObj.unique_number = row[0]
                #     companiesModelObj.name = row['name']
                #     companiesModelObj.domain = row['domain']
                #     if row['year founded'] != 0:
                #         companiesModelObj.year_founded = row['year founded']
                    
                #     companiesModelObj.industry = row['industry']
                #     companiesModelObj.size_range = row['size range']
                #     companiesModelObj.locality = row['locality']
                    
                #     if row['locality'] != '':
                #         companiesModelObj.city = str(row['locality']).split(',')[0]
                #         try:
                #             companiesModelObj.state = str(row['locality']).split(',')[1]
                #         except:
                #             pass
                    
                #     companiesModelObj.country = row['country']
                #     companiesModelObj.linkedin_url = row['linkedin url']

                #     if row['current employee estimate'] != '':
                #         companiesModelObj.current_employee_estimate = row['current employee estimate']
                    
                #     if row['total employee estimate'] != '':
                #         companiesModelObj.total_employee_estimate = row['total employee estimate']

                #     companiesModelObj.save()
            # to upload the content of the file to the database
            # data=''
            # with open(filesUploadModelObj.uploaded_file.url, 'rb') as f:
            #     data=f.read()
            # print(data)
        # except Exception as e:
        #     print(e)
        #     exception_type, exception_object, exception_traceback = sys.exc_info()
        #     filename = exception_traceback.tb_frame.f_code.co_filename
        #     line_number = exception_traceback.tb_lineno
        #     print("Exception type: ", exception_type)
        #     print("File name: ", filename)
        #     print("Line number: ", line_number)
        #     response_message = "An error Occurred. Please Try Again"
            return JsonResponse({'message':response_message})
    return render(request, 'upload_data.html')

@login_required(login_url='login_page')
def query_builder(request):
    return render(request, 'query_builder.html')
