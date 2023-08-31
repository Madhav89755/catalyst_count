from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

# Create your views here.
def loginView(request):
    return render(request, 'authorization/login.html')



@login_required(login_url='login_page')
def manage_users(request):
    context={}
    if request.method =="GET":
        try:
            context['userList'] = User.objects.all().order_by('-date_joined').values('id','first_name','last_name','username','email','is_active','date_joined')
        except Exception as e:
            print("Error occurred in manage_users_views while fetching data",e)

    if request.method == 'POST':
        # to delete a user
        if 'deleteUser' in request.POST:
            try:
                user_id = request.POST['user_id']
                User.objects.get(id = user_id).delete()
                messages.success(request, 'User Deleted Successfully.')
            except Exception as e:
                print("Error while deleting User object",e)
                messages.warning(request, 'User Deletion Unsuccessfull.')
        
        # to add a user
        elif 'add_new_user' in request.POST:
            try:
                invalid_values_list = ['', None, 'NA', False, True, 0, 1]
                first_name = request.POST.get('first_name')
                last_name = request.POST.get('last_name')
                username = request.POST.get('username')
                email = request.POST.get('email')
                password_1 = request.POST.get('password_1')
                password_2 = request.POST.get('password_2')

                if first_name in invalid_values_list:
                    messages.warning(request,'Please enter a valid value in First Name field')
                elif last_name in invalid_values_list:
                    messages.warning(request,'Please enter a valid value in Last Name field')
                elif username in invalid_values_list:
                    messages.warning(request,'Please enter a valid value in Username field')
                elif email in invalid_values_list:
                    messages.warning(request,'Please enter a valid value in Email field')
                elif password_1 in invalid_values_list:
                    messages.warning(request,'Please enter a valid value in Password field')
                elif password_2 in invalid_values_list:
                    messages.warning(request,'Please enter a valid value in Confirm Password field')
                elif User.objects.filter(username=username).exists():
                    messages.warning(request, 'This Username is already taken , Please try other one!')
                elif password_1 != password_2:
                    messages.warning(request, 'Passwords are not matching! Please try again.')
                else:
                    user_obj = User.objects.create_user(
                        username = username.lower(),
                        email = email.lower(),
                        first_name = first_name.title(), 
                        last_name = last_name.title(),
                        password = password_1
                    )
                    user_obj.save()
                    messages.success(request, 'User added Successfully.')
                return redirect('manage_users')
            except Exception as e:
                print("Error occurred in manage_users_views while adding new user",e)
                messages.warning(request, 'User not added.')
    
        # to update a user
        elif 'edit_user' in request.POST:
            try:
                user_id = request.POST['user_id']

                first_name = request.POST.get('first_name').title()
                last_name = request.POST.get('last_name').title()
                email = request.POST.get('email').lower()
                isActiveCheckbox = request.POST.get('isActiveCheckbox')

                user_obj = User.objects.get(id = user_id)
                user_obj.first_name = first_name
                user_obj.last_name = last_name
                user_obj.email = email
                if isActiveCheckbox == 'on':
                    user_obj.is_active = True
                else:
                    user_obj.is_active = False

                user_obj.save()
                messages.success(request, 'User Updated Successfully.')
            except Exception as e:
                print("Error occurred in manage_users_views while updating user",e)
                messages.warning(request, 'User Updation Unsuccessful.')
        return redirect('manage_users')
    return render(request, 'manage_users.html', context)

