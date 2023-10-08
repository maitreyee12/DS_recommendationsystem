from django.shortcuts import render , redirect , HttpResponseRedirect
from django.contrib.auth.hashers import  check_password
from django.template import RequestContext
from store.models.customer import Customer
from django.views import View
from django.views.decorators.csrf import csrf_protect

class Login(View):
    return_url = None
    def get(self, request):
        print("GET LOGIN")
        Login.return_url = request.GET.get ('return_url')
        print(Login.return_url)
        return render (request, 'login.html')
    
    def post(self, request):
        csrfContext = RequestContext(request)
        email = request.POST.get ('email')
        password = request.POST.get ('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                print(customer)
                request.session['customer'] = customer.id
                request.session['customername'] = customer.first_name
                print(customer.first_name)
                if Login.return_url:
                    print(Login.return_url)
                    print("Login.return_url")
                else:
                    Login.return_url = None
                    return redirect ('homepage')
                    #return redirect (request , 'homepage' , {'customername' : custname} )
            else:
                error_message = 'Invalid !!'
        else:
                error_message = 'Invalid !!'
                    #return HttpResponseRedirect (Login.return_url)
        print(email, password)
        return render (request, 'login.html', {'error': error_message})
def logout(request):
    #request.session['customer'] = ""
    #request.session['customername']=""
    request.session.clear()
    return redirect('login')