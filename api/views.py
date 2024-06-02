from django.shortcuts import render, redirect
from .forms import RegisterForm, LoginForm, NewProperty, UpdateProperty
from .models import users_collection, properties_collection, applications_collection
import bson
from datetime import datetime

# Create your views here.

def landing(request):
    return render(request, 'landing.html')

def login(request):
    error=''
    data = {}
    isLogged = False
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            try:
                data = users_collection.find_one({'email': email})
                if data.get('password') == password:
                    data['userId'] = str(data['_id'])
                    isLogged = True
                
                else:
                    form = LoginForm()
                    error = 'Wrong credientials. Please try again.'
                    
            except:
                form = LoginForm()
                error = 'User not found!! Please try again.'
        else:
            form = LoginForm()
            error = 'Wrong credientials. Please try again.'
    else:
        form = LoginForm()
    
    context = {'form': form, 'isLogged': isLogged, 'data': data, 'error': error}
    return render(request, 'login.html', context)

def register(request):
    error=''
    data = {}
    isLogged = False
    
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            usertype = form.cleaned_data['usertype']
            user = {"username": username, "email": email, "password": password, "usertype": usertype}
            result = users_collection.insert_one(user)
            isLogged = True
            data = {
            'userId': str(result.inserted_id),
            'username': username,
            'email': email,
            'password': password,
            'usertype': usertype
            }
            
        else:
            form = RegisterForm()
            error = 'Invalid form data. Please try again.'
    else:
        form = RegisterForm()
    
    context = {'form': form, 'isLogged': isLogged, 'data': data, 'error': error}
    return render(request, 'register.html', context)
    
    

def userHome(request):
    return render(request, 'user/loadHome.html')

def userHomeWithId(request, id):
    properties = [property for property in properties_collection.find() if property['status'] == 'Available']
    for property in properties:
        property['id'] = str(property['_id'])
    return render(request, 'user/home.html', {'properties': properties, 'id': id})

def applyProperty(request, propId, userId):
    prop_id = bson.ObjectId(propId)
    property = properties_collection.find_one({'_id': prop_id})
    
    user_id = bson.ObjectId(userId)
    user = users_collection.find_one({'_id': user_id})

    application = {"propertyId": propId, "ownerId": property['ownerId'], "ownerName": property['ownerName'], "carouselImage1": property['carouselImage1'], "carouselImage2": property['carouselImage2'], "carouselImage3": property['carouselImage3'], "description": property['description'], "rent": property['rent'], "deposit": property['deposit'], "agreementDuration": property['agreementDuration'], "address": property['address'], "applicantId": userId, "applicantName": user['username'], "applicantEmail": user['email'], "status": "Pending"}
    applications_collection.insert_one(application)
    
    properties_collection.update_one({"_id": prop_id}, {"$push": {"applicantsList": userId}})
    
    return redirect('/user-home')

def userApplications(request):
    return render(request, 'user/loadApplic.html')

def userApplicationsWithId(request, id):
    applications = [application for application in applications_collection.find({"applicantId": id})]
    for application in applications:
        application['id'] = str(application['_id'])
    applications.reverse()
    return render(request, 'user/applications.html', {'applications': applications})

def withdrawApplication(request, id):
    object_id = bson.ObjectId(id)
    application = applications_collection.find_one({'_id': object_id})
    prop_id = bson.ObjectId(application['propertyId'])
    properties_collection.update_one({"_id": prop_id}, {"$pull": {"applicantsList": application['applicantId']}})
    applications_collection.update_one({'_id': object_id}, {"$set": {"status": "Withdrawn"}})
    
    return redirect('/user-applications')

def vacateProperty(request, id):
    object_id = bson.ObjectId(id)
    properties_collection.update_one({"_id": object_id}, {"$set": {"tenantId": "", "tenantName": "", "rentStartDate": "", "status": "Available"}})
    
    return redirect('/user-rentals')

def userRentals(request):
    return render(request, 'user/loadRentals.html')

def userRentalsWithId(request, id):
    rentals = [rental for rental in properties_collection.find({"tenantId": id})]
    for rental in rentals:
        rental['id'] = str(rental['_id'])
    return render(request, 'user/rentals.html', {'rentals': rentals})




def ownerHome(request):
    return render(request, 'owner/loadHome.html')

def ownerHomeWIthId(request, id):
    properties = [property for property in properties_collection.find({"ownerId": id})]
    for property in properties:
        property['id'] = str(property['_id'])
    return render(request, 'owner/home.html', {'properties': properties})

def ownerApplications(request):
    return render(request, 'owner/loadApplic.html')

def ownerApplicationsWithId(request, id):
    applications = [application for application in applications_collection.find({"ownerId": id})]
    print(applications)
    for application in applications:
        application['id'] = str(application['_id'])
    applications.reverse()
    return render(request, 'owner/applications.html', {'applications': applications})

def approveApplication(request, id):
    object_id = bson.ObjectId(id)
    application = applications_collection.find_one({'_id': object_id})
    prop_id = bson.ObjectId(application['propertyId'])
    
    currentDateAndTime = datetime.now()
    
    properties_collection.update_one({"_id": prop_id}, {"$set": {"tenantId": application['applicantId'], "tenantName": application['applicantName'], "rentStartDate": str(currentDateAndTime), "status": "Rented"}})
    properties_collection.update_one({"_id": prop_id}, {"$pull": {"applicantsList": application['applicantId']}})
    applications_collection.update_one({'_id': object_id}, {"$set": {"status": "Approved"}})
    
    return redirect('/owner-applications')

def rejectApplication(request, id):
    object_id = bson.ObjectId(id)
    application = applications_collection.find_one({'_id': object_id})
    prop_id = bson.ObjectId(application['propertyId'])
    
    properties_collection.update_one({"_id": prop_id}, {"$pull": {"applicantsList": application['applicantId']}})
    applications_collection.update_one({'_id': object_id}, {"$set": {"status": "Rejected"}})
    
    return redirect('/owner-applications')


def newProperty(request):
    
    error=''
    if request.method == 'POST':
        form = NewProperty(request.POST)
        if form.is_valid():
 
            ownerId = form.cleaned_data['ownerId']
            ownerName = form.cleaned_data['ownerName']
            description = form.cleaned_data['description']
            carouselImage1 = form.cleaned_data['carouselImage1']
            carouselImage2 = form.cleaned_data['carouselImage2']
            carouselImage3 = form.cleaned_data['carouselImage3']
            rent = form.cleaned_data['rent']
            area = form.cleaned_data['area']
            deposit = form.cleaned_data['deposit']
            agreementDuration = form.cleaned_data['agreementDuration']
            availableFor = form.cleaned_data['availableFor']
            furnished = form.cleaned_data['furnished']
            address = form.cleaned_data['address']

            property = {"ownerId": ownerId, "ownerName": ownerName, "description": description, "carouselImage1": carouselImage1, "carouselImage2": carouselImage2, "carouselImage3": carouselImage3, "rent": rent, "area": area, "deposit": deposit, "agreementDuration": agreementDuration, "availableFor": availableFor, "furnished": furnished, "address": address, "tenantId": "", "tenantName": "", "rentStartDate": "", "status": "Available", "applicantsList": []}
            result = properties_collection.insert_one(property)
            
            return redirect('/owner-home')
            
        else:
            form = NewProperty()
            error = 'Please try again.'
    else:
        form = NewProperty()
        error = ''
    
    context = {'form': form, 'error': error}
    return render(request, 'owner/newProperty.html', context)


def updateProperty(request, id):
    
    error=''
    if request.method == 'POST':
        form = UpdateProperty(request.POST)
        if form.is_valid():
            
            object_id = bson.ObjectId(id)
            property = properties_collection.find_one({'_id': object_id})
 
            ownerId = form.cleaned_data['ownerId']
            ownerName = form.cleaned_data['ownerName']
            description = form.cleaned_data['description']
            carouselImage1 = form.cleaned_data['carouselImage1']
            carouselImage2 = form.cleaned_data['carouselImage2']
            carouselImage3 = form.cleaned_data['carouselImage3']
            rent = form.cleaned_data['rent']
            area = form.cleaned_data['area']
            deposit = form.cleaned_data['deposit']
            agreementDuration = form.cleaned_data['agreementDuration']
            availableFor = form.cleaned_data['availableFor']
            furnished = form.cleaned_data['furnished']
            address = form.cleaned_data['address']

            
            properties_collection.update_one({"_id": object_id}, {"$set": {"ownerId": ownerId, "ownerName": ownerName, "description": description, "carouselImage1": carouselImage1, "carouselImage2": carouselImage2, "carouselImage3": carouselImage3, "rent": rent, "area": area, "deposit": deposit, "agreementDuration": agreementDuration, "availableFor": availableFor, "furnished": furnished, "address": address}})
            
            
            return redirect('/owner-home')
            
        else:
            form = UpdateProperty()
            error = 'Please try again.'
    else:
        object_id = bson.ObjectId(id)
        property = properties_collection.find_one({'_id': object_id})
        if property is None:
            error = "Error in fetching property!!"
            form = UpdateProperty()
        else:
            form = UpdateProperty(initial={'ownerId': property['ownerId'],
                                            'ownerName': property['ownerName'],
                                            'description': property['description'],
                                            'carouselImage1': property['carouselImage1'],
                                            'carouselImage2': property['carouselImage2'],
                                            'carouselImage3': property['carouselImage3'],
                                            'rent': property['rent'],
                                            'area': property['area'],
                                            'deposit': property['deposit'],
                                            'agreementDuration': property['agreementDuration'],
                                            'availableFor': property['availableFor'],
                                            'furnished': property['furnished'],
                                            'address': property['address']})

    
    context = {'form': form, 'error': error}
    return render(request, 'owner/updateProperty.html', context)




def adminHome(request):
    
    properties = properties_collection.find()
    properties = [property for property in properties_collection.find()]
    
    for property in properties:
        property['id'] = str(property['_id'])
    
    return render(request, 'admin/home.html', {'properties': properties})

def adminApplications(request):
    properties = properties_collection.find()
    applications = [application for application in applications_collection.find()]
    
    for application in applications:
        application['id'] = str(application['_id'])
    
    return render(request, 'admin/applications.html', {'applications': applications})

def allUsers(request):
    users = users_collection.find()
    users = [user for user in users_collection.find()]
    
    for user in users:
        user['id'] = str(user['_id'])
    return render(request, 'admin/allUsers.html', {'users': users})


