from django.shortcuts import render
from django.shortcuts import render,redirect,reverse
from . import models, forms
from .models import Doctor,Patient,Receptionist, AttendsTO, Profile, Appointment, PhoneNumber, Symptoms, Prescription, MedicalTest, MedicinesPrescribed, PrescribedIn
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect,HttpResponse
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
    doctor=Doctor.objects.filter(doctorId=request.user.id)
    print(request.user.id)
    print(doctor) #for profile picture of doctor in sidebar
    appointments=Appointment.objects.all().filter(doctorId__user__id=request.user.id)
    print(appointments)
    phoneno=[]
    prescriptionid=[]
    test=[]
    # patientid=[]
    for a in appointments:
        # patientid.append(str(a.patientId))
        temp = models.PhoneNumber.objects.all().filter(user__id=a.patientId.user.id)
        # print(temp.phone)
        for i in temp:
            test.append(i.phone)
        phoneno.append(test)
        test=[]
    # patients = models.Patient.objects.all().filter(patientStatus=True,patientId__in=patientid)

    # patients = models.AttendsTO.objects.all().filter(did__doctorId=request.user.id, pid__patientStatus=True)

    # for i in patients:
    #     temp = models.PhoneNumber.objects.all().get(user__id=i.pid.patientId)
    #     print(temp.phone)
    #     phoneno.append(temp.phone)
    # print(patients)

    appointments=zip(appointments,phoneno)
    return render(request,'hospital/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})

def doctor_delete_appointment_view(request):
    doctor=models.Doctor.objects.get(doctorId=request.user.id) #for profile picture of doctor in sidebar
    appointments=models.Appointment.objects.all().filter(doctorId__doctorId=request.user.id)
    # patientid=[]
    # for a in appointments:
        # patientid.append(a.patientId)
    # patients=models.Patient.objects.all().filter(user_id__in=patientid)
    print(appointments)
    appointments=zip(appointments)
    return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})

# def delete_appointment_view(request,pk):
#     appointment=models.Appointment.objects.get(id=pk)
#     appointment.delete()
#     doctor=models.Doctor.objects.get(user_id=request.user.id) #for profile picture of doctor in sidebar
#     appointments=models.Appointment.objects.all().filter(status=True,doctorId=request.user.id)
#     patientid=[]
#     for a in appointments:
#         patientid.append(a.patientId)
#     patients=models.Patient.objects.all().filter(status=True,user_id__in=patientid)
#     appointments=zip(appointments,patients)
#     return render(request,'hospital/doctor_delete_appointment.html',{'appointments':appointments,'doctor':doctor})
def doctor_prescription_add(request,p):

    print(p)
    a = Appointment.objects.filter(appointmentId=p).first()
    print(a)
    x = PrescribedIn.objects.filter(aid=a)

    if not x.exists():
        presobj = Prescription.objects.create()
        presobj.save()

        PrescribedIn.objects.create(aid=a,fees=0,prescriptionid=presobj)
        pk = presobj.prescriptionid
        symptom=Symptoms.objects.filter(prescriptionid=presobj)
        medicaltest=MedicalTest.objects.filter(prescriptionid=presobj)
        medicines = MedicinesPrescribed.objects.filter(prescriptionid=presobj)
        return render(request,'hospital/doctor_prescription_add.html',{'symptoms':symptom , 'pk':pk,'medicaltest':medicaltest
                                                                        ,'medicines':medicines})

    x = PrescribedIn.objects.filter(aid=a).first()
    print(x)
    pk = x.prescriptionid.prescriptionid
    print(pk)
    symptom=Symptoms.objects.filter(prescriptionid=x.prescriptionid)
    medicaltest=MedicalTest.objects.filter(prescriptionid=x.prescriptionid)
    medicines = MedicinesPrescribed.objects.filter(prescriptionid=x.prescriptionid)
    return render(request,'hospital/doctor_prescription_add.html',{'symptoms':symptom , 'pk':pk,'medicaltest':medicaltest
                                                                        ,'medicines':medicines})

def doctor_prescription_add_symptom(request, p):
    if request.method=="POST":
        symptom = request.POST['symptom']
        pers = Prescription.objects.filter(prescriptionid=p).first()
        Symptoms.objects.create(symptoms=symptom,prescriptionid = pers)

        print(p)
    pers = Prescription.objects.filter(prescriptionid=p).first()
    symptom=Symptoms.objects.filter(prescriptionid=pers)
    medicaltest=MedicalTest.objects.filter(prescriptionid=pers)
    medicines = MedicinesPrescribed.objects.filter(prescriptionid=pers)
    pk = p
    return render(request,'hospital/doctor_prescription_add.html',{'symptoms':symptom , 'pk':pk,'medicaltest':medicaltest
                                                                        ,'medicines':medicines})

def doctor_prescription_delete_symptom(request, p, a):

    print(p)
    print(a)
    test = Symptoms.objects.get(id=a)
    print(test)
    test.delete()

    pers = Prescription.objects.filter(prescriptionid=p).first()
    symptom=Symptoms.objects.filter(prescriptionid=pers)
    medicaltest=MedicalTest.objects.filter(prescriptionid=pers)
    medicines = MedicinesPrescribed.objects.filter(prescriptionid=pers)
    pk = p
    return render(request,'hospital/doctor_prescription_add.html',{'symptoms':symptom , 'pk':pk,'medicaltest':medicaltest
                                                                        ,'medicines':medicines})




def doctor_prescription_add_medicaltest(request, p):
    if request.method=="POST":
        medicaltest = request.POST['medicaltest']
        pers = Prescription.objects.filter(prescriptionid=p).first()
        MedicalTest.objects.create(medicaltest=medicaltest,prescriptionid = pers)

        print(p)
    pers = Prescription.objects.filter(prescriptionid=p).first()
    symptom=Symptoms.objects.filter(prescriptionid=pers)
    medicaltest=MedicalTest.objects.filter(prescriptionid=pers)
    medicines = MedicinesPrescribed.objects.filter(prescriptionid=pers)
    pk = p
    return render(request,'hospital/doctor_prescription_add.html',{'symptoms':symptom , 'pk':pk, 'medicaltest':medicaltest
                                                                        ,'medicines':medicines})

def doctor_prescription_delete_medicaltest(request, p, a):

    print(p)
    print(a)
    test = MedicalTest.objects.get(id=a)
    print(test)
    test.delete()

    pers = Prescription.objects.filter(prescriptionid=p).first()
    symptom=Symptoms.objects.filter(prescriptionid=pers)
    medicaltest=MedicalTest.objects.filter(prescriptionid=pers)
    medicines = MedicinesPrescribed.objects.filter(prescriptionid=pers)
    pk = p
    return render(request,'hospital/doctor_prescription_add.html',{'symptoms':symptom , 'pk':pk,'medicaltest':medicaltest
                                                                        ,'medicines':medicines})




def doctor_prescription_add_medicines(request, p):
    if request.method=="POST":
        mname = request.POST['mname']
        mdosage = request.POST['mdosage']
        mduration = request.POST['mduration']
        pers = Prescription.objects.filter(prescriptionid=p).first()
        MedicinesPrescribed.objects.create(mname=mname,mdosage=mdosage,mduration=mduration,prescriptionid = pers)

        print(p)
    pers = Prescription.objects.filter(prescriptionid=p).first()
    symptom=Symptoms.objects.filter(prescriptionid=pers)
    medicaltest=MedicalTest.objects.filter(prescriptionid=pers)
    medicines = MedicinesPrescribed.objects.filter(prescriptionid=pers)
    pk = p
    return render(request,'hospital/doctor_prescription_add.html',{'symptoms':symptom , 'pk':pk, 'medicaltest':medicaltest
                                                                    ,'medicines':medicines})

def doctor_prescription_delete_medicines(request, p, a):

    print(p)
    print(a)
    test = MedicinesPrescribed.objects.get(id=a)
    print(test)
    test.delete()

    pers = Prescription.objects.filter(prescriptionid=p).first()
    symptom=Symptoms.objects.filter(prescriptionid=pers)
    medicaltest=MedicalTest.objects.filter(prescriptionid=pers)
    medicines = MedicinesPrescribed.objects.filter(prescriptionid=pers)
    pk = p
    return render(request,'hospital/doctor_prescription_add.html',{'symptoms':symptom , 'pk':pk,'medicaltest':medicaltest
                                                                        ,'medicines':medicines})

def doctor_view_records(request):
    doctor = Doctor.objects.get(doctorId=request.user.id)

    data = AttendsTO.objects.filter(did=doctor)

    return render(request, 'hospital/doctor_view_records.html',{'data':data})

def doctor_view_records_single(request,a):
    doctor = Doctor.objects.get(doctorId=request.user.id)

    data = AttendsTO.objects.filter(did=doctor)
    if request.method == 'POST':
        desc = models.Description.objects.get(id = request.POST['clicked'])
        return render(request,'hospital/patient_view_records2.html',{'desc':desc})
    else:
        patient=Patient.objects.get(patientId=a)
        # print(request.user.id)
        print(patient)
        records=models.Records.objects.filter(pid=patient)

        # for i in records:
        #     descriptionlist.append(models.Description.objects.filter(rid = i))
        descriptionlist = models.Description.objects.all().filter(rid__in = models.Records.objects.all().filter(pid=patient))
        # patients=models.Patient.objects.all().filter(user_id__in=patientid)
        return render(request,'hospital/doctor_view_records_single.html',{'patient':patient,'descriptionlist':descriptionlist})

    return render(requet, 'doctor_view_records.html',{'data':data})

def doctor_patient_view(request):
    mydict={
    'doctor':models.Doctor.objects.get(user_id=request.user.id), #for profile picture of doctor in sidebar
    }
    return render(request,'hospital/doctor_patient.html',context=mydict)


def doctor_view_patient_view(request):
    patients=AttendsTO.objects.all().filter(pid__patientStatus=True,did__doctorId=request.user.id)
    doctor=Doctor.objects.get(doctorId=request.user.id) #for profile picture of doctor in sidebar
    phoneno=[]
    test=[]

    for a in patients:
        # patientid.append(str(a.patientId))
        temp = models.PhoneNumber.objects.all().filter(user__id=a.pid.user.id)
        for i in temp:
            test.append(i.phone)
        # print(temp.phone)
        phoneno.append(test)
        test=[]
    patient = zip(patients,phoneno)
    return render(request,'hospital/doctor_view_patient.html',{'patients':patient,'doctor':doctor})

def doctor_view_discharge_patient_view(request):
    patients=AttendsTO.objects.all().filter(pid__patientStatus=False,did__doctorId=request.user.id)
    doctor=Doctor.objects.get(doctorId=request.user.id) #for profile picture of doctor in sidebar
    phoneno=[]
    test=[]

    for a in patients:
        # patientid.append(str(a.patientId))
        temp = models.PhoneNumber.objects.all().filter(user__id=a.pid.user.id)
        for i in temp:
            test.append(i.phone)
        # print(temp.phone)
        phoneno.append(test)
        test=[]
    patient = zip(patients,phoneno)
    return render(request,'hospital/doctor_view_patient_discharge.html',{'patients':patient,'doctor':doctor})



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
            return render(request, 'hospital/patientlogin.html')
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

def patient_appointments_cancel(request,p):

    a = Appointment.objects.get(appointmentId=p)
    a.isCancelled=True
    a.save()
    
    patient=Patient.objects.get(patientId=request.user.id)
    appointments = models.Appointment.objects.filter(patientId = patient)
    return render(request,'hospital/patient_view_appointments.html',{'patient':patient,'appointments':appointments})


#### RECORDS ####
def patient_records(request):
    return render(request,'hospital/patient_records.html')

def patient_view_records(request):
    if request.method == 'POST':
        desc = models.Description.objects.get(id = request.POST['clicked'])
        return render(request,'hospital/patient_view_records2.html',{'desc':desc})
    else:
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
        uploadform = forms.UploadRecordForm(request.POST,request.FILES)
        # descmodel = models.Description()
        # descmodel.recimage = uploadform.recordfile
        # descmodel.save()
        recordmodel = models.Records.objects.create(pid= models.Patient.objects.get(patientId=request.user.id ))
        recordmodel.save()
        print(uploadform)
        # if uploadform.is_valid():
        type = uploadform.cleaned_data['type']
        title = uploadform.cleaned_data['title']
        recimage = request.FILES['recimage']
            # print(uploadform.items())
            # uploadform.save(commit = False)
        print(recimage)
        try:
            descmodel = models.Description.objects.create(type = type,title = title,recimage = recimage, rid = recordmodel)
        except:
            print('failed')
            # uploadform.rid = recordmodel
        descmodel.save()
        return render(request,'hospital/patient_records.html.html',{'message':'Uploaded Successfully'})

#### PATIENT MY DOCTORS ####
def patient_doctors(request):
    return render(request,'hospital/patient_doctors.html')

def patient_view_doctors(request):
    patient=Patient.objects.get(patientId=request.user.id)
    doctors = models.AttendsTO.objects.filter(pid = patient)
    # doctors = models.Doctor.objects.all().filter(id = attendedby.did)
    print(patient)
    # print(doctors)

        # patients=models.Patient.objects.all().filter(user_id__in=patientid)
    return render(request,'hospital/patient_view_doctors.html',{'patient':patient,'doctors':doctors})

def patient_add_doctors(request):
    if request.method=='POST':
        add_doctor_form  = forms.AddDoctorForm(request.POST)
        did = request.POST['did']
        doc = models.Doctor.objects.get(id = did)
        patient = models.Patient.objects.get(patientId = request.user.id)
        attendstomodel = models.AttendsTO.objects.create(pid = patient,did = doc)
        attendstomodel.save()
        return render(request,'hospital/patient_add_doctors.html',{'Message':'Added Successfully'})
    else:
        add_doctor_form = forms.AddDoctorForm()
        # patients=models.Patient.objects.all().filter(user_id__in=patientid)
        return render(request,'hospital/patient_add_doctors.html',{'add_doctor_form':add_doctor_form})

#### PATIENT APPOINTMENTS ####
def patient_appointments(request):
    return render(request,'hospital/patient_appointments.html')

def patient_view_appointments(request):
    patient=Patient.objects.get(patientId=request.user.id)
    appointments = models.Appointment.objects.filter(patientId = patient)
    return render(request,'hospital/patient_view_appointments.html',{'patient':patient,'appointments':appointments})

def patient_add_appointments(request):
    if request.method=='POST':
        add_appointment_form  = forms.AddAppointmentForm(request.POST)
        did = request.POST['doctorId']
        date = request.POST['date']
        timing = request.POST['timing']
        patientId = models.Patient.objects.get(patientId = request.user.id)
        doctorId = models.Doctor.objects.get(id = did)
        print(doctorId.clinicname)
        receptionistid = models.Receptionist.objects.get(clinicname = doctorId.clinicname )

        appointmentmodel = Appointment.objects.create(patientId = patientId,doctorId = doctorId, receptionistid = receptionistid,date = date,timing = timing)
        appointmentmodel.save()
        return render(request,'hospital/patient_book_appointments.html',{'Message':'Added Successfully'})
    else:
        add_appointment_form = forms.AddAppointmentForm()
        # patients=models.Patient.objects.all().filter(user_id__in=patientid)
        return render(request,'hospital/patient_book_appointments.html',{'add_appointment_form':add_appointment_form})

def patient_prescription_view(request, p):
    print(p)
    a = Appointment.objects.filter(appointmentId=p).first()
    print(a)

    x = PrescribedIn.objects.filter(aid=a).first()
    print(x)
    pk = x.prescriptionid.prescriptionid
    print(pk)
    symptom=Symptoms.objects.filter(prescriptionid=x.prescriptionid)
    medicaltest=MedicalTest.objects.filter(prescriptionid=x.prescriptionid)
    medicines = MedicinesPrescribed.objects.filter(prescriptionid=x.prescriptionid)
    return render(request,'hospital/patient_prescription_view.html',{'symptoms':symptom , 'pk':pk,'medicaltest':medicaltest
                                                                        ,'medicines':medicines})


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

def admin_appointment(request):
    #print(receptionistid__receptionistid)
    appointment = Appointment.objects.filter(receptionistid__receptionistid = request.user.id, is_approved=False)
    #print(appointment)
    return render(request,'hospital/admin_approve_appointment.html', {'appointment':appointment})

def admin_patient(request):
    rid = Receptionist.objects.get(receptionistid = request.user.id )
    clinic = rid.clinicname
    doctor = Doctor.objects.filter(clinicname = clinic)
    ls = []
    for i in doctor:
        patient = AttendsTO.objects.filter(did = i)
        for j in patient:
            ls.append(j)
    print(ls)
    test=[]
    phoneno=[]
    for i in patient:
         temp = PhoneNumber.objects.all().filter(user__id = i.pid.user.id)
         for i in temp:
             test.append(i.phone)
         phoneno.append(test)
    patient = zip(ls,phoneno)

    return render(request, 'hospital/admin_view_patient.html', {'patient':patient})

def admin_doctor(request):
    rid = Receptionist.objects.get(receptionistid = request.user.id )
    clinic = rid.clinicname
    doctor = Doctor.objects.filter(clinicname = clinic)

    return render(request, 'hospital/admin_view_doctor.html', {'doctor':doctor})

def admin_scheduled_appointment(request):
    appointment = Appointment.objects.filter(receptionistid__receptionistid = request.user.id, is_approved=True)
    return render(request,'hospital/admin_scheduled_appointment.html', {'appointment':appointment})
def approve(request, pk):

    appointment1 = Appointment.objects.get(appointmentId = pk)
    appointment1.is_approved = True
    appointment1.save()
    appointment = Appointment.objects.filter(receptionistid__receptionistid = request.user.id, is_approved=False, is_disapproved = False)

    return render(request,'hospital/admin_approve_appointment.html', {'appointment':appointment})

def disapprove(request, pk):
    appointment1 = Appointment.objects.get(appointmentId = pk)
    appointment1.reasonOfDisapproval = request.POST['reasonOfDisapproval']
    appointment1.is_disapproved = True
    appointment1.save()

    appointment = Appointment.objects.filter(receptionistid__receptionistid = request.user.id, is_approved=False, is_disapproved = False)

    return render(request,'hospital/admin_approve_appointment.html', {'appointment':appointment})

    #return render(request,'hospital/aboutsus.html')
