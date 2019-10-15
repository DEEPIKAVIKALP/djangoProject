from django.db import models
from django.contrib.auth.models import (
	AbstractBaseUser, BaseUserManager
)
#from django.contrib.auth.models import PermissionsMixin
from datetime import datetime

# Create your models here.
class Supplier(models.Model):
    supplier_id = models.AutoField(primary_key=True)
    company_name = models.CharField(max_length=100)
    contact_fname = models.CharField(max_length=50)
    contact_lname = models.CharField(max_length=50)
    contact_title = models.CharField(max_length=10)
    address1 = models.CharField(max_length=200)
    address2 = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    pincode = models.CharField(max_length=6)	
    country = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    email= models.EmailField(max_length=100)
    payment_method = models.CharField(max_length=15)
    type_goods =models.CharField(max_length=100)
    
    def __str__(self):
    	return self.company_name

class Category(models.Model):
	category_id = models.AutoField(primary_key=True)
	category_name = models.CharField(max_length=255)	
	description = models.CharField(max_length=50)
	picture = models.ImageField(upload_to='category_images/%Y/%m/%d')
	active = models.BooleanField(default=True)

	def __str__(self):
		return self.category_name


class Payment(models.Model):
	payment_id = models.AutoField(primary_key=True)
	payment_type = models.CharField(max_length=20)
	allowed = models.BooleanField(default=True)

	def __str__(self):
		return self.payment_type

class Shipper(models.Model):
	shipper_id = models.AutoField(primary_key=True)
	company_name = models.CharField(max_length=100)
	phone = models.CharField(max_length=10)

	def __str__(self):
		return self.company_name

class UserManager(BaseUserManager):
	def create_user(self, email, password=None):
		if not email:
			raise ValueError("Users must have an email address")
		if not password:
			raise ValueError("Users must have a password")
		user_obj = self.model(
			email = self.normalize_email(email)
		)
		
		user_obj.set_password(password)
		user_obj.save(using=self._db)
		return user_obj
		

	def create_staffuser(self, email, password):
		user = self.create_user(
            	email,
            	password = password,
        )

		user.staff = True
		user.save(using=self._db)
		return user


	def create_superuser(self, email, password):
		user = self.create_user(
        		email,
        		password = password,
        )
		user.staff = True
		user.admin = True
		user.save(using=self._db)
		return user


		

		
class User(AbstractBaseUser):
	email = models.EmailField(max_length=255, unique=True)
	active = models.BooleanField(default=True)
	staff = models.BooleanField(default=False)
	admin = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []

	objects = UserManager()

	def __str__(self):
		return self.email

	def get_first_name(self):
		return self.first_name

	def get_last_name(self):
		return self.last_name

	def has_perm(self, perm, object=None):
		return True
	def has_module_perms(self, app_label):
		return True	

	@property
	def is_admin(self):
		return self.admin
	@property
	def is_active(self):
		return self.active
	@property
	def is_staff(self):
		return self.staff

		
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete = models.CASCADE)
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
#	address1 = models.CharField(max_length=200)
#	address2 = models.CharField(max_length=200)
#	city = models.CharField(max_length=50)
##	state = models.CharField(max_length=50)
#	pincode = models.CharField(max_length=6)	
#	country = models.CharField(max_length=50)
	phone = models.CharField(max_length=10)
#	password = models.CharField(max_length=50)
#	credit_card = models.CharField(max_length=50)
#	credit_card_type_id = models.CharField(max_length=4)
#	card_exp_month = models.CharField(max_length=2)
#	card_exp_year = models.CharField(max_length=4)
#	date_entered = models.DateTimeField('date entered')
	

	def __str__(self):
		return self.user.email	 	

class Address_details(models.Model):
	address_id=models.AutoField(primary_key=True)
	email=models.ForeignKey(User, verbose_name='Email', on_delete=models.CASCADE)
	name=models.CharField(max_length=200)
	house_no = models.CharField(max_length=200)
	building_name = models.CharField(max_length=200,null=True,blank=True)
	landmark = models.CharField(max_length=200,null=True,blank=True)
	city = models.CharField(max_length=50)
	state = models.CharField(max_length=50)
	pincode = models.CharField(max_length=6)	
	country = models.CharField(max_length=50)
	phone = models.CharField(max_length=10)

	def __str__(self):
		return str(self.address_id)

class Orders(models.Model):
	order_id = models.CharField(max_length=20, primary_key=True)
	payment_mode = models.CharField(max_length=10)
	billing_address_id = models.ForeignKey(Address_details, verbose_name='Address Id', on_delete=models.CASCADE)
	order_date = models.DateTimeField('order date')
	ship_date = models.DateTimeField('ship date')
	shipper_id = models.ForeignKey(Shipper, verbose_name='Shipper ID',on_delete=models.CASCADE)
	sales_tax = models.IntegerField()
	transact_status = models.CharField(max_length=20)
	fulfilled = models.BooleanField(default=False)
	cancelled = models.BooleanField(default=False)#for cancellation
	paid = models.BooleanField(default=False)
	payment_date = models.DateTimeField('payment date', null=True, blank=True)
	order_total = models.DecimalField(max_digits=10,decimal_places=2)

	def __str__(self):
		return self.order_id

class Product(models.Model):
	product_id = models.AutoField(primary_key=True)
	sku = models.CharField(max_length=255)
	id_sku = models.CharField(max_length=255)
	product_name = models.CharField(max_length=255)
	product_description = models.CharField(max_length=255)
	supplier_id = models.ForeignKey(Supplier, verbose_name='Supplier ID',on_delete=models.CASCADE)
	category_id = models.ForeignKey(Category, verbose_name='Category ID',on_delete=models.CASCADE)
	quantity_per_unit = models.IntegerField() 
	unit_price = models.DecimalField(max_digits=10,decimal_places=2)
	mrp = models.DecimalField(max_digits=10,decimal_places=2)
	available_size = models.CharField(max_length=255)
	available_colors = models.CharField(max_length=255)
	size = models.CharField(max_length=255)
	color = models.CharField(max_length=255)
	discount = models.DecimalField(max_digits=10,decimal_places=2)
	unit_weight = models.CharField(max_length=255) 
	units_in_stock = models.PositiveIntegerField()
	product_available = models.BooleanField(default=True)
	discount_available = models.BooleanField(default=False)
	picture1 = models.ImageField(upload_to='product_images/%Y/%m/%d')
	picture2 = models.ImageField(upload_to='product_images/%Y/%m/%d', null=True,blank=True)
	picture3 = models.ImageField(upload_to='product_images/%Y/%m/%d', null=True, blank=True)
	picture4 = models.ImageField(upload_to='product_images/%Y/%m/%d',null=True,blank=True)
	picture5 = models.ImageField(upload_to='product_images/%Y/%m/%d',null=True,blank=True)
	picture6 = models.ImageField(upload_to='product_images/%Y/%m/%d',null=True,blank=True)
	picture7 = models.ImageField(upload_to='product_images/%Y/%m/%d',null=True,blank=True)
	ranking = models.IntegerField(blank=True, null=True)
	note = models.CharField(max_length=255)
	
	def __int__(self):
		return self.product_id

class OrderDetails(models.Model):
	order_detail_id = models.AutoField(primary_key=True)
	order_id = models.ForeignKey(Orders, verbose_name='Order ID', on_delete=models.CASCADE)
	email = models.ForeignKey(User, verbose_name='Email', on_delete=models.CASCADE)
	product_id = models.ForeignKey(Product, verbose_name='Product ID', on_delete=models.CASCADE)
	shipping_address_id = models.ForeignKey(Address_details, verbose_name='Address Id', on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=10,decimal_places=2)
	quantity = models.IntegerField()
	discount = models.DecimalField(max_digits=10,decimal_places=2)
	total = models.DecimalField(max_digits=10,decimal_places=2)
	id_sku = models.CharField(max_length=255)
	size = models.CharField(max_length=255)
	color = models.CharField(max_length=255)
	fulfilled = models.BooleanField(default=False)
	cancelled = models.BooleanField(default=False)
	ship_date = models.DateTimeField('ship date')
	bill_date = models.DateTimeField('bill date')
	deliver_date = models.DateTimeField('deliver date')
	status = models.CharField(max_length=20)

	def __str__(self):
		return str(self.order_detail_id)
#adjust postive integer field for quantity and price

  
class Cart(models.Model):
	cart_id=models.AutoField(primary_key=True)
	email = models.ForeignKey(User, verbose_name='Email', on_delete=models.CASCADE)
	product_id = models.ForeignKey(Product, verbose_name='Product ID', on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=10,decimal_places=2)
	quantity = models.PositiveIntegerField()
	def __str__(self):
		return str(self.cart_id)
 
