from django.shortcuts import render,redirect,get_object_or_404
from django.core.cache import cache
from blog.models import question,student_all_data,courses,number_of_tests_taken,AcceptanceofRules,TestStatus,TestStatus_aimode
from django.contrib.auth.models import User
from django.contrib import messages
from blog.my_ai_code import get_data_from_view,main,calculate_closes_question,grading_student,train_extra_grade_model
import pandas as pd
from django.db.models import Sum
from django.contrib.auth.signals import user_logged_out
from django.dispatch import receiver
import json
from decimal import Decimal


# Create your views here.

#@receiver(user_logged_out)
#def clear_cache_on_logout(sender, request, **kwargs):
#    # Kullanıcı oturumu kapandığında cache'deki verileri temizle
#    cache.clear()

#'home.html' ana dizindeki templates dosyasındaki home çalıştırır
def home(request):
    # Get all courses from the database
    all_courses = courses.objects.all()
    return render(request, 'home.html', {'courses': all_courses})
   

def register(request):
    #blog klasosurunde templates/blog klasorunun içindeki blog_detail.html çalıştırır
    return render(request,'blog/register.html')


def get_prev_question_id(request):
    return request.session.get('prev_question_id')

def set_prev_question_id(request, question_id):
    request.session['prev_question_id'] = question_id

def delete_prev_question_id(request):
    if 'prev_question_id' in request.session:
        del request.session['prev_question_id']
# get_prev_question_id ,set_prev_question_id,delete_prev_question_id  fonksiyonları kullanıcıyı bir önceki soruya geçisini sessiona kayıt etme silme işlemleri için yardımcı fonksiyonlardır.

# sınava başlamadan önce kuralları okudum kabul ediyorum sayfası
def rulesofexam(request):
    # ögrenci giriş yapmış mı kontrol eder
    if not request.user.is_authenticated:
        messages.error(request,"Error : Please Login to Start Test")
        return redirect('login')
    # ögrenci kuralları okuyup onaylayıp göndermiş mi ona bakar
    if request.method=="POST":
        checkbox_stituation=request.POST.get('accept_rule_checkbox')
        # eger onaylama kutucugunu işaretli degilse uyarı verir ve işaretlenmesi istenir
        if checkbox_stituation:
            user=request.user
            course=courses.objects.all()
            acceptance_obj=AcceptanceofRules(userid_acceptance=user,courseid_acceptance=course[0],user_rules_acceptance=True)
            acceptance_obj.save()
            cache.clear()
            return redirect ("Test") 
        else:
            messages.error(request,"You have to accept to rules before start to exam!!")

    return render (request,"rulesofexam.html")


# development mode active oldugunda database kayıtlı tüm soruları sırasıyla sorup veri toplaycak
def Test_in_development_mode(request):
    global theta_new,question_ids
    global i_num
    global num_question,question_data,thecourse,theuser,tests_taken_obj,tests_taken_obj_id
    global current_userid,selected_question
    # ögrenci giriş yapmış mı bakar
    if not request.user.is_authenticated:
        messages.error(request,"Error : Please Login to Start Test")
        return redirect('login')
    
    theuser=request.user
    acceptance_of_rules = AcceptanceofRules.objects.filter(userid_acceptance=theuser).first()
    # ögrenci rule onaylamış mı bakar onaylamışsa onaylama sayfasına gider
    if not acceptance_of_rules.user_rules_acceptance:
        return redirect("rulesofexam")  

    # ders hangi modda açılmış eger development modendu degil test modeunda açılmışsa teste yönlendirir.
    if not courses.objects.filter(development_mode=True).first():
        return redirect("Test")
    
    # eger ders tanımlama ekranın ögrencinin sınavı birkez çözsün secenegi açıksa ögrenci daha önce sınavı çözmüşmü bakar
    if courses.objects.filter(student_solve_exam_once=True).first():
            userexist = number_of_tests_taken.objects.filter(userid_tested=theuser,courseid_tested=1).count()
            if userexist>0:
                messages.warning(request, "You have already take the exam. You can not solve the test again")
                return redirect('home')

    
    if request.method == 'GET':
        print("GETTT ALINDI")

        if 'started_test' in request.session:
            messages.warning(request, "You have already started the test.")
            request.session.pop('started_test', None)  # Delete the session variable if it exists
            return redirect('home')
            
        request.session['started_test'] = True
        
         # Toplam soru sayısını ögreniyorum(databasede kayıtlı toplam soru sayısı) development mode oldugu için tüm soruları sırasıyla soracak
        question_data=question.objects.all()
        num_question=question_data.count()
        #ders objesi alıyorum databaseden
        thecourse=courses.objects.all()
        #giriş yapmış kullanıcının id alıyorum
        current_userid=request.user.id
        
        # Giriş yapmış kullanıcının id de objesini databaseden alıyorum
        theuser=request.user
        tests_taken_obj=number_of_tests_taken(userid_tested=theuser,courseid_tested=thecourse[0])
        tests_taken_obj.save()
        request.session['tests_taken_obj_id']=tests_taken_obj.id
        test_status, created = TestStatus.objects.get_or_create(user=theuser, defaults={'current_question': 0 })
       
       
        
    if request.method=="POST":
        
        print("POSTTT ALINDI ")
        theuser=request.user
        thecourse=courses.objects.all()
        question_data=question.objects.all()
        num_question=question_data.count()
        tests_taken_obj_id=request.session.get('tests_taken_obj_id')
        tests_taken_obj=number_of_tests_taken.objects.get(id=tests_taken_obj_id,userid_tested=theuser,courseid_tested=thecourse[0])
        answer=request.POST["answer"]
        counter_value = request.POST["counter"]
        #selected_question = question_data.filter(id=next_question_id).first()
        test_status=TestStatus.objects.get(user=theuser)
        i_num=test_status.current_question 
        
        if answer== question_data[i_num].True_choice:
            question_id=question_data[i_num].id
            student_obj=student_all_data(courseid=thecourse[0],questionid=question_data[i_num],userid=theuser,theanswer=1,theanswertime=counter_value,tests_taken_id=tests_taken_obj)
            student_obj.save()   
        else:
            student_obj=student_all_data(courseid=thecourse[0],questionid=question_data[i_num],userid=theuser,theanswer=0,theanswertime=counter_value,tests_taken_id=tests_taken_obj)
            student_obj.save()
               
        test_status.current_question += 1
        test_status.save()

        if test_status.current_question>=num_question:
            test_status.current_question = 0
            test_status.save()
            # Bir değeri session'dan silme
            if 'tests_taken_obj_id' in request.session:
                del request.session['tests_taken_obj_id']

            request.session.pop('started_test', None)  # Delete the session variable if it exists
            messages.success(request,"You complete The TEST!!")
            return redirect('home')
    return render(request,"TEST_development_mode.html",{'blog':question_data[test_status.current_question],'question_no':(test_status.current_question+1)})
        

         

# Yapay zeka ile adptif test sunar ögrenciye.ayrıca ögrencinin verdigi cevap süresine göre extra grdae verir.
def Test(request):

    global theta_old ,theta_new,student_time_data,question_ids,average_student_time_data
    global i_num,student_answers_dataframe,answer_condition_array,next_question_id,theta_new
    global num_question,question_data,thecourse,theuser,tests_taken_obj,thequestion
    global current_userid,selected_question,numberofquestionwillask
    

    #try:
    # giriş yapılmışmı kontrol eder
    if not request.user.is_authenticated:
        messages.error(request,"Error : Please Login to Start Test")
        return redirect('login')
    #development mode acık/kapalı kontrol eder açıksa development mode yönlendirir.
    if courses.objects.filter(development_mode=True).first():
        print("DEVELOPMENT MODE ON")
        return redirect("Test_in_development_mode")
    

    # Get methodunda ilk defa test açılıken sadece başlangıçta birdefa yapılmasını istedigim şeyleri belirtiyorum.
    # data baseden sadece birdefa ilk başta almak istedigim verileri GET belirtiyorum
    if request.method == 'GET':
        print("GETTT ALINDI")
        theuser=request.user
        acceptance_of_rules = AcceptanceofRules.objects.filter(userid_acceptance=theuser).first()
        if not acceptance_of_rules.user_rules_acceptance:
                return redirect("rulesofexam") 
        # eger ders tanımlama ekranında ogrenciler sınavı birkez cozsun isaretli ise aynı kullanıcıdan varmı bakar ve aynı kullanıcı varsa tekrar testi çözdürmez.
        if courses.objects.filter(student_solve_exam_once=True).first():
            userexist = number_of_tests_taken.objects.filter(userid_tested=theuser,courseid_tested=1).count()
            if userexist>0:
                messages.warning(request, "You have already take the exam. You can not solve the test again")
                return redirect('home')
        
    
        answer_condition_array=[]
        i_num=0 
        #question_data=question.objects.all()
        
        #ders objesi alıyorum databaseden
        thecourse=courses.objects.get(id=1)
        # listeden ilk dersi alır id=1 farklı olsada onu alır

        #giriş yapmış kullanıcının id alıyorum
        current_userid=request.user.id
        
    
        # Giriş yapmış kullanıcının id de objesini databaseden alıyorum
        theuser=request.user
    
        # Soruyu alın (örnek bir id kullandım, gerçek id'yi belirtin)
        tests_taken_obj=number_of_tests_taken(userid_tested=theuser,courseid_tested=thecourse)#development_mode_is_active=
        tests_taken_obj.save()
        # Şimdi tests_taken_obj'yi sessiona kaydedebilirsiniz
        request.session['tests_taken_obj_id'] = tests_taken_obj.id
        
        # Toplam soru sayısını ögreniyorum
        question_data=question.objects.all()
        num_question=question_data.count()
        # ögrencilere ders tanımlarken kaçtane soru sorulmasını istiyor isek girdigimiz degeri alır
        numberofquestionwillask=thecourse.question_asked
        request.session['numberofquestionwillask']=numberofquestionwillask
        test_status_aimode, created = TestStatus_aimode.objects.get_or_create(user=theuser, defaults={'current_question': 0 ,'current_theta': 0})
        theta_old =0
        print("test_status_aimode Theta ",test_status_aimode.current_theta)
        if(numberofquestionwillask > num_question ):
            messages.error(request,"Error : Total question number less than number of question will asked please load more question or less question will asked")
            return redirect('home')
        
        question_ids = question.objects.filter(course_id=thecourse.id).values_list('id', flat=True)
        
        # Her bir soru için verileri çek (ileride tüm verileriçekip sonradan python koduyla sorular ayrı kolumlarda ayarlanabilir.)
        student_time_data={}
        student_answers_data = {}
        for question_id in question_ids:
            answers = student_all_data.objects.filter(questionid=question_id).values_list('theanswer', flat=True)
            student_answers_data[f'{question_id}'] = list(answers)
            time= student_all_data.objects.filter(questionid=question_id).values_list('theanswertime', flat=True)
            student_time_data[f'{question_id}'] = list(time)

        request.session['student_time_data']=student_time_data 
        
        answer_condition_array=request.session.get('answer_condition_array',[])
        request.session['student_answers_data']=student_answers_data
        
        # soruların goru cevaplarını toplayıp sonra average alıp sonra average -1 ile 1 arasına truncate eder
        student_answers_dataframe=get_data_from_view(student_answers_data)
       
        next_question_id=calculate_closes_question(student_answers_dataframe,answer_condition_array,theta_old)
        request.session['next_question_id']=next_question_id
        #calculate average answer times of the questions
        student_time_data = pd.DataFrame.from_dict(student_time_data, orient='index').transpose() # conver into dataframe
        average_student_time_data=(student_time_data.mean(skipna=True)) # get average of the time dataframe
        
                 

    elif request.method=="POST":
        print("POSTTTT ALINDIIII.")
        theuser=request.user
        test_status_aimode=TestStatus_aimode.objects.get(user=theuser)
        theta_old=test_status_aimode.current_theta
        question_data=question.objects.all()
        answer=request.POST["answer"]
        counter_value = request.POST["counter"]
        #try:
        student_time_data=request.session.get('student_time_data')
        student_time_data = pd.DataFrame.from_dict(student_time_data, orient='index').transpose() # conver into dataframe
        average_student_time_data=(student_time_data.mean(skipna=True)) # get average of the time dataframe
        

        student_answers_data=request.session.get('student_answers_data',[])
        student_answers_dataframe=get_data_from_view(student_answers_data)
        numberofquestionwillask=request.session.get('numberofquestionwillask')
        next_question_id=request.session.get('next_question_id')
        print("next_question_id : ",next_question_id)
        answer_condition_array=request.session.get('answer_condition_array',[])
        answer_condition_array.append(next_question_id)
        request.session['answer_condition_array']=answer_condition_array         
        selected_question = question_data.filter(id=next_question_id).first()
        # Sessiondan tests_taken_obj'yi al
        tests_taken_obj_id = request.session.get('tests_taken_obj_id')
        if tests_taken_obj_id is not None:
        # Eğer tests_taken_obj_id varsa, objeyi veritabanından çek
            tests_taken_obj = get_object_or_404(number_of_tests_taken, id=tests_taken_obj_id)

        if answer== selected_question.True_choice:

            theta_old=test_status_aimode.current_theta
            question_id=question_data[i_num].id
            difficulty=student_answers_dataframe.loc[str(question_id),'Normalized_difficulty']
            extra_grade=train_extra_grade_model(counter_value,average_student_time_data.loc[str(question_id)],difficulty)
            selected_question = question_data.filter(id=next_question_id).first()
            student_obj=student_all_data(courseid=thecourse,questionid=selected_question,userid=theuser,theanswer=1,extragrade=extra_grade,theanswertime=counter_value,tests_taken_id=tests_taken_obj)
            student_obj.save()
            next_question_id_calculated,theta_new=main(student_answers_dataframe,answer_condition_array,1,theta_old) 
            next_question_id=next_question_id_calculated
            request.session['next_question_id']=next_question_id
            theta_old=theta_new
            test_status_aimode.current_theta=theta_new
            print('test_status_aimode.current_theta :',test_status_aimode.current_theta)
        else:
            
            selected_question = question_data.filter(id=next_question_id).first()
            student_obj=student_all_data(courseid=thecourse,questionid=selected_question,userid=theuser,theanswer=0,extragrade=0,theanswertime=counter_value,tests_taken_id=tests_taken_obj)
            student_obj.save()
            next_question_id_calculated,theta_new=main(student_answers_dataframe,answer_condition_array,0,theta_old) 
            next_question_id=next_question_id_calculated
            request.session['next_question_id']=next_question_id
            theta_old=theta_new
            test_status_aimode.current_theta=theta_new
            print('test_status_aimode.current_theta :',test_status_aimode.current_theta)
        test_status_aimode.current_question += 1
        test_status_aimode.save()
        i_num=test_status_aimode.current_question
        print('test_status_aimode.current_question :',test_status_aimode.current_question)

        if test_status_aimode.current_question>=numberofquestionwillask:
            instance_student_extra_grade_total=student_all_data.objects.filter(courseid=thecourse,userid=theuser,tests_taken_id=tests_taken_obj).aggregate(Sum('extragrade'))['extragrade__sum']
            tests_taken_obj.Total_extra_time_grade=round(instance_student_extra_grade_total,4)
            theta_grade=round(grading_student(theta_old),3)
            print('theta_gradeeee: ',theta_grade)
            setattr(tests_taken_obj,'Total_theta_grade', theta_grade)
            theta_end=round(test_status_aimode.current_theta,4)
            setattr(tests_taken_obj,'ability_theta', theta_end)
            Total_grade=instance_student_extra_grade_total+theta_grade
            setattr(tests_taken_obj,'Total_grade', Total_grade)
            tests_taken_obj.save()
            request.session.pop('started_test', None)  # Delete the session variable if it exists
            messages.success(request,"You complete The TEST!!")
            test_status_aimode.current_question = 0
            test_status_aimode.current_theta = 0
            test_status_aimode.save()
            request.session.clear()
            return redirect('home')
            
        #except Exception as e:
            #messages.error(request,f"Beklenmeyen bir hata oluştu: {str(e)}")
            #return redirect('home')
        
#except Exception as e:
    
    #messages.error(request,f"Beklenmeyen bir hata oluştu: {str(e)}")
    #return redirect('home')   

    print('GET GEÇİLDİİİ')
    selected_question = question_data.filter(id=next_question_id).first()
    return render(request,"TEST_main.html",{'blog':selected_question,'question_no':(next_question_id)})
            
        

# veritabanına data yazma
#b1=question(question_description="asd2",A="a2",B="b2",C="c2",D="d2",E="e2")
#b1.save()

#veri tabanından data çekme(tüm dataları) b2=[{1.row},{2.row},{3.row}...] şeklinde datalar geliyor
# dataları kullanmak için dictionaru yapısında kullanıyoruz b2[0].A dedigimde birinci row da A isimli colomun datasını getir demek 
#b2=question.objects.all()
#print("1 row da quesstion description columndaki data= ",b2[0].question_description)


# question tablosundan id=1 olan kolumnda quesiton_description alır
#print("question_description",question.objects.get(id=1).question_description)

'''
    blog=question.objects.all() # tüm columnları dictinary şekilde döner
    answers  = question.objects.values('True_choice')   # dictionary döner
    answers2 = question.objects.values_list('True_choice', flat=True) # liste dizi döner
    print("question_data : ",question_data)
    print("question_answers ",answers)
    print("question_answers2 ",answers2)

    #selected_question = question_data.filter(id=next_question_id).first()

      if student_data.objects.get(userid=request.user.id).istested:
        messages.error(request,"You have Alredy take the TEST!!")
        return redirect('home')

        
    ogrenci = Ogrenci.objects.get(user__username='kullanici_adi')
    kullanici = ogrenci.user
    print(kullanici.username)  # Kullanıcının kullanıcı adını almak
    print(kullanici.email)      

    ogrenci = Ogrenci.objects.get(user__username='kullanici_adi')
    # Kullanıcı bilgilerini güncellemek
    ogrenci.user.first_name = 'Yeni Ad'
    ogrenci.user.save()    
        
        
        
'''
'''  
      # Tüm soruları database den alıyorum (yapay zeka tarafına gönderme method 2)     
        
        student_answer_datas=student_all_data.objects.all()
        question_names=student_all_data.question_name
        question_names=[key for key in question_names]
        print("question_names",question_names)
        student_data=student_all_data.objects.values_list(*question_names)
        print("student_data : ",student_data)
        get_data_from_view(student_data)
        # Toplam soru sayısını ögreniyorum
        num_question=question_data.count()
        print("num_question",str(num_question))
        #return render(request,"Test3.html",{'blog':question_data[i]})
        print("USER ID ",str(request.user.id))
    
        #setattr(student_answer_instance,'theanswertime', counter_value)
        #student_time_instance.save()

        #student_answer_instance.save_student_data('theanswer',0)
        #student_answer_instance.save()

        #student_answer_instance.save_student_data('theanswer',1)
            #student_answer_instance.save()
            #student_data_instance.soru_1="1"

        question_names = question.objects.filter(course_id=thecourse.id).values_list('question_description', flat=True)
        print("question_ids : ",list(question_names))

        # Her bir soru ID'si için ilgili alanları çek
        #student_answers_data = student_all_data.objects.filter(questionid__in=question_ids).values_list('theanswer',flat=True)
        #print("student_data",*student_data)

        # aynı id den kaçtane kullanıcı var bakıyorum.
        #userexist = number_of_tests_taken.objects.filter(userid_tested=current_userid,courseid_tested=1).count()
        #numberOfTest=number_of_tests_taken.objects.filter(userid_tested=theuser,courseid_tested=1).count()
        #kullanıcı daha önce varmı bakar eger var ise database yeni obje oluşturmaz.Var olan objenin üstüne yazar.
            
            
            
            thequestion = question()
            print("thequestion : ",thequestion)
            #giriş yapmış kişinin database student_datada row oluşturuyorum default degerler ile
            #anwers_obj=student_all_data.objects.create(userid=theuser,courseid=thecourse,questionid=thequestion)
        
        # giriş yapmış kullanıcının sorulara verdigi cevapları kaydetmek için instance objesi oluşturdum
        #student_answer_instance = get_object_or_404(student_all_data,userid=current_userid,questionid=thequestion)
        # giriş yapmış kullanıcının sorulara verdigi cevapları kaydetmek için instance objesi oluşturdum
        #student_answer_instance = get_object_or_404(student_all_data,userid=current_userid,questionid=thequestion)
        '''

