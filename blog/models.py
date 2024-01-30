from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.safestring import mark_safe
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError


# Create your models here.
# aynı anda giriş  yapan kullanıcıları ayırt edip hangi  kullanıcı 
class TestStatus_aimode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_question = models.IntegerField(default=1)
    current_theta=models.FloatField(default=0)

# aynı anda giriş  yapan kullanıcıları ayırt edip hangi  kullanıcı 
class TestStatus(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_question = models.IntegerField(default=1)

# kullanıcının kuralları kabul edip etmedigini tutar database de
class AcceptanceofRules(models.Model):
    userid_acceptance = models.ForeignKey(User, on_delete=models.CASCADE)
    courseid_acceptance = models.ForeignKey('courses', on_delete=models.CASCADE)
    user_rules_acceptance=models.BooleanField(default=False)
    date_taken_acceptance = models.DateTimeField(auto_now_add=True)
    # Bu örnekte, courses modelindeki development_mode değerini alıp, number_of_tests_taken modeline atıyoruz
    #data print ettiginde terminalde nasıl görünmesi istiyorsan __str__ ile tanımlarsın
    def __str__(self):
        return f"{self.userid_acceptance.username}'s test result for {self.courseid_acceptance.course_name}"



class courses(models.Model):
    # coursename
    course_name=models.CharField('Dersin Adini Giriniz',max_length=120)
    # Total question in the course
    total_question_number=models.PositiveIntegerField(default=1)
    # number of question that will ask student
    question_asked=models.PositiveIntegerField()
    course_is_active=models.BooleanField() # şuan için kullanılmıyor ilerde çok ders olunca dersleri user açmak veya kapatmak için kullanılacak
    student_solve_exam_once=models.BooleanField(default=False)
    development_mode=models.BooleanField()
    def clean(self):
        # Eğer development_mode aktifse ve total_question_number, question_asked'den küçükse hata fırlat
        if  self.total_question_number < self.question_asked:
            raise ValidationError({'question_asked': 'Total questions should be greater than or equal to the number of questions asked.'})
    
    def save(self, *args, **kwargs):
        # clean metodunu çağır
        self.clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.course_name
    



class student_all_data(models.Model):
    courseid = models.ForeignKey('courses', default=1, on_delete=models.CASCADE)
    questionid=models.ForeignKey('question',default=0,on_delete=models.CASCADE)
    userid = models.ForeignKey(User, default=1, on_delete=models.CASCADE)
    theanswer=models.PositiveIntegerField(default=2) # 2 means question not asked yet. 1 is True 0 is False
    theanswertime=models.PositiveIntegerField(default=0) # 0 means question doesnot asked yet. 
    extragrade=models.IntegerField(default=0)
    istested = models.BooleanField(default=False)
    tests_taken_id=models.ForeignKey('number_of_tests_taken',null=True,on_delete=models.CASCADE)

from decimal import Decimal, InvalidOperation
# kullanıcının kaç kez  teste girdigi ve zamanını verisini tutar
class number_of_tests_taken(models.Model):
    userid_tested = models.ForeignKey(User, on_delete=models.CASCADE)
    courseid_tested = models.ForeignKey('courses', on_delete=models.CASCADE)
    development_mode_is_active = models.BooleanField()
    ability_theta=models.FloatField(default=0)
    Total_theta_grade=models.FloatField(default=0)
    Total_extra_time_grade=models.FloatField(default=0)
    Total_grade=models.FloatField(default=0)
    date_taken = models.DateTimeField(auto_now_add=True)
     # Bu örnekte, courses modelindeki development_mode değerini alıp, number_of_tests_taken modeline atıyoruz
    def save(self, *args, **kwargs):
        try:
            # Bu örnekte, courses modelindeki development_mode değerini alıp, number_of_tests_taken modeline atıyoruz
            if self.courseid_tested:
                self.development_mode_is_active = self.courseid_tested.development_mode
            super().save(*args, **kwargs)
        
        except InvalidOperation as e:
            print(f"number_of_tests_taken save sırasında hata oluştu. HATA: {e}")
    
        except Exception as e:
            print(f" number_of_tests_taken save sırasında başka bir hata oluştu. HATA: {e} ")

    #data print ettiginde terminalde nasıl görünmesi istiyorsan __str__ ile tanımlarsın
    def __str__(self):
        return f"{self.userid_tested.username}'s test result for {self.courseid_tested.course_name}"

class question(models.Model):
    #question_image=models.FileField():
    image=models.ImageField(upload_to="blogs",blank=True,null=True)
    # html sayfaısnda quesiton_description gösterildigi yere |safe yazmamız gerek
    question_description= models.TextField(blank=True,null=True)
    A=models.CharField('A',max_length=120,blank=True,null=True)
    B=models.CharField('B',max_length=120,blank=True,null=True)
    C=models.CharField('C',max_length=120,blank=True,null=True)
    D=models.CharField('D',max_length=120,blank=True,null=True)
    E=models.CharField('E',max_length=120,blank=True,null=True)
    True_choice=models.CharField('true_choice',max_length=3,choices={"A":"A","B":"B","C":"C","D":"D","E":"E"})
    #many to one iliski tipi(bir soru bir derse sadece ait olabilir)
    course_id= models.ForeignKey(courses,default=1,on_delete=models.CASCADE) # models.CASCADE courses biri silindiginde o derse ait sorularda silinir.
    # may to many iliskide (bir soru birden fazla derse ait olabilir)
    # course_id=models.ManyToManyField(courses) 
    def __str__(self):
        return f" soru {self.id} "
    # bir sorunun resmini günceller iken önceki yüklenmiş resmi siler
    def save(self, *args, **kwargs):
        # Eğer bu model daha önce kaydedilmişse (id'si varsa)
        if self.id:
            # Önceki modeli veritabanından getir
            old_instance = question.objects.get(pk=self.id)
            # Eğer eski resim varsa, onu sil
            if old_instance.image and self.image != old_instance.image:
                old_instance.image.delete(save=False)
        super().save(*args, **kwargs)
    
@receiver(pre_delete,sender=question)
def delete_image_on_model_delete(sender, instance, **kwargs):
    # Eğer bu modelin bir resmi varsa, resmi sil (modeli soruyu silerken baglı oldgu resmide siler)
    if instance.image:
        instance.image.delete(save=False)
    
   


# sisteme giriş yapan kişinin bilgilerinden clasaa verdik direk
class Students(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

def validate_unique_image_name(self, value):
            # Fonksiyonun içeriği burada olmalı
        pass 
'''
class student kullanımı

 ogrenci = Ogrenci.objects.get(user__username='kullanici_adi')
    kullanici = ogrenci.user
    print(kullanici.username)  # Kullanıcının kullanıcı adını almak
    print(kullanici.email)      

    ogrenci = Ogrenci.objects.get(user__username='kullanici_adi')
    # Kullanıcı bilgilerini güncellemek
    ogrenci.user.first_name = 'Yeni Ad'
    ogrenci.user.save() 

    
    
    
ckeditöre sahip html kodlarini da yorumlayan bir editör şeklinde textfield tanimlamak icin
from ckeditor.fields import RichTextField
question_description= RichTextField(blank=True,null=True)   

html kodlarını html göre yorumlar öyle kayıteder
  def save(self, *args, **kwargs):
    # Burada mark_safe fonksiyonunu kullanabilirsiniz,
    # ancak dikkatli olmalısınız, güvenlik riskleri olabilir.
        self.question_description = mark_safe(self.question_description)
        super().save(*args, **kwargs)


    
class Answer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.ForeignKey(question, on_delete=models.CASCADE)
    answer_text = models.TextField()
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s answer to {self.question.question_text}"

        
@receiver(pre_save, sender=courses)
def add_dynamic_fields(sender, instance, **kwargs):
    number_of_questions = instance.total_question_number
    print("eentered receiver total_question :",number_of_questions)


class student_time_data(models.Model):
    question_time_name={}
    for i in range(1,4):
        question_time_name[f'soru{i}_time']=models.PositiveIntegerField(default=0)            
    locals().update(question_time_name)

    student_id=models.ForeignKey(User,default=1,on_delete=models.CASCADE)
    numberoftest_time=models.PositiveIntegerField(default=1)

'''

