from django.db import models
from django.utils import timezone

class SettingSite(models.Model):
    site_title = models.CharField('عنوان الموقع', max_length=100)
    
    site_name = models.CharField('اسم الموقع', max_length=100)

    description = models.TextField('الوصف',)

    keywords = models.TextField('كلمات مفتاحية', blank=True, null=True)

    icon = models.ImageField('أيقونة الموقع', upload_to='img/')

    logo = models.ImageField('لوجو الموقع', upload_to='img/')

    main_image = models.ImageField('صورةالخلفية الرئيسية', upload_to='img/')

    about_us_image = models.ImageField('صورة فقرة من نحن', upload_to='img/')

    currency = models.CharField('العملة', max_length=30)

    address = models.CharField('العنوان', max_length=200, blank=True, null=True)

    phone = models.CharField('رقم الهاتف', max_length=30)

    email = models.EmailField('البريد الإلكتروني', max_length=60, blank=True, null=True)

    whatsapp = models.BooleanField("خاصية الاتصال بواتساب", default=True)

    instagram = models.URLField('انستجرام', max_length=200, blank=True, null=True)

    facebook = models.URLField('فيسبوك', max_length=200, blank=True, null=True)

    phone_feature = models.BooleanField('خاصية الاتصال بالهاتف', default=True)
    
    imogie = models.BooleanField('الايموجي', default=True)
    
    contact_section = models.BooleanField('قسم التواصل', default=True)
    
    end_order = models.BooleanField('الولج الى صفحة استلام الطلبية', default=False, help_text="هل تريد المستخدم ان يستطيع الولوج الى الصفحة النهائية ( استلام الطلبية ) دائما ؟")

    color = models.CharField(max_length=20, verbose_name=' اللون الرئيسي', help_text='أدخل اللون (مثل #FF0000 أو red)')

    created_on = models.DateTimeField(
         'تاريخ الاضافة', default=timezone.now)

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'اعدادات الموقع'
        verbose_name_plural = 'اعدادات الموقع'

    def __str__(self):
        return self.site_title

class Constants(models.Model):
    about_us_title = models.CharField('عنوان فقرة من نحن', max_length=255)

    about_us_content = models.TextField('محتوى فقرة من نحن',)

    subscription_title = models.CharField('عنوان نموذج الاشتراك', max_length=255)

    title_products = models.CharField('عنوان المنتجات', max_length=255)

    title_special_products =  models.CharField('عنوان المنتجات الاكثر طلبا', max_length=255)
    
    title_lists = models.CharField('عنوان القوائم الخاصة', max_length=255)

    title_footer = models.CharField('عنوان الفوتر (أسفل الصفحة)', max_length=255)

    contact_title = models.CharField('عنوان صفحة اتصل بنا', max_length=255)

    contact_form_title = models.CharField('عنوان الفورم الخاصة بصفحة اتصل بنا', max_length=255)
    
    command_title = models.CharField('عنوان صفحة استلام الطلبية ', max_length=255)
    
    command_details = models.TextField('تفاصيل الطلبية' ,)
    
    contact_note = models.CharField('ملاحظات الاتصال', max_length=255)
    
    phone_button = models.CharField('نص زر الاتصال بالهاتف', max_length=255)

    whatsapp_button = models.CharField( "نص زر الاتصال بالواتساب" , max_length=255)

    created_on =  models.DateTimeField('تاريخ الاضافة',  default=timezone.now)

    checkout_title = models.CharField('عنوان صفحة تأكيد الطلبية ', max_length=255)
    
    checkout_button = models.CharField('نص زر التأكيد', max_length=255)
    
    class Meta:
        ordering = ['-created_on']
        verbose_name = 'النصوص و الثوابت'
        verbose_name_plural = 'النصوص و الثوابت'


class ProductType(models.Model):
    name = models.CharField("الاسم",max_length=255)

    created_on =  models.DateTimeField(
         'تاريخ الاضافة',  default=timezone.now)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_on']
        verbose_name = 'النوع'
        verbose_name_plural = 'أنواع المنتجات'

class Subscription(models.Model):
    name = models.CharField("الاسم", max_length=40 )

    phone = models.CharField('رقم الهاتف', max_length=30)

    created_on = models.DateTimeField(
        'تاريخ الاضافة', default=timezone.now)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['-created_on']
        verbose_name = 'المشترك'
        verbose_name_plural = 'المشتركين'


class Message(models.Model):
    name = models.CharField("الاسم", max_length=40)

    phone = models.CharField('رقم الهاتف', max_length=30)

    subject = models.CharField('الموضوع', max_length=200)

    message = models.TextField('الرسالة')

    created_on = models.DateTimeField(
        'تاريخ الاضافة', default=timezone.now)

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'رسائل المستخدمين'
        verbose_name_plural = 'رسائل المستخدمين'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField("الاسم",max_length=255)
    
    description = models.TextField('الوصف')

    max_quantity = models.IntegerField('أقصى قيمة', default=30)
    
    product_type = models.ForeignKey(ProductType,  on_delete=models.CASCADE, verbose_name='نوع المنتوج')
    
    old_price = models.IntegerField('ثمن المنتوج قبل التخفيض', blank=True, null=True)
    
    price = models.IntegerField('ثمن المنتوج')
    
    image = models.ImageField('الصورة', upload_to='products/', )

    state = models.BooleanField('حالة المنتج', default=True)
    
    created_on =  models.DateTimeField(
         'تاريخ الاضافة',  default=timezone.now)
    
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'المنتج'
        verbose_name_plural = 'المنتجات'


    @property
    def url(self):
        link = self.name.replace(' ', '-')

        return link
    
class BigProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    created_on =  models.DateTimeField('تاريخ الاضافة', default=timezone.now)

    def __str__(self):
        return f'{self.product.name}'
    
    class Meta:
        ordering = ['-created_on']
        verbose_name = 'المنتج'
        verbose_name_plural = 'المنتجات الأكثر طلبا'



class ListProducts(models.Model):
    title =  models.CharField('اسم القائمة', max_length=255)

    products = models.ManyToManyField(Product, related_name='lists')

    created_on =  models.DateTimeField('تاريخ الاضافة', default=timezone.now)

    def __str__(self):
        return f'{self.title}'
    
    class Meta:
        ordering = ['-created_on']
        verbose_name = 'القائمة'
        verbose_name_plural = 'قوائم المنتجات'

class Shipping(models.Model):
    city = models.CharField('المدينة', max_length=255)

    price = models.IntegerField('الثمن')
    
    state = models.BooleanField('الحالة', default=True)
    
    created_on =  models.DateTimeField('تاريخ الاضافة', default=timezone.now)

    def __str__(self):
        return f'{self.city}'
    
    class Meta:
        ordering = ['-created_on']
        verbose_name = 'المدينة'
        verbose_name_plural = 'المدن'

class Features(models.Model):
    icon = models.CharField('الايقونة', max_length=255)

    title = models.CharField('العنوان', max_length=255)

    content = models.TextField('المحتوى')

    created_on =  models.DateTimeField('تاريخ الاضافة', default=timezone.now)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_on']
        verbose_name = 'السمة'
        verbose_name_plural = 'السمات او الخاصيات'
    

class Order(models.Model):
    number = models.CharField('رقم الطلبية', max_length=15)
    
    customer = models.CharField('العميل', max_length=70)
    
    phone_number = models.CharField('رقم الهاتف', max_length=70)
    
    city = models.ForeignKey(Shipping, verbose_name='المدينة', on_delete=models.Aggregate)
    
    address = models.CharField('العنوان', max_length=255)
    
    state = models.BooleanField('الحالة', default=False)
    
    note = models.TextField('ملاحظة', blank=True, null=True)
    
    created_on =  models.DateTimeField('تاريخ الاضافة', default=timezone.now)

    def __str__(self):
        return f'{self.customer} #{self.number}'
    
    @property
    def getTotal(self):
        total = int(self.city.price)
        ps = self.products.all()
        for p in ps:
            total += p.getTotal
        return total
    
    class Meta:
        ordering = ['-created_on']
        verbose_name = 'الطلبية'
        verbose_name_plural = 'الطلبيات'


class CartProduct(models.Model):
    product = models.ForeignKey( Product, verbose_name='المنتج', on_delete=models.CASCADE)
    
    order = models.ForeignKey( Order, verbose_name='الطلبية', on_delete=models.CASCADE, related_name='products')
    
    quantity = models.PositiveIntegerField('الكمية', default=1)
    
    created_on =  models.DateTimeField('تاريخ الاضافة', default=timezone.now)

    def __str__(self):
        return f"{self.product.name} ({self.quantity})"

    @property
    def getTotal(self):
        return int(self.product.price) * self.quantity
    
    class Meta:
        ordering = ['-created_on']
        verbose_name = 'منتج الطلبية'
        verbose_name_plural = 'منتجات الطلبيات'
