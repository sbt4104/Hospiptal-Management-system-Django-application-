from django.shortcuts import render
from account.forms import UserForm,UserProfileInfoForm , UserForm2, UserProfileInfoForm2, Searchprofession
from account.models import UserProfileInfo, UserProfileInfo2
from api1.models import Schedules, Case
from api1.forms import SchedulesForm


# Extra Imports for the Login and Logout Capabilities
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from api1.forms import CaseForm, Fromdoctodate, Updatehelper

import io
from django.http import FileResponse
from reportlab.pdfgen import canvas

def upload_csv(request):
    data = {}
    if "GET" == request.method:
        return render(request, "basic_app/mlinput.html", data)
    # if not GET, then proceed
    try:
        csv_file = request.FILES["csv_file"]
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("basic_app:upload_csv"))
        #if file is too large, return
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size/(1000*1000),))
            return HttpResponseRedirect(reverse("basic_app:upload_csv"))

        file_data = csv_file.read().decode("utf-8").splitlines()		
        print(file_data[0])
        csvv = []
        rt=0
        for i in file_data:
                if rt==0:
                    rt=rt+1
                    continue
                else:
                    csvv.append(i.split(','))
                rt=rt+1
        matrix=[] 
        print(len(csvv))  
        print(csvv[0][1])
        Y=[]    
        for i in range(len(csvv)):
            temp=[]
            try:
                for j in range(1,10):
                    #print(temp)
                    temp.append(int(csvv[i][j]))
                if csvv[i][10]=='2':
                    Y.append(0)
                else:    
                    Y.append(1)

                matrix.append(temp)           
            except:
                print("error again")     
        print(matrix)       
        print(Y) 
        print(len(matrix),len(Y))
        from sklearn.neural_network import MLPClassifier
        clf = MLPClassifier(hidden_layer_sizes=(1024,512), activation="relu", solver='adam', alpha=0.0001, batch_size='auto', learning_rate="constant", learning_rate_init=0.001, power_t=0.5, max_iter=16000, shuffle=True, random_state=None, tol=1e-4, verbose=False, warm_start=False, momentum=0.9, nesterovs_momentum=True, early_stopping=False, validation_fraction=0.1, beta_1=0.9, beta_2=0.999, epsilon=1e-8)
        clf.fit(matrix,Y)
        print('done')    
    except Exception as e:
        print('error')

    return HttpResponseRedirect(reverse("basic_app:upload_csv"))


@login_required
def downloadpdf(request, pk):
    buffer = io.BytesIO()
    print('you are in')
    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)

    obj = Case.objects.get(pk = pk)
    pres = obj.prescription
    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    p.drawString(100, 100, pres)

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='report.pdf')


@login_required
def show_all1(request):
    #pat = Case.objects.filter(patients = request.user) 
    person = UserProfileInfo.objects.get(user = request.user)
    doc = Case.objects.filter(doctor = person)
    
    return render(request,'basic_app/showall.html', {'person':person, 'doc':doc})

@login_required
def show_all2(request):
    person = UserProfileInfo2.objects.get(user = request.user)
    pat = Case.objects.filter(patient = person) 
    #doc = Case.objects.filter(doctors = request.user)

    return render(request,'basic_app/showall.html', {'person':person, 'pat':pat})

@login_required
def updatestatus1(request,pk):
    obj = Case.objects.get(pk=pk)
    form = Updatehelper()
    person = UserProfileInfo.objects.get(user=request.user)
    return render(request,'basic_app/updatestatus.html',{'form':form, 'ider':pk, 'person':person})

@login_required
def updatestatus2(request,pk):
    if request.method=="POST":
        obj = Case.objects.get(pk=pk)
        print(request.POST)
        pres = request.POST.get("prescription")
        stat = request.POST.get("status")
        print(pres, stat)
        obj.status = stat
        obj.prescription = pres
        obj.save() 
    else:
        print("remove bugs")
    return HttpResponseRedirect(reverse('basic_app:appointdoc'))


@login_required
def deletesc(request,pk):
    obj = Schedules.objects.get(pk=pk)
    obj.delete()
    return HttpResponseRedirect(reverse('basic_app:schedules1'))

@login_required
def selectdoctor(request,pk):
    selected = Schedules.objects.get(pk=pk)
    selected.status = 1
    selected.save()
    print(selected.avlday)
    form = Case( doctor=selected.user, appointday= "12/12/12" , appointtime="01:02:03")
    #svd = form.save(commit=False)
    form.doctor = selected.user
    user1 = UserProfileInfo2.objects.get(user = request.user)
    form.patient = user1
    form.appointday = selected.avlday
    form.appointtime = selected.avltime
    #print(svd)
    form.save()
    return HttpResponseRedirect(reverse('basic_app:appointment'))     

@login_required
def appointdoc(request):
    user1 = UserProfileInfo.objects.get(user = request.user)
    all = Case.objects.filter(status = 'inprocess').filter(doctor = user1) | Case.objects.filter(status = 'accepted').filter(doctor = user1)
    person = UserProfileInfo.objects.get(user=request.user)
    return render(request, 'basic_app/appointdoc.html', {'all':all,'person':person})

@login_required
def searchfield(request):
    flag=False
    person = UserProfileInfo2.objects.get(user=request.user)
    form = Searchprofession()
    if request.method=="POST":
        obj = UserProfileInfo.objects.filter(field = request.POST.get('field'))
        flag=True
        return render(request,'basic_app/showme.html',{'form':form, 'obj':obj,'flag':flag,'person': person})
    return render(request,'basic_app/showme.html',{'form':form,'flag':flag, 'person': person})

@login_required
def doctoform(request):
    doc = UserProfileInfo.objects.get(id=request.POST.get('doctor'))
    #print(request.POST)
    print(doc)
    all = Schedules.objects.filter(user=doc).filter(status=0)
    person = UserProfileInfo2.objects.get(user = request.user)
    return render(request,'basic_app/selectdoc2.html', {'all':all, 'person':person,'doc':doc})

@login_required
def appointment(request):
    user1 = UserProfileInfo2.objects.get(user = request.user)
    history = Case.objects.filter(patient = user1)
    person = UserProfileInfo2.objects.get(user=request.user)
    if request.method == "POST":
        form2 = Fromdoctodate(data=request.POST)

        if form2.is_valid:
            svd = form2.save(commit=False)
            svd.patient = user1
            svd.save()
        else:
            print("error")
    else:
        form2 = Fromdoctodate()
    return render(request,'basic_app/appointment.html',{'form2':form2, 'history':history, 'person':person})                

@login_required
def schedules1(request):
    user1 = UserProfileInfo.objects.get(user = request.user)
    form = Schedules.objects.filter(user = user1)
    doc = Case.objects.filter(doctor = user1)
    
    if request.method=="POST":
        form2 = SchedulesForm(data=request.POST)
        if form2.is_valid:
            svd = form2.save(commit=False)
            svd.user = user1
            svd.save()
        else:
            print("error")     
    else:
        form2 = SchedulesForm()    
    return render(request, 'basic_app/schedules.html',{'form':form,'doc':doc,'person':user1,'form2':form2})

@login_required
def schedules2(request):
    user1 = UserProfileInfo2.objects.get(user = request.user)
    pat = Case.objects.filter(patient = user1)
    return render(request, 'basic_app/schedules.html',{'form':form,'pat':pat,'person':user1})    

# Create your views here.
def index1(request):
    person = UserProfileInfo.objects.get(user=request.user)
    return render(request,'basic_app/index.html', {'person':person})

def index2(request):
    person = UserProfileInfo2.objects.get(user=request.user)
    return render(request,'basic_app/index.html',{'person':person})    

def welcome(request):
    return render(request,'basic_app/index.html')

@login_required
def special(request):
    # Remember to also set login url in settings.py!
    # LOGIN_URL = '/basic_app/user_login/'
    return HttpResponse("You are logged in. Nice!")

@login_required
def user_logout(request):
    # Log out the user.
    logout(request)
    # Return to homepage.
    return HttpResponseRedirect(reverse('welcome'))

def register(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileInfoForm(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']
            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'basic_app/registration.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login(request):

    if request.method == 'POST':
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)
        
        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index1'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'basic_app/login.html', {})



def register2(request):

    registered = False

    if request.method == 'POST':

        # Get info from "both" forms
        # It appears as one form to the user on the .html page
        user_form = UserForm2(data=request.POST)
        profile_form = UserProfileInfoForm2(data=request.POST)

        # Check to see both forms are valid
        if user_form.is_valid() and profile_form.is_valid():

            # Save User Form to Database
            user = user_form.save()

            # Hash the password
            user.set_password(user.password)

            # Update with Hashed password
            user.save()

            # Now we deal with the extra info!

            # Can't commit yet because we still need to manipulate
            profile = profile_form.save(commit=False)

            # Set One to One relationship between
            # UserForm and UserProfileInfoForm
            profile.user = user

            # Check if they provided a profile picture
            if 'profile_pic' in request.FILES:
                print('found it')
                # If yes, then grab it from the POST form reply
                profile.profile_pic = request.FILES['profile_pic']

            # Now save model
            profile.save()

            # Registration Successful!
            registered = True

        else:
            # One of the forms was invalid if this else gets called.
            print(user_form.errors,profile_form.errors)

    else:
        # Was not an HTTP post so we just render the forms as blank.
        user_form = UserForm2()
        profile_form = UserProfileInfoForm2()

    # This is the render and context dictionary to feed
    # back to the registration.html file page.
    return render(request,'basic_app/registration2.html',
                          {'user_form':user_form,
                           'profile_form':profile_form,
                           'registered':registered})

def user_login2(request):

    if request.method == 'POST':
        print(request)
        # First get the username and password supplied
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Django's built-in authentication function:
        user = authenticate(username=username, password=password)
        #print(user.designation)
        # If we have a user
        if user:
            #Check it the account is active
            if user.is_active:
                #print(user.designation)
                # Log the user in.
                login(request,user)
                # Send the user back to some page.
                # In this case their homepage.
                return HttpResponseRedirect(reverse('index2'))
            else:
                # If account is not active:
                return HttpResponse("Your account is not active.")
        else:
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".format(username,password))
            return HttpResponse("Invalid login details supplied.")

    else:
        #Nothing has been provided for username or password.
        return render(request, 'basic_app/login2.html', {})        