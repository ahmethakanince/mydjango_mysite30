from blog.models import question,student_all_data,courses
import pandas as pd
import numpy as np
from scipy.special import expit
import time

global student_answer_dataframe

def calculate_question_difficulty(student_answers_dataframe):
    
    # Sütunlardaki NaN değerleri dikkate almadan ortalama al
    average_of_colums_difficulty = 1-(student_answers_dataframe.mean(skipna=True)) 
    # DataFrame'deki değerleri normalize et
    min_val = average_of_colums_difficulty.min().min()  # DataFrame içindeki en küçük değer
    max_val = average_of_colums_difficulty.max().max()  # DataFrame içindeki en büyük değer

    # mean_of_colums_difficulty ile soruların ortalaması hesaplanarak alınan diffulty degerlerini ...
    # en yüksek degeri zorluk derecesi 1 en düşün zorluk derecesine(0) olan soruyu -1 eşitleyecek şekilde normalize eder
    # normalized dataframe yazar
    normalized_diffulty= average_of_colums_difficulty.apply(lambda x: (x - min_val) / (max_val - min_val) * 2 - 1)

    # Her bir sütunun toplamını alıp yeni bir DataFrame oluştur(yukarıdaki tüm dataframaleri birlestirir.)
    Combineddataframe = pd.DataFrame({'question_columns': student_answers_dataframe.columns, 'SummationOfTrueAnswers': student_answers_dataframe.sum(),'AverageOfStudentAnswers(difficulty)':average_of_colums_difficulty,'Normalized_difficulty':normalized_diffulty}).set_index('question_columns') 
    # Combineddataframe = question id'sine göre hangi soruya kaçtane dogru cevap verilmiş (NaN degerlerini pass geçer)
    # Combineddataframe= question id sine göre cevap toplam dogru cevap sayısını/ toplam cevaplama sayısına bölerek sorunun diffulty hesaplar ve Combineddataframe column olarak verir (NaN degerlerini pass geçer)
    return Combineddataframe

def get_data_from_view(student_answer_datas_table):
    # Pandas DataFrame oluştur
    # DataFrame'e dönüştür, eksik değerleri NaN yap
    student_answer_dataframe = pd.DataFrame.from_dict(student_answer_datas_table, orient='index').transpose()
    CombinedAlldataframe=calculate_question_difficulty(student_answer_dataframe)
    return CombinedAlldataframe



# thetaya en yakın zorluk seviyesine(Normalized diffuculty)sahip sorunun question_id bulma
def calculate_closes_question(student_answer_dataframe,answer_condition_array,theta_old):
    
    # DataFrame'in indeks numaralarını al
    question_id_numbers = student_answer_dataframe.index.tolist()
    
    # answer_condition_array'da bulunmayan değerleri filtrele(cevaplanmamış soruları bul) question_id bulur
    not_answered_question_ids = result = [value for value in question_id_numbers if value not in answer_condition_array]
   
    # Belirtilen indekslere(question_id) sahip verileri alın
    selected_not_answered_data = student_answer_dataframe[student_answer_dataframe.index.isin(not_answered_question_ids)]
    #diffulty satırından Veri çıkartıldıktan sonra, mutlak değeri en küçük olan değerin indeksi bul
    # Belirli bir sütundaki tüm değerlerden theta çıkartın
    selected_not_answered_data = selected_not_answered_data.copy() # pandas kütüphanesi uyarı verdiği için bu işlem yapıldı
    selected_not_answered_data['min_values'] = (selected_not_answered_data['Normalized_difficulty']-theta_old)
    # Mutlak değeri en küçük olan değerin indeksini(quesiton_id) bulur (question_id string olarak verir)
    min_abs_index = (selected_not_answered_data['min_values'].abs()).idxmin()

    return min_abs_index

def main(student_answer_dataframe,answer_condition_array,answer,theta_old):#answer aklenecek dogru ise 1 yanlış ise 0 #theta_old eklenecek

    min_abs_index=calculate_closes_question(student_answer_dataframe,answer_condition_array,theta_old)
    b= student_answer_dataframe.loc[min_abs_index,'Normalized_difficulty']
    k = 0.6
    if answer == 1:
        x = 1
        probability = expit(b - theta_old)
        theta_new = theta_old + k * (x - probability)
        return min_abs_index,theta_new 
        
    if answer==0:
        x = 0
        probability = expit(theta_old - b)
        theta_new = theta_old + k * (x - probability)
        return min_abs_index,theta_new
            

          

      
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures

def train_extra_grade_model(answer_time,average_student_time,difficulty):

        if(int(answer_time) >(2*average_student_time)):
             return -3
        # Ekstra puanlar: en kolay soru -1 zorluk derecesine sahip, +5 puan alacak,
        # en zor soru ise 1 zorluk derecesine sahip, +20 puan alacak
        ekstra_puan = 5 + 7.5 * (difficulty + 1)
        e=ekstra_puan  
        a = average_student_time     # İstediğiniz average_student_time_data değerini burada belirtin
        # Cevap süreleri (x) ve ekstra puanlar (y) verilerini kullanalım
        # a/3 ile a arasını 6 parçaya böl
        lower_range = np.linspace(a/3, a, 6)

        # a ile 2*a arasını 6 parçaya böl
        upper_range = np.linspace(a, 2*a, 6)

        # Her iki aralığı birleştirerek yeni bir array oluştur
        cevap_sureleri = np.concatenate([lower_range, upper_range])
        

        #cevap_sureleri = np.array([])
        ekstra_puanlar = np.array([e,e-2,e-5,e-7,e-8,e-9,0,0,0,-1,-2,-3])
        # Verileri düzenleyelim
        cevap_sureleri = cevap_sureleri.reshape(-1, 1)
        ekstra_puanlar = ekstra_puanlar.reshape(-1, 1)
        # PolynomialFeatures kullanarak kubik regresyon için yeni özellikler ekleyelim
        poly = PolynomialFeatures(degree=3)
        cevap_sureleri_poly = poly.fit_transform(cevap_sureleri)

        # Lineer regresyon modelini oluşturalım ve eğitelim
        model = LinearRegression()
        model.fit(cevap_sureleri_poly, ekstra_puanlar)

        x = np.array([[answer_time]])
        x_poly = poly.transform(x)
        y_pred = model.predict(x_poly)
        return y_pred

#grading_student(theta_old, student_all_data, difficulty_matrix)
def grading_student(theta_student):#, student_data, difficulty_matrix)
    # grading_student fonksiyonunu buraya ekleyin
    # Örnek sayılar
    values = theta_student
    # -3 ile 3 arasındaki sayıları 0 ile 100 arasına çevirme
    old_min = -2.70
    old_max = 0.74
    new_min = 0
    new_max = 100
    scaled_values = ((values - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
    return scaled_values
    
    #train_extra_grade_model(answer_time,average_student_time_data,difficulty)

    #dogru cevaba,sorunun ortalama zamana ve sorunun zorluk katsayısına göre ortlama sürenin altında ve üstünde olcak şekilde model oluştur 
'''
    # cevap verilen soru sayısı
    answered_question_num = len(student_data)
    # soruların difficulty sayısı kadar süre sayısını oluşturuyorum (1dk - 10 dk arasında soru sayısı kadar bölüyorsun)
    time_range = np.linspace(60, 600, num=len(difficulty_matrix))

    # Burada belirtilen sürelerin %40 daha aşağı cevap verdiyse ekstra puan alacak
    extra_time_range = 0.6 * time_range

    # Toplam sorulan soru sayısındaki extra puan alımını denetlemek için
    i = 0
    extra_grade = 0

    # Eğer öğrenci belirli bir sürenin altında cevap verdiyse soruya sorunun zorluk derecesine paralel olarak extra puan kazanır.
    while i < answered_question_num:
        i += 1
        if student_data[i - 1][1] < extra_time_range[i - 1] and student_data[i - 1][2] == "TRUE":
            extra_grade += abs(difficulty_matrix[i - 1])

    print("Extra Grade:", extra_grade)

# Örnek kullanım
#grading_student([1.2, -0.5, 0.8], [[1, 120, 'TRUE'], [0, 180, 'TRUE'], [1, 90, 'FALSE']], [0.2, -0.1, 0.5])
'''
