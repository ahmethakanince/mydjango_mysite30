from django.contrib import admin
from .models import question,courses,student_all_data,number_of_tests_taken,TestStatus,TestStatus_aimode
from django.utils.safestring import mark_safe
from django.utils.html import format_html



# django question panelinin görünümünü özelleştirme
#admin tarafında soruları kaydettikten sonra tablo şeklinde tüm soruların görünüm kısmını özelleştirir.Yapmak zorunda degiliz.


class teststatus_development_mode(admin.ModelAdmin):
    list_display=(["user","display_current_question"])
    search_fields=(["user"])
    def display_current_question(self, obj):
        # current_question değerine 1 ekleyip göster
        return obj.current_question + 1
class teststatus_ai_mode(admin.ModelAdmin):
    list_display=(["user","display_current_question","current_theta"])
    search_fields=(["user"])
    def display_current_question(self, obj):
        # current_question değerine 1 ekleyip göster
        return obj.current_question + 1

class question_seems(admin.ModelAdmin):
    list_display=(["id","question_description","corrected_course_id"])
    list_display_links = (["question_description"])
    search_fields=(["question_description"])
    list_filter=(["course_id__course_name"])
    #list_editable=(["question_description"])
    #readonly_fields=(["question_description"])
    
    # soru tanımlama ekraninda course_id yerine id karsilik gelen  dersin ismini gösterir soru hangi derse aitse onu gösterir
    def corrected_course_id(self,obj):
       return obj.course_id.course_name

    '''def corrected_question_description(self,obj):
       return mark_safe(obj.question_description)     question sayfasının görünümü marksafe ile html kodunu yorumlayıp öyle gösterir ekranda <h1> hello world</h1> şeklinde degil h1 etiketi özelliklerine göre yazar ekrana'''
    
    #  corrected_question_description.short_description = 'Content'

class course_seems(admin.ModelAdmin):
    list_display=(["course_name","id","development_mode"])
    list_display_links = (["course_name"])
    list_filter=(["course_name"])
    search_fields = ['course_name']


class studentdata_seems(admin.ModelAdmin):
    list_display=(["id","student_name","student_course"])
    list_display_links = (["student_name"])
    list_filter=(["courseid__course_name"])
    search_fields = ['userid_tested__username', 'courseid_tested__course_name']

    def student_name(self,obj):
        return obj.userid.username
    
    def student_course(self,obj):
       return obj.courseid.course_name
# özelleştrilmis admin panel kullanmak istiyorisek admin.site.register(question,question_seems) seklinde tanımlamamız gerek    
# Register your models here.    
#yukarıdaki bütün tanimlamalar admin panel görünümü özellestirmek icin  yapılır
class number_of_tests_taken_seems(admin.ModelAdmin):
    list_display=(["get_username","student_course","date_taken","development_mode_is_active","Total_grade"])
    list_filter=(["userid_tested__username","courseid_tested__course_name","date_taken","development_mode_is_active"])
    search_fields = ['userid_tested__username', 'courseid_tested__course_name']
    def get_username(self, obj):
        return obj.userid_tested.username
    
    def student_course(self,obj):
       return obj.courseid_tested.course_name
    class Meta:
        verbose_name = "User Test Results"
        verbose_name_plural = "Custom Test Results"

# admin giriş sayfasını ozellestirme
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
class CustomAdminSite(AdminSite):
    site_header = _('Admin Login Page')

custom_admin_site = CustomAdminSite(name='customadmin')

teststatus_ai_mode
admin.site.register(TestStatus,teststatus_development_mode)
admin.site.register(TestStatus_aimode,teststatus_ai_mode)
admin.site.register(question,question_seems)
admin.site.register(courses,course_seems)
admin.site.register(student_all_data,studentdata_seems)
admin.site.register(number_of_tests_taken,number_of_tests_taken_seems)

'''
#admin panelinden course tanımlarken aynı ekranda question da tanımlayabiliriz
class QuestionInline(admin.StackedInline):
    model = question
    extra = 1
class CourseAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]

admin.site.register(courses, CourseAdmin)
    '''