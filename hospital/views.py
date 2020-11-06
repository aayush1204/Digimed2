from django.shortcuts import render
from django.shortcuts import render,redirect,reverse
from . import models
from .models import Doctor,Patient,Receptionist, Profile, Appointment, PhoneNumber
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required,user_passes_test
from datetime import datetime,timedelta,date
from django.conf import settings
from django.contrib.auth.models import User, auth

# Create your views here.
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/index.html')

def doctorclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/doctorclick.html')

def doctor_signup_view(request):

    if (request.method == "POST"):
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        # email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        # confirm_password=request.POST['confirm_password']

        clinicname = request.POST['clinicname']
        specialization = request.POST['specialization']
        sex = request.POST['sex']
        age =  request.POST['age']
        buildingname =  request.POST['buildingname']
        sname = request.POST['Sname']
        city =  request.POST['city']
        zipcode = request.POST['pincode']

        user = User.objects.create_user(first_name=first_name, last_name=last_name,username=username,password=password)

        user.save()
        profile = Profile.objects.create(sex=sex,age=age,Bname=buildingname,Sname=sname,city=city,pincode=zipcode,user=user)
        profile.save()
        doctor = Doctor.objects.create(user=user,clinicname=clinicname,specialization=specialization,doctorId=user.id)
        doctor.save()
        return HttpResponseRedirect('doctorlogin')
    
    return render(request,'hospital/doctorsignup.html')

def doctor_dashboard_view(request):
    #for three cards
    # patientcount=models.Patient.objects.all().filter(status=True,assignedDoctorId=request.user.id).count()
    if(request.method=="POST"):

        username=request.POST['username']
        password=request.POST['password']

        user =  auth.authenticate(username=username,password=password)
        
        try:
            
            auth.login(request, user)
            return redirect('doctor-dashboard')
        except:
                # messages.info(request, "Incorrect Credentials. Please enter the correct ones!")
            return render(request, 'doctorlogin.html')
    appointmentcount=Appointment.objects.all().filter(isCancelled=False,doctorId=request.user.id).count()
    # patientdischarged=models.PatientDischargeDetails.objects.all().distinct().filter(assignedDoctorName=request.user.first_name).count()

    #for  table in doctor dashboard
    appointments = Appointment.objects.all().filter(isCancelled=False,doctorId=request.user.id)
    patientid=[]
    for a in appointments:
        patientid.append(a.patientId)
    patients=models.Patient.objects.all().filter(user_id__in=patientid)
    appointments=zip(appointments,patients)
    mydict={
    # 'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    # 'patientdischarged':patientdischarged,
    'appointments':appointments,
    'doctor':Doctor.objects.filter(doctorId=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_dashboard.html',context=mydict)

def doctor_appointment_view(request):
    doctor=Doctor.objects.filter(doctorId=request.user.id) #for profile picture of doctor in sidebar
    return render(request,'hospital/doctor_appointment.html',{'doctor':doctor})

def doctor_view_appointment_view(request):
    doctor=Doctor.objects.filter(doctorId=request.user.id) #for profile picture of doctor in sidebar
    appointments=Appointment.objects.all().filter(doctorId__doctorId=request.user.id)
    print(appointments)
    patientid=[]
    for a in appointments:
        patientid.append(str(a.patientId))
    # patients = models.Patient.objects.all().filter(patientStatus=True,patientId__in=patientid)

    patients = models.AttendsTO.objects.all().filter(did__doctorId=request.user.id, pid__patientStatus=True)
    phoneno=[]
    for i in patients:
        temp = models.PhoneNumber.objects.all().get(user__id=i.pid.patientId)
        print(temp.phone)
        phoneno.append(temp.phone)
    print(patients)
    
    appointments=zip(appointments,patients,phoneno)
    return render(request,'hospital/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})

def patientclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/patientclick.html')

def patient_signup_view(request):
    
    if (request.method == "POST"):
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        # email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        # confirm_password=request.POST['confirm_password']

        phone=request.POST['phonenumber']
        sex = request.POST['sex']
        age =  request.POST['age']
        buildingname =  request.POST['buildingname']
        sname = request.POST['Sname']
        city =  request.POST['city']
        zipcode = request.POST['pincode']

        user = User.objects.create_user(first_name=first_name, last_name=last_name,username=username,password=password)

        user.save()
        profile = Profile.objects.create(sex=sex,age=age,Bname=buildingname,Sname=sname,city=city,pincode=zipcode,user=user)
        profile.save()
        patient = Patient.objects.create(user=user,patientId=user.id)
        patient.save()
        phoneno = PhoneNumber.objects.create(phone=phone,user=user)
        phoneno.save()
        return HttpResponseRedirect('patientlogin')
    return render(request,'hospital/patientsignup.html')

def patient_dashboard_view(request):
    patient=Patient.objects.filter(patientId=request.user.id)

    if(request.method=="POST"):

        username=request.POST['username']
        password=request.POST['password']

        user =  auth.authenticate(username=username,password=password)
        
        try:
            
            auth.login(request, user)
            return redirect('patient-dashboard')
        except:
                # messages.info(request, "Incorrect Credentials. Please enter the correct ones!")
            return render(request, 'patientlogin.html')
    # doctor=Appointment.objects.filter(patientId = patient.patientId)
    # Doctor.objects.get(user_id=patient.assignedDoctorId)
    mydict={
    'patient':patient,
    # 'doctorName':doctor.get_name,
    # 'doctorMobile':doctor.mobile,
    # 'doctorAddress':doctor.address,
    'doctor':'doctor',
    # 'symptoms':patient.symptoms,
    # 'doctorDepartment':doctor.department,
    # 'admitDate':patient.admitDate,
    }
    return render(request,'hospital/patient_dashboard.html',context=mydict)  

#### RECORDS ####
def patient_records(request):
    return render(request,'hospital/patient_records.html')

def patient_view_records(request):
    patient=Patient.objects.get(patientId=request.user.id)
    print(request.user.id)
    print(patient)
    records=models.Records.objects.filter(pid=patient)
    
    # for i in records:
    #     descriptionlist.append(models.Description.objects.filter(rid = i))
    descriptionlist = models.Description.objects.all().filter(rid__in = models.Records.objects.all().filter(pid=patient))
    # patients=models.Patient.objects.all().filter(user_id__in=patientid)
    return render(request,'hospital/patient_view_records.html',{'patient':patient,'descriptionlist':descriptionlist})

def patient_upload_records(request):
    if request.method == 'GET':
        uploadform = forms.UploadRecordForm()
        return render(request,'hospital/patient_upload_records.html',{'uploadform':uploadform})
    else:
        uploadform = forms.UploadRecordForm(request.FILES)
        descmodel = Description()
        descmodel.recimage = uploadform.recimage
        descmodel.save()
        return render(request,'hospital/patient_upload_records.html',{'message':'Uploaded Successfully'})

def adminclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/adminclick.html')

def admin_signup_view(request):
    # form=forms.AdminSigupForm()
    # if request.method=='POST':
    #     form=forms.AdminSigupForm(request.POST)
    #     if form.is_valid():
    #         user=form.save()
    #         user.set_password(user.password)
    #         user.save()

    #         Receptionist.objects.create(user = user, receptionistid=user.id, clinicname=form.clinicname, jobstatus=form.jobstatus)

    #         my_admin_group = Group.objects.get_or_create(name='ADMIN')
    #         my_admin_group[0].user_set.add(user)
    #         return HttpResponseRedirect('adminlogin')
    if(request.method=="POST" ):    
        first_name=request.POST['firstname']
        last_name=request.POST['lastname']
        # email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        clinicname = request.POST['clinicname']
        user = User.objects.create_user(first_name=first_name, last_name=last_name,username=username,password=password)

        user.save()

        reception = Receptionist.objects.create(user=user,receptionistid=user.id,clinicname=clinicname,jobstatus='P')
        reception.save()
        return HttpResponseRedirect('adminlogin')
    return render(request,'hospital/adminsignup.html')

def admin_dashboard_view(request):
    #for both table in admin dashboard
    if(request.method=="POST"):

        username=request.POST['username']
        password=request.POST['password']

        user =  auth.authenticate(username=username,password=password)
        
        try:
            
            auth.login(request, user)
            return redirect('admin-dashboard')
        except:
                # messages.info(request, "Incorrect Credentials. Please enter the correct ones!")
            return render(request, 'adminlogin.html')
    doctors=models.Doctor.objects.all().order_by('-id')
    patients=models.Patient.objects.all().order_by('-id')
    #for three cards
    doctorcount=models.Doctor.objects.all().count()
    pendingdoctorcount=models.Doctor.objects.all().count()

    patientcount=models.Patient.objects.all().count()
    pendingpatientcount=models.Patient.objects.all().count()

    appointmentcount=models.Appointment.objects.all().count()
    pendingappointmentcount=models.Appointment.objects.all().count()
    mydict={
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'hospital/admin_dashboard.html',context=mydict)