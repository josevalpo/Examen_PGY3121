from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from store.models.customer import Customer
from django.views import View


class Signup (View):
    def get(self, request):
        return render (request, 'signup.html')

    def post(self, request):
        postData = request.POST
        first_name = postData.get ('firstname')
        last_name = postData.get ('lastname')
        phone = postData.get ('phone')
        email = postData.get ('email')
        password = postData.get ('password')
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Customer (first_name=first_name,
                             last_name=last_name,
                             phone=phone,
                             email=email,
                             password=password)
        error_message = self.validateCustomer (customer)

        if not error_message:
            print (first_name, last_name, phone, email, password)
            customer.password = make_password (customer.password)
            customer.register ()
            return redirect ('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render (request, 'signup.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "Por favor ingresar su nombre"
        elif len (customer.first_name) < 3:
            error_message = 'Su nombre debe tener, al menos, 3 letras'
        elif not customer.last_name:
            error_message = 'Por favor ingrese su apellido'
        elif len (customer.last_name) < 3:
            error_message = 'Su apellido debe tener, al menos, 3 letras'
        elif not customer.phone:
            error_message = 'Ingrese su número de teléfono'
        elif len (customer.phone) < 9:
            error_message = 'El número de teléfono debe tener 9 dígitos'
        elif len (customer.password) == 0:
            error_message = 'Debe ingresar una contraseña'
        elif len (customer.password) < 5:
            error_message = 'La contraseña debe tener, al menos, 5 caracteres'
        elif len (customer.email) < 10:
            error_message = 'Dirección de correo muy corta (debe ser de al menos 10 caracteres)'
        elif customer.isExists ():
            error_message = 'Correo ya registrado'
        # saving

        return error_message
