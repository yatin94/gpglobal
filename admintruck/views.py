from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect
import boto3

dynamodb = boto3.resource('dynamodb',region_name = 'ap-south-1',aws_access_key_id="AKIA5O3E5IOBPSOBNZXJ",aws_secret_access_key="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")

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
        return render(request,"login.html")
    if request.method == "POST":
        emailaddress = request.POST['email']
        password = request.POST['password'] 
        errMsg,username = loginVerification(request,emailaddress,password)
        if errMsg == "Error":
            messages.warning(request, 'Incorrect emailid or password')
            return redirect('/login')
        if errMsg == "Admin":
            request.session['username'] = username
            request.session.set_expiry(50)
            # return redirect('../trucks')
            return HttpResponse("inside")
        messages.warning(request, 'Not yet decided')
        return redirect('login')