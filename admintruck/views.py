from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
import boto3

dynamodb = boto3.resource('dynamodb',region_name = 'ap-south-1',aws_access_key_id="AKIA5O3E5IOBPSOBNZXJ",aws_secret_access_key="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")
trucks = ['truck1','truck2','truck3','truck4','truck5']
trucksUser = ['truck1','truck2','truck3']

def loginVerification(request,username,password):
    try:
        table = dynamodb.Table('gpglobal')
        response = table.get_item(Key={'username':username,'password':password})
        if len(response) > 1:
            if response['Item']['isAdmin'] == "True" :
                return "Admin",response['Item']['username']
            return "Customer",response['Item']['username']
        else:
            raise Exception("Failed Login")
    except Exception as e:
        print(str(e))
        return "Error",str(e)


# Create your views here.
#source ~/eb-virt/bin/activate

def login(request):
    if request.method == "GET":
        if request.session.has_key("username"):
            return redirect('/')
        client = boto3.client('dynamodb',region_name = 'ap-south-1')
        response = client.get_item(TableName='gpglobal', Key={
            'username':{
                "S":"admin@admin",
            },
            'password':{
                "S":"admin",
            },
        })
        return render(request,"login.html",{'response':response})
    if request.method == "POST":
        emailaddress = request.POST['email']
        password = request.POST['password'] 
        errMsg,username = loginVerification(request,emailaddress,password)
        if errMsg == "Error":
            messages.warning(request, 'Incorrect emailid or password')
            return redirect('/login')
        if errMsg == "Admin":
            request.session['username'] = username
            request.session['GpGlobal'] = 'Admin'
            request.session.set_expiry(500)
            return redirect('/')
            # return redirect('../trucks')
        elif errMsg == 'Customer':
            request.session['username'] = username
            request.session['GpGlobal'] = 'Customer'
            request.session.set_expiry(500)
            return redirect('/')
        else:
            messages.warning(request,"Cannot Login")
            return redirect('/login')
    
def homePage(request):
    if request.method == "GET":
        if request.session.has_key("username"):
            if request.session['GpGlobal'] == "Admin":
                return render(request,"index.html",{"trucks":trucks})
            else:
                return render(request,"user.html",{"trucks":trucksUser})
        else:
            return redirect('/login')

def logout(request):
    try:
        del request.session['username']
        messages.warning(request,"Logged Out")
        return redirect('/login')
    except Exception as e:
        messages.warning(request,str(e))
        return redirect('/login')