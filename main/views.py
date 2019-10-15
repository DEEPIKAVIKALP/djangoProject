from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import UserAdminCreationForm, UserProfileForm, Address_detailsForm,User_form, ChangePassword, ForgotPassword
from django.contrib.auth import logout, authenticate, login
from django.utils import timezone
from .models import Product,Category,Cart,User,Address_details, Orders, OrderDetails, Shipper, UserProfile
from django.contrib import messages 
from django.contrib.auth.forms import AuthenticationForm 
import time, calendar
from django.contrib.auth.hashers import check_password, make_password


#import  django.contrib.auth.hashers

#from . models import Supplier
# Create your views here.
def register(request):

	if request.method == "POST":
	  	form = UserAdminCreationForm(request.POST)
	  	form_profile = UserProfileForm(request.POST)
	  	if form.is_valid() and form_profile.is_valid():
	  		user = form.save()

	  		profile = form_profile.save(commit=False)
	  		profile.user = user
	  		profile.date_entered = timezone.now()
	  		profile.save()

	  		#email = form.cleaned_data.get('username')
	  		login(request, user)
	  		return redirect("main:homepage")

	  	else:
	  		
	  		return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form, "form_profile":form_profile})

	form = UserAdminCreationForm
	form_profile = UserProfileForm
	return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form, "form_profile":form_profile})

def login_requested(request):
	if request.method == 'POST':
		form = AuthenticationForm(request=request, data=request.POST) 	
		if form.is_valid():
			email = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(email=email, password=password)
			 
			if user is not None:
				login(request, user)
				messages.success(request, f"You are now logged in as {email}")
				cart_count=0
				if request.user.is_authenticated :
					cart_count=Cart.objects.all().filter(email=User.objects.get(email=request.user.email)).count()
				return render(request = request,
                  template_name = "main/index.html",
                  context={"user":user,'cart_count':cart_count})
				#redirect("main:homepage")
			else:
				messages.error(request,f"Invalid email or password")
				return render(request = request,
                  template_name = "main/login.html",
                  context={"form":form})
                  #context={"error_messages":"Invalid email or password"})
		else:
			messages.error(request,f"Invalid email or password")
			return render(request = request,
                  template_name = "main/login.html",
                  context={"form":form})
                  #context={"error_messages":"Invalid email or password"})


	form = AuthenticationForm()
	return render(request = request,
				  template_name = "main/login.html",
				  context={"form":form})

def logout_requested(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("main:homepage")

def homepage(request):
	cart_count=0
	if request.user.is_authenticated :
		cart_count=Cart.objects.all().filter(email=User.objects.get(email=request.user.email)).count()
		return render(request = request,
				  template_name = "main/index.html",
				  context = {"cart_count": cart_count}
				 )
	else:
		return render(request = request,
				  template_name = "main/index.html",
				  #context = {"cart_count": cart_count}
				 )

def products(request):
	all_products=Product.objects.all()
	cart_count=0
	if request.user.is_authenticated :
		cart_count=Cart.objects.all().filter(email=User.objects.get(email=request.user.email)).count()

	return render(request = request,
				  template_name = "main/products.html",
				  context = {'all_products':all_products,
				  			 'cart_count':cart_count}
				 )
def shop(request):
	all_products=Product.objects.all()    
	
	cart_count=0
	if request.user.is_authenticated :
		cart_count=Cart.objects.all().filter(email=User.objects.get(email=request.user.email)).count()
	

	return render(request = request,
				  template_name = "main/shop.html",
				  context = {'all_products':all_products,
				  'cart_count':cart_count}
				 )

def cart(request):
	all_items=Cart.objects.all().filter(email=User.objects.get(email=request.user.email))
	
	cart_count=0
	if request.user.is_authenticated :
		cart_count=Cart.objects.all().filter(email=User.objects.get(email=request.user.email)).count()
	
	return render(request = request,
				  template_name = "main/cart.html",
				  context = {'all_items':all_items,
				  'cart_count':cart_count}
				 )
#'item_products_id':item_products_id,'matched_items':products
def item_details(request,product_id):
		product=Product.objects.get(pk=product_id)
		out_of_stock=False
		discount=Product.objects.get(product_id=product_id).discount #10
		mrp=Product.objects.get(product_id=product_id).mrp
		price=mrp-(discount/100)*mrp
		price=round(price,2)

		cart_count=0
		if request.user.is_authenticated :
			cart_count=Cart.objects.all().filter(email=User.objects.get(email=request.user.email)).count()
	
		if product.units_in_stock == 0:
			out_of_stock=True

		return render(request = request,
					  template_name = "main/shop-single.html",
					  context = {"product_id": product_id,'product':product,'price':price,'out_of_stock':out_of_stock,
					  'cart_count':cart_count}
					 )

def product_category(request,slug):
	categories = [c.category_name for c in Category.objects.all()]
	cart_count=0
	if request.user.is_authenticated :
		cart_count=Cart.objects.all().filter(email=User.objects.get(email=request.user.email)).count()
	
	if slug in categories:
		#return HttpResponse(f"{slug} is a category")
		matched_products=Product.objects.filter(category_id__category_name=slug)  #add oos filter
		return render(request = request,
				  template_name = "main/product_category.html",
				  context = {"matched_products": matched_products,
				  			"slug":slug,
				  			'cart_count':cart_count})
	else:
		return HttpResponse(f"'{slug} {str(categories[0])}' does not correspond to anything we know of!")





	
def register(request):

	if request.method == "POST":
	  	form = UserAdminCreationForm(request.POST)
	  	form_profile = UserProfileForm(request.POST)
	  	if form.is_valid() and form_profile.is_valid():
	  		user = form.save()

	  		profile = form_profile.save(commit=False)
	  		profile.user = user
	  		#profile.date_entered = timezone.now()
	  		profile.save()

	  		#email = form.cleaned_data.get('username')
	  		login(request, user)
	  		return redirect("main:homepage")

	  	else:
	  		
	  		return render(request = request,
                          template_name = "main/register.html",
                          context={"form":form, "form_profile":form_profile})

	form = UserAdminCreationForm
	form_profile = UserProfileForm
	return render(request = request,
                  template_name = "main/register.html",
                  context={"form":form, "form_profile":form_profile})

def Add_To_Cart(request,quantity,product_id):
	#e={{user.email}}
	if request.user.is_authenticated:
		
		#e=request.user.email
		#User.objects.get(email=request.user.email)
		
		count = Cart.objects.filter(email=User.objects.get(email=request.user.email), product_id=product_id).count()

		if count:
			cart_exist = Cart.objects.get(email=User.objects.get(email=request.user.email), product_id=product_id)
			cart_exist.quantity=cart_exist.quantity + quantity
			
			if cart_exist.quantity <= cart_exist.product_id.units_in_stock:
				discount=Product.objects.get(product_id=product_id).discount
				mrp=Product.objects.get(product_id=product_id).mrp
				price=(mrp-(discount/100)*mrp)*cart_exist.quantity
				cart_exist.price=price
				cart_exist.save()
				messages.success(request, f"Successfully added to Cart")
			else:
				messages.error(request, f"This much quantity isn't in stock")

		else:	
			prod=Product.objects.get(product_id=product_id)
			if quantity <= prod.units_in_stock:
				discount=Product.objects.get(product_id=product_id).discount #10
				mrp=Product.objects.get(product_id=product_id).mrp
				price=(mrp-(discount/100)*mrp)*quantity
				value_inserted = Cart(email=User.objects.get(email=request.user.email), product_id=Product.objects.get(product_id=product_id),price=price,quantity=quantity)
				value_inserted.save()
				messages.success(request, f"Successfully added to Cart")
			else:
				messages.error(request, f"This much quantity isn't in stock")
	else:
		messages.error(request,f"Please login to add to cart")		
	
	a="/shop/"+str(product_id)+"/"
	
   #need to add messages here in case user is not authenticated

	return redirect(a)

def cart_item_remove(request,cart_id):
	Cart.objects.filter(cart_id=cart_id).delete()
	all_items=Cart.objects.all().filter(email=User.objects.get(email=request.user.email))
	return redirect('/cart/')
	#return render(request = request,
	#			  template_name = "main/cart.html",
	#			  context = {'all_items':all_items}
	#			 )
def update_cart_quantity(request,cart_id,quantity):
	a=Cart.objects.get(cart_id=cart_id)
	
	if a.product_id.units_in_stock >= quantity:
		a.quantity=quantity
		discount=a.product_id.discount
		mrp=a.product_id.mrp 
		a.price=(mrp-(discount/100)*mrp)*quantity
		a.save()

	else:
		messages.error(request, f"This much quantity isn't in stock")
	return redirect('/cart/')

def checkout(request):

	cart_count=0
	if request.user.is_authenticated :
		cart_count=Cart.objects.all().filter(email=User.objects.get(email=request.user.email)).count()
 		

	if request.method == "POST":
	  	form = Address_detailsForm(request.POST)
	  	
	  	if form.is_valid():
	  		address_details = form.save(commit=False)
	  		address_details.email = User.objects.get(email=request.user.email)
	  		address_details.save()

	  		return redirect("main:checkout")

	  	else:
	 		
			
	  		return render(request = request,
                  template_name = "main/checkout.html",
                  context={"items":items,"total":total,"address_details":address_details,"form":address_form,'cart_count':cart_count})



	address_form = Address_detailsForm
	items=Cart.objects.all().filter(email=User.objects.get(email=request.user.email))
	address_details=Address_details.objects.all().filter(email=User.objects.get(email=request.user.email)).order_by('-address_id')
	#prices = [c.price for c in items]
	total=0
	for cart in items:
		if cart.product_id.units_in_stock == 0:
			Cart.objects.all().filter(email=User.objects.get(email=request.user.email),cart_id=cart.cart_id).delete()
			messages.error(request,f"Cart updated due to unavailability")
			count=Cart.objects.all().filter(email=User.objects.get(email=request.user.email)).count()
			if count==0:
				return redirect("../cart")
			
		elif cart.product_id.units_in_stock < cart.quantity:
			cart.quantity=cart.product_id.units_in_stock
			discount=cart.product_id.discount
			mrp=cart.product_id.mrp 
			cart.price=(mrp-(discount/100)*mrp)*cart.quantity
			cart.save()
		
	items=Cart.objects.all().filter(email=User.objects.get(email=request.user.email))
	for item in items:
		total=total+(item.price)


	cart_count=0
	if request.user.is_authenticated :
		cart_count=Cart.objects.all().filter(email=User.objects.get(email=request.user.email)).count()
	
	items=Cart.objects.all().filter(email=User.objects.get(email=request.user.email))
	return render(request = request,
                  template_name = "main/checkout.html",
                  context={"items":items,"total":total,"address_details":address_details,"form":address_form,'cart_count':cart_count})


def placeorder(request, address_id):

	address = Address_details.objects.get(address_id=address_id)
	items=Cart.objects.all().filter(email=User.objects.get(email=request.user.email))
	#address_details=Address_details.objects.all().filter(email=User.objects.get(email=request.user.email))
	#prices = [c.price for c in items]
	total=0
	for p in items:
		total=total+(p.price)

	cart_count=0
	if request.user.is_authenticated :
		cart_count=Cart.objects.all().filter(email=User.objects.get(email=request.user.email)).count()
	
	return render(request = request,
                  template_name = "main/placeorder.html",
                  context={"address":address,"items":items,"total":total,'cart_count':cart_count}
                )

def thankyou(request, address_id, payment_mode):
	address = Address_details.objects.get(address_id=address_id)
	items=Cart.objects.all().filter(email=User.objects.get(email=request.user.email))
	total=0
	orderid=""
	ship_date=timezone.now()
	for p in items:
		total=total+(p.price)
	if items:
		
		for item in items:
			if item.product_id.units_in_stock < item.quantity or item.product_id.units_in_stock == 0 :
				messages.error(request,f"Few items in your cart are currently out of stock. Please check the quantities again")
				loc='../../../cart/'
				return redirect (loc)

		max_cart=items.order_by('cart_id')[0]
		max_product=items.order_by('product_id')[0]

		orderid="OD"+str(calendar.timegm(time.gmtime()))+str(max_product)+str(max_cart)
		
		ship_date=timezone.now()+timezone.timedelta(days=1)
		
		shipper_id=Shipper.objects.get(company_name='BlueDart')
		
		order=Orders(order_id=orderid,payment_mode=payment_mode,billing_address_id=Address_details.objects.get(address_id=address_id),order_date=timezone.now(), ship_date=ship_date,
					 shipper_id=shipper_id, sales_tax=0, transact_status="True",order_total=total)
		order.save()

		for item in items:
			orderdetail=OrderDetails(

				order_id=Orders.objects.get(order_id=orderid), 
				email=User.objects.get(email=request.user.email),
				product_id=item.product_id, 
				shipping_address_id=Address_details.objects.get(address_id=address_id), 
				price=item.product_id.mrp, 
				quantity=item.quantity, 
				discount=item.product_id.discount, 
				total=item.price,
				id_sku=item.product_id.id_sku, 
				size=item.product_id.size, 
				color=item.product_id.color,			
				ship_date=ship_date, 
				bill_date=timezone.now(), 
				deliver_date=ship_date,
				status="Ordered"
				)
			orderdetail.save()


		count=Orders.objects.filter(order_id=orderid).count()

		if count:
			
			for item in items:
				prod=Product.objects.get(product_id=item.product_id)
				prod.units_in_stock=prod.units_in_stock-item.quantity
				prod.save()
			Cart.objects.all().filter(email=User.objects.get(email=request.user.email)).delete()
		else:
			messages.error(request,f"Error in Order")
	
	cart_count=0
	if request.user.is_authenticated :
		cart_count=Cart.objects.all().filter(email=User.objects.get(email=request.user.email)).count()

	return render(request = request,
                  template_name = "main/thankyou.html",
                  context={"order_id":orderid,"delivery_date":ship_date.date(),'cart_count':cart_count}
                )

def order_history(request):

	orderdetail=OrderDetails.objects.all().filter(email=User.objects.get(email=request.user.email)).order_by('-deliver_date')
	cart_count=0
	if request.user.is_authenticated :
		cart_count=Cart.objects.all().filter(email=User.objects.get(email=request.user.email)).count()

	
	return render(request = request,
                  template_name = "main/order_history.html",
                  context={"order_detail":orderdetail,'cart_count':cart_count}
                  )

def profile(request):
	user=User.objects.get(email=request.user.email)
	user_profile = UserProfile.objects.get(user=user)
	cart_count=0
	if request.user.is_authenticated :
		cart_count=Cart.objects.all().filter(email=User.objects.get(email=request.user.email)).count()
	

	return render(request = request,
                  template_name = "main/profile.html",
                  context={"user_profile":user_profile,'cart_count':cart_count}
                  )
def change_profile(request):

	if request.method == "POST":
		
		form = User_form(request.POST)
		form_profile = UserProfileForm(request.POST)
		user=User.objects.get(email=request.user.email)
		profile = form_profile.save(commit=False)
		user_profile = UserProfile.objects.get(user=user)
		user_profile.first_name = profile.first_name
		user_profile.last_name = profile.last_name
		user_profile.phone = profile.phone
		user_profile.save()


	cart_count=0
	if request.user.is_authenticated :
		cart_count=Cart.objects.all().filter(email=User.objects.get(email=request.user.email)).count()
	
	user = User.objects.get(email=request.user.email)  	
	user_profile = UserProfile.objects.get(user=user)
	form = User_form(initial={'email':user.email})
	form_profile = UserProfileForm(initial={'first_name':user_profile.first_name,'last_name':user_profile.last_name,'phone':user_profile.phone})

	return render(request = request,
                  template_name = "main/change_profile.html",
                  context={"form":form,'form_profile':form_profile,'cart_count':cart_count}
                  )

def change_password(request):

	if request.method == "POST":
		
		form = ChangePassword(request.POST)
		
		user=User.objects.get(email=request.user.email)
		

		if form.is_valid() :
			cur_pass = form.cleaned_data['password']
			
			if check_password(cur_pass, user.password) :
				user.password=make_password(form.cleaned_data['password1'])
				user.save()
				messages.success(request,f"Password updated successfully")
			else:
				messages.error(request, f"Incorrect Old password")
		else:
			messages.error(request,f"Invalid email or passwords dont match")

	cart_count=0
	if request.user.is_authenticated :
		cart_count=Cart.objects.all().filter(email=User.objects.get(email=request.user.email)).count()
	
	
	form = ChangePassword
	#form_profile = UserProfileForm(initial={'first_name':user_profile.first_name,'last_name':user_profile.last_name,'phone':user_profile.phone})

	return render(request = request,
                  template_name = "main/change_password.html",
                  context={"form":form,'cart_count':cart_count}
                  )

def forgot_password(request):

	if request.method == "POST":
			
		form = ForgotPassword(request.POST)

		if form.is_valid() :
			email = form.cleaned_data['email']
			
			if(User.objects.filter(email=email).exists()):
				user=User.objects.get(email=email)
				user.password=make_password(form.cleaned_data['password1'])
				user.save()
				messages.success(request,f"Password changed successfully")
				return redirect("main:login")
			else:
				messages.error(request,f"Entered email is not registered")

		else:
			messages.error(request,f"Invalid email or passwords dont match")				
				 
	form = ForgotPassword
	return render(request =request,
				  template_name="main/forgot_password.html",
				  context={"form":form}
				  ) 

def cancelorder(request,order_detail_id):
	
	order_detail = OrderDetails.objects.get(order_detail_id=order_detail_id)

	order_detail.cancelled=True
	order_detail.status = "Cancelled"

	product = Product.objects.get(product_id=order_detail.product_id)
	product.units_in_stock = product.units_in_stock + order_detail.quantity
	

	print(order_detail.order_id)
	products_in_order_count=OrderDetails.objects.filter(order_id=order_detail.order_id).count()
	if(products_in_order_count == 1):
		order=Orders.objects.get(order_id=order_detail.order_id)
		order.cancelled=True
		order.save()

	order_detail.save()
	product.save()
	messages.success(request,f"Order Successfully Cancelled")
	return redirect("main:order_history")