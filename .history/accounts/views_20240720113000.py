from django.shortcuts import render, redirect,reverse,get_object_or_404
from .forms import LearnerForm, LearnerLoginForm, VerifyForm,AddManyTeacherForm,AddOneTeacherForm,TeacherLoginForm,PassForm,ProfileForm,SubscriptionForm
from django.contrib.auth import login, authenticate, get_user_model,logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib import messages
from .models import CustomUser
import random,string,requests,json,http.client
from datetime import datetime, timedelta
from django.contrib.auth.hashers import make_password,check_password
from courses.models import Matter, Course, Evaluation, Tutorial, Challenge,Transaction
from .constants import LEARNER_FACULTY, LEARNER_LEVEL,TEACHER_MATTER
from django.http import JsonResponse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.core.cache import cache

def famous_404(request, exception):
    return render(request, 'accounts/404.html', status=404)


def learner_signup(request):
    if request.method == 'POST':
        form = LearnerForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('learner_email')
            phone = form.cleaned_data.get('learner_phone')
            code = random.randint(100000, 999999)
            expiration_time = datetime.now() + timedelta(minutes=3)
            request.session['verification_code'] = code
            request.session['code_expiration'] = expiration_time.isoformat()
            request.session['user_data'] = form.cleaned_data

            if CustomUser.objects.filter(learner_email=email).exists():
                form.add_error('learner_email', 'Cet email est déjà utilisé.')
            elif CustomUser.objects.filter(learner_phone=phone).exists():
                form.add_error('learner_phone', 'Ce numéro de téléphone est déjà utilisé.')

            send_mail(
                'Votre code de vérification',
                f'Voici votre code de vérification, svp ne le communiquez à personne : {code}',
                'arsenenikiema685@gmail.com',
                [email],
                fail_silently=False,
            )
            return redirect('verify_email')  # Utilisez le nom d'URL ici
    else:
        form = LearnerForm()
    return render(request, 'accounts/inscription.html', {'form': form})



def verify_email(request):

    if request.method == 'POST':
        verify_form = VerifyForm(request.POST)
        if verify_form.is_valid():
            code = verify_form.cleaned_data.get('code')
            expiration_time = datetime.fromisoformat(request.session.get('code_expiration'))
            
            if datetime.now() > expiration_time:
                verify_form.add_error('code', 'Le code de vérification a expiré.')
            elif code == request.session.get('verification_code'):
                # Code de vérification correct, vérifier l'existence de l'email et du téléphone
                user_data = request.session.get('user_data')
                # if CustomUser.objects.filter(learner_email=user_data['learner_email']).exists():
                #     verify_form.add_error('learner_email', 'Cet email est déjà utilisé.')
                # elif CustomUser.objects.filter(learner_phone=user_data['learner_phone']).exists():
                #     verify_form.add_error('learner_phone', 'Ce numéro de téléphone est déjà utilisé.')
                # else:
                    # is_first_cycle =True
                    # if user_data["learner_level"] in second_cycle:
                    #     is_first_cycle =False
        
                    # Créer l'utilisateur ici
                user = CustomUser.objects.create_user(
                    learner_email=user_data['learner_email'],
                    learner_phone=user_data['learner_phone'],
                    password=user_data['password1'],
                    first_name=user_data['first_name'],
                    last_name=user_data['last_name'],
                    learner_level=user_data['learner_level'],
                    learner_subscription=user_data['learner_subscription'],
                )
                del request.session['verification_code']
                del request.session['user_data']
                del request.session['code_expiration']
                return redirect('learner_home')
            else:
                verify_form.add_error('code', 'Code de vérification incorrect.')
    else:
        verify_form = VerifyForm()

    return render(request, 'accounts/verify_email.html', {'verify_form': verify_form})

def regenerate_verification_code(request):
    if 'user_data' in request.session:
        user_data = request.session['user_data']
        verification_code = random.randint(100000, 999999)
        expiration_time = datetime.now() + timedelta(minutes=3)
        request.session['verification_code'] = verification_code
        request.session['code_expiration'] = expiration_time.isoformat()

        send_mail(
            'Votre nouveau code de vérification',
            f'Voici votre nouveau code de vérification, svp ne le communiquez à personne : {verification_code}',
            'arsenenikiema685@gmail.com',
            [user_data['learner_email']],
            fail_silently=False,
        )
        return redirect('verify_email')
    else:
        return redirect('learner_signup')

def learner_login(request):
    if request.method == 'POST':
        cache.clear()
        learner_login_form = LearnerLoginForm(request.POST)
        if learner_login_form.is_valid():
            user = learner_login_form.get_user()
            if user is not None:
                login(request, user)
                return redirect('learner_home')
            else:
                learner_login_form.add_error(None, "Identifiants invalides")
    else:
        learner_login_form = LearnerLoginForm()
    
    return render(request, 'accounts/learner_login.html', {'learner_login_form': learner_login_form})






    
def failled_subscribing(request):
    return render (request,'accounts/failled_event.html')



@login_required
def learner_logout(request):
    cache.clear()
    logout(request)
    return redirect('learner_login')





        #####################################################################################
        #                                                                                   # 
        #                      View for teacher                                             #
        #                                                                                   #
        #####################################################################################



@login_required
def teacher_logout(request):
    cache.clear()
    logout(request)
    return redirect('teacher_login')



def teacher_login(request):
    if request.method == 'POST':
        cache.clear()
        teacher_login_form = TeacherLoginForm(request.POST)
        if teacher_login_form.is_valid():
            user = teacher_login_form.get_user()
            if user is not None:
                login(request, user)
                return redirect('teacher_home')
            else:
                teacher_login_form.add_error(None, "Identifiants invalides")
    else:
        teacher_login_form = TeacherLoginForm()
    
    return render(request, 'accounts/teacher_login.html', {'teacher_login_form': teacher_login_form})


def teacher_signup(request):
    return render(request,"accounts/teacher_signup.html")



def success(request):
    return render(request,"accounts/success_event.html")


def signup_one_teacher(request):
    if request.method == 'POST':
        teacher_one_form = AddOneTeacherForm(request.POST)
        if teacher_one_form.is_valid():
            teacher_register = teacher_one_form.cleaned_data['teacher_register']
            email = teacher_one_form.cleaned_data['learner_email']
            
            # Vérifier l'existence de l'utilisateur sans lever une exception 404
            exists = CustomUser.objects.filter(teacher_register=teacher_register, learner_email=email).exists()
            if exists:
                teacher_one_form.add_error(None, "Enseignant déjà existant")
            else:
                user = CustomUser.objects.create_user(
                    first_name=teacher_one_form.cleaned_data['first_name'],
                    learner_email=email,
                    teacher_register=teacher_register,
                    teacher_matter=teacher_one_form.cleaned_data["teacher_matter"],
                    password=teacher_one_form.cleaned_data['password1'],
                    is_learner=False
                )
                send_mail(
                    f'Hello, {user.first_name} {user.last_name}',
                    f'Vos informations de connexion à LearnSpace: \nMatricule : {teacher_register} \nPassword : {teacher_one_form.cleaned_data["password1"]}',
                    'arsenenikiema685@gmail.com',
                    [email],
                    fail_silently=False,
                )
                return redirect("teacher_login")
    else:
        teacher_one_form = AddOneTeacherForm()
    return render(request, "accounts/inscription_one_teacher.html", {"teacher_one_form": teacher_one_form})



def teacher_exists(email, register):
    try:
        get_object_or_404(CustomUser, learner_email=email, teacher_register=register)
        return True
    except:
        return False

def signup_many_teachers(request):
    if request.method == 'POST':
        teacher_many_form = AddManyTeacherForm(request.POST)
        if teacher_many_form.is_valid():
            teacher_name = teacher_many_form.cleaned_data['first_name']
            teacher_register = teacher_many_form.cleaned_data['teacher_register']
            teacher_email = teacher_many_form.cleaned_data['teacher_email']
            teacher_matter = teacher_many_form.cleaned_data['teacher_matter']
            teacher_number = teacher_many_form.cleaned_data['teacher_number']

            if teacher_number < 1 or teacher_number > 15:
                teacher_many_form.add_error("teacher_number", "Valeur hors de la plage ou incorrecte")
            else:
                for i in range(teacher_number):
                    unique_suffix = random_string(5)
                    unique_teacher_name = f"{teacher_name}{unique_suffix}"
                    unique_teacher_register = f"{teacher_register}{unique_suffix}"
                    unique_teacher_password = f"{random_string(2)}{random_string(8)}{i}"
                    unique_teacher_email = f"{teacher_email}{random_string(2)}{i}@gmail.com"
                    
                    if teacher_exists(unique_teacher_email, unique_teacher_register):
                        continue
                    else:
                        CustomUser.objects.create_user(
                            first_name=unique_teacher_name,
                            password=unique_teacher_password,
                            teacher_matter=teacher_matter,
                            learner_email=unique_teacher_email,
                            teacher_register=unique_teacher_register,
                            is_learner=False
                        )
                messages.success(request, "Enregistrement de plusieurs enseignants réussi.")
                return redirect('teacher_home')
        else:
            messages.error(request, "Formulaire invalide. Veuillez vérifier les informations fournies.")
    else:
        teacher_many_form = AddManyTeacherForm()

    return render(request, "accounts/inscription_many_teachers.html", {"teacher_many_form": teacher_many_form})



def random_string(length=5):
    return ''.join(random.choices(string.ascii_lowercase, k=length))



        #####################################################################################
        #                                                                                   # 
        #                      View learners                                                #
        #                                                                                   #
        #####################################################################################



@login_required
def user_progress(request):
    progress, created = UserProgress.objects.get_or_create(user=request.user)
    return render(request, 'accounts/progress.html', {'progress': progress})

@login_required
def update_progress(request):
    if request.method == 'POST':
        progress, created = UserProgress.objects.get_or_create(user=request.user)
        new_progress = int(request.POST.get('progress', 0))
        progress.progress = new_progress
        progress.save()
        return JsonResponse({'progress': new_progress})
    return JsonResponse({'error': 'Invalid request'}, status=400)


def user_profile(request):
    if request.method=='POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            learner_email = user.cleaned_data["learner_email"]
            learner_phone = user.cleaned_data["learner_phone"]    
            if ((user.learner_email == learner_email ) and (user.learner_phone == learner_phone)):
                user.learner_email = learner_email
                user.learner_phone = learner_phone
                user.save()
            else:
                form.add_error(None,"Identifiants dejà existants")
    else:
        form = ProfileForm()
    return render(request,"accounts/profile.html",{"form":form})

def edit_password(request):
    if request.method == 'POST':
        form = PassForm(request.POST)
        if form.is_valid():
            learner_email = form.cleaned_data['learner_email']
            learner_phone = form.cleaned_data['learner_phone']
            user = request.user
            if ((learner_email == user.learner_email) and (learner_email == user.learner_email)):
                return redirect('help_reinitialize')
            else:
                form.add_error(None,"Identifiants introuvables")
        else:
            form = PassForm()
    return render(request,"accounts/edit_password.html",{"form":form})


def help(request):
    return render(request,"accounts/help.html")

def help_create(request):        
    return render(request,"accounts/help_create.html")


def help_reinitialize(request):
    if request.method =='POST' :
        form = PassForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['learner_email']
            password_1 = form.cleaned_data['password1']
            password_2 = form.cleaned_data['password1']
            
            if password_1 != password_2:
                form.add_error("password1","Les mots de passe ne correspondent pas")
            else:
                user =request.user
                user.password = make_password(password1)
                user.save()
                return redirect('learner_login')
    else:
        form=PassForm()
    return render(request,"accounts/help_reinitialize.html",{"form":form})

def help_subscribing(request):
    return render(request,"accounts/help_subscribing.html")



        #####################################################################################
        #                                                                                   # 
        #                      View for admin                                               #
        #                                                                                   #
        #####################################################################################


def forgot_verify(request):
    return render(request,"accounts/forgot_verify.html")



from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import SubscriptionForm  # Assurez-vous d'avoir ce formulaire

@login_required
@csrf_protect
def choose_subscription(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            plan = form.cleaned_data['plan']
            montant = 0
            
            if plan.lower() == 'premium':
                montant = 150
            elif plan.lower() == 'standard':
                montant = 100
            else:
                montant = 0  # Free plan

            request.session['chosen_plan'] = plan
            return redirect('payment', montant=montant)
    else:
        form = SubscriptionForm()
    
    return render(request, 'accounts/subscription.html', {'form': form})


@login_required
def payment(request, montant):
    if Transaction.objects.filter(learner=request.user.id).exists():
        Transaction.objects.get(learner=request.user.id).delete()
        
    transac_id = f'TRANS{random.randint(0, 9999)}{datetime.now().strftime("%Y%m%d%H%M%S")}'
    learner = request.user
    response = redirection_payement(transac_id, montant)

    if response.get('response_code') == '00':
        token = response.get("token")
        redirect_url = response.get("response_text")

        Transaction.objects.create(
            learner=learner,
            transId=transac_id,
            status="pending",
            token=token 
        )

        request.session['transaction_id'] = transac_id
        return redirect(redirect_url)
    else:
        return render(request, 'accounts/cancel.html')


def redirection_payement(trans_id, montant):
    url = "https://app.ligdicash.com/pay/v01/redirect/checkout-invoice/create"
    headers = {
        "Apikey": "MAGPMLT3QFJLIPUDN",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZF9hcHAiOjE1MDA5LCJpZF9hYm9ubmUiOjg5OTQyLCJkYXRlY3JlYXRpb25fYXBwIjoiMjAyNC0wNC0wOCAwODozMjoyNCJ9.NRcyHfFO8OyaXOaklZ2DJ2Arf-gV8OXGfMIELQzdw88",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "commande": {
            "invoice": {
                "items": [
                    {
                        "name": "abonnement",
                        "description": "abonnement a LearneSpace",
                        "quantity": 1,
                        "unit_price": montant,
                        "total_price": montant
                    }
                ],
                "total_amount": montant,
                "devise": "XOF",
                "description": "abonnement a LearnSpace",
                "customer": "",
                "customer_firstname": "Prenom du client",
                "customer_lastname": "Nom du client",
                "customer_email": "devseniors2024@gmail.com"
            },
            "store": {
                "name": "webapp",
                "website_url": "https://appweb.com"
            },
            "actions": {
                "cancel_url": "http://127.0.0.1:8000/payment/cancel/",
                "return_url": "http://localhost:8000/payment/success/",
                "callback_url": "http://localhost:8000/payment/callback/"
            },
            "custom_data": {
                "transaction_id": trans_id
            }
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    return response.json()


@login_required
def success(request):
    transaction_id = request.session.get('transaction_id')
    if transaction_id:
        payment = Transaction.objects.get(transId=transaction_id)
        payment_data = check_payment_status(payment.token)

        if payment_data.get("status") == "completed":
            payment.status = "completed"
            payment.save()

            # Mettre à jour l'abonnement de l'utilisateur
            chosen_plan = request.session.get('chosen_plan')
            user = request.user
            user.learner_subscription = chosen_plan
            user.save()

            return redirect('learner_home')
        else:
            return redirect('cancel')
    else:
        messages.error(request, 'Erreur de transaction. Veuillez réessayer.')
        return redirect('learner_home')


@login_required
def cancel(request):
    return render(request, 'accounts/cancel.html')

@login_required
def info_payement(request):
    return render(request, 'accounts/payment.html')

def callback(request):
    pass

"""
@login_required
def choose_subscription(request):
    if request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            montant=100
            learner_subscription = request.user.learner_subscription
            plan = form.cleaned_data['plan']
            if (learner_subscription == 'PREMIEUM'):
                montant=150
                return montant
            elif(learner_subscription=="STANTARD"):
                return montant
            #Subscription.objects.update_or_create(user=request.user, defaults={'plan': plan})
            return redirect('payement',montant)
    else:
        form = SubscriptionForm()
    
    return render(request, 'subscription.html', {'form': form})


@login_required
def payment(request,montant):
    if Transaction.objects.filter(learner=request.user.id).exists():
        Transaction.objects.get(learner=request.user.id).delete()
    transac_id = f'TRANS{random.randint(0, 9999)}{datetime.now().strftime("%Y%m%d%H%M%S")}'
    learner = request.user
    response = redirection_payement(transac_id)


    if response.get('response_code') == '00':
        token = response.get("token")
        redirect_url = response.get("response_text")

        Transaction.objects.create(
            learner=learner,
            transId=transac_id,
            status="pending",
            token=token 
        )

        request.session['transaction_id'] = transac_id
        return redirect(redirect_url,montant)
    else:
        
        return render(request, 'accounts/cancel.html')


def redirection_payement(trans_id):
    url = "https://app.ligdicash.com/pay/v01/redirect/checkout-invoice/create"
    headers = {
        "Apikey": "MAGPMLT3QFJLIPUDN",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZF9hcHAiOjE1MDA5LCJpZF9hYm9ubmUiOjg5OTQyLCJkYXRlY3JlYXRpb25fYXBwIjoiMjAyNC0wNC0wOCAwODozMjoyNCJ9.NRcyHfFO8OyaXOaklZ2DJ2Arf-gV8OXGfMIELQzdw88",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    data = {
        "commande": {
            "invoice": {
                "items": [
                    {
                        "name": "abonnement",
                        "description": "abonnement a LearneSpace",
                        "quantity": 1,
                        "unit_price": montant,
                        "total_price": montant
                    }
                ],
                "total_amount": montant,
                "devise": "XOF",
                "description": "abonnement a LearnSpace",
                "customer": "",
                "customer_firstname": "Prenom du client",
                "customer_lastname": "Nom du client",
                "customer_email": "devseniors2024@gmail.com"
            },
            "store": {
                "name": "webapp",
                "website_url": "https://appweb.com"
            },
            "actions": {
                "cancel_url": "http://127.0.0.1:8000/payment/cancel/",
                "return_url": "http://localhost:8000/payment/success/",
                "callback_url": "http://localhost:8000/payment/callback/"
            },
            "custom_data": {
                "transaction_id": trans_id
            }
        }
    }
    response = requests.post(url, headers=headers, data=json.dumps(data), verify=False)
    return response.json()

@login_required
def cancel(request):
    return render(request, 'accounts/cancel.html')

@login_required
def info_payement(request):
    return render(request, 'accounts/payment.html')

@login_required
def success(request):
    transaction_id = request.session.get('transaction_id')
    if transaction_id:
        payment = Transaction.objects.get(transId=transaction_id)
        payment_data = check_payment_status(payment.token)

        if payment_data.get("status") == "completed":  
            payment.status = "completed"
            payment.save()

            return redirect('accounts/learner_home')
        else:
            return redirect('accounts/cancel')
    else:
        messages.error(request, 'Erreur de transaction. Veuillez réessayer.')
        return redirect('accounts/learner_home')
    
def check_payment_status(token):
    url = f"https://app.ligdicash.com/pay/v01/redirect/checkout-invoice/confirm/?invoiceToken={token}"
    headers = {
        "Apikey": "MAGPMLT3QFJLIPUDN",
        "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZF9hcHAiOjE1MDA5LCJpZF9hYm9ubmUiOjg5OTQyLCJkYXRlY3JlYXRpb25fYXBwIjoiMjAyNC0wNC0wOCAwODozMjoyNCJ9.NRcyHfFO8OyaXOaklZ2DJ2Arf-gV8OXGfMIELQzdw88",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as errh:
        return {"error": "HTTP Error", "message": str(errh)}
    except requests.exceptions.RequestException as err:
        return {"error": "Request Exception", "message": str(err)}



def callback(request):
    pass"""

