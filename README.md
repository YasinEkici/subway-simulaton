# 🚇 Driverless Metro Simulation

Bu proje, **graf tabanlı bir metro ağı üzerinde rota optimizasyonu** yapmayı amaçlayan interaktif bir simülasyon arayüzüdür. Kullanıcılar iki istasyon arasında **en hızlı rota (A*)** veya **en az aktarmalı rota (BFS)** seçeneklerini seçerek ideal güzergahı bulabilir. Proje bir GUI arayüzü, görselleştirme, arama, animasyon ve tema seçenekleriyle zenginleştirilmiştir.

---

## 🛠️ Kullanılan Teknolojiler ve Kütüphaneler

| Teknoloji/Kütüphane | 
|---------------------|
| `tkinter`           | 
| `matplotlib`        | 
| `networkx`          | 
| `heapq`             | 
| `collections.deque` | 
| `itertools`         | 
| `math`              | 
| `typing`            | 

*   **Tkinter:**
    *   Grafik kullanıcı arayüzü (GUI) geliştirmek için kullanılmıştır.
    *   Python'ın standart GUI kütüphanesidir.
    *   Kullanıcı etkileşimli pencereler, düğmeler, giriş alanları ve diğer GUI bileşenlerini oluşturmayı sağlar.
    *   Bu proje, kullanıcıların metro ağını görselleştirmesi ve rota hesaplama işlemlerini gerçekleştirmesi için Tkinter kullanılarak geliştirilmiş bir GUI sunar.

*   **networkx:**
    *   Graf veri yapılarını oluşturmak, manipüle etmek ve analiz etmek için kullanılmıştır.
    *   Düğümler, kenarlar ve özellikler içeren karmaşık ağ yapılarını temsil etmeyi sağlar.
    *   Bu proje, metro ağını bir graf olarak modellemek ve rota bulma algoritmalarını uygulamak için networkx kütüphanesini kullanır.

*   **matplotlib:**
    *   Grafikleri ve görselleştirmeleri oluşturmak için kullanılmıştır.
    *   Çeşitli grafik türlerini (çizgi grafikleri, dağılım grafikleri, çubuk grafikleri vb.) oluşturmayı sağlar.
    *   Bu proje, metro ağını ve rota sonuçlarını görsel olarak temsil etmek için matplotlib kütüphanesini kullanır.

*   **collections.deque:**
    *   BFS (Breadth-First Search) algoritması için çift uçlu bir kuyruk (deque) veri yapısını oluşturmak için kullanılmıştır.
    *   Kuyruğun her iki ucundan da ekleme ve çıkarma işlemlerini verimli bir şekilde gerçekleştirmeyi sağlar.
    *   BFS algoritması, istasyonları ziyaret sırasına göre işlemek için bir kuyruk kullanır.

*   **heapq:**
    *   A\* algoritması için öncelik kuyruğunu (priority queue) oluşturmak için kullanılmıştır.
    *   En küçük elemana hızlı erişim sağlayan bir yığın (heap) veri yapısıdır.
    *   A\* algoritması, en düşük maliyetli istasyonları önceliklendirmek için bir öncelik kuyruğu kullanır.

*   **typing:**
    *   Tip ipuçları (type hints) için kullanılmıştır.
    *   Kodun okunabilirliğini ve bakımını artırmak için değişkenlerin ve fonksiyonların tiplerini belirtmeyi sağlar.
    *   Bu proje, kodun daha anlaşılır ve hatasız olmasını sağlamak için tip ipuçlarını kullanır.

*   **itertools:**
    *   Sayaç (counter) oluşturmak için kullanılmıştır.
    *   A\* algoritması, istasyonları ziyaret sırasına göre etiketlemek için bir sayaç kullanır.

*   **math:**
    *   Matematiksel işlemler için kullanılmıştır.
    *   A\* algoritması, sezgisel fonksiyonu (heuristic function) hesaplamak için matematiksel fonksiyonları kullanır.
---

## ⚙️ Algoritmaların Çalışma Mantığı

### 🔄 BFS (Breadth-First Search) - Minimum Aktarma Rotası
- **Amaç**: İki istasyon arasındaki **en az hat değişimiyle** rotayı bulmak.
- **Yapı**: `deque` kullanılarak kuyruk temelli genişlik öncelikli arama yapılır.
- **Maliyet Sistemi**:
  - Aynı hat üzerindeyse maliyet **0**
  - Farklı hatta geçiliyorsa maliyet **1**
- **Çalışma Mantığı:**
    1.  Bir kuyruk (deque) oluşturulur ve başlangıç istasyonu bu kuyruğa eklenir.
    2.  Ziyaret edilen istasyonları takip etmek için bir küme (set) kullanılır.
    3.  Kuyruk boş olmadığı sürece, kuyruğun başındaki istasyon alınır.
    4.  Alınan istasyonun komşu istasyonları ziyaret edilir.
    5.  Komşu istasyonlar ziyaret edilmemişse, rotaya eklenir ve kuyruğa eklenir.
    6.  Hat geçişleri maliyetli (1) ve aynı hatta kalmak ücretsiz (0) olarak değerlendirilir.
    7.  Hedef istasyona ulaşılana kadar bu işlem tekrarlanır.
    8.  En kısa rota bulunduğunda, rota döndürülür.
- **Neden Kullanıldı**: Transfer sayısı bir rota kalitesi ölçütü olarak baz alındığında en verimli çözümdür.

### 🚀 A* (A-Star Search) - En Hızlı Rota
- **Amaç**: İki istasyon arasındaki **toplam seyahat süresi** açısından en kısa rotayı bulmak.
- **Heuristik**: Öklid mesafesi (x, y koordinatları kullanılarak) hedefe olan tahmini mesafeyi hesaplar.
- **Yapı**: `heapq` ile öncelik kuyruğu; en düşük `f(n) = g(n) + h(n)` değerine sahip düğüm önceliklidir.
- **Çalışma Mantığı:**
    1.  Bir öncelik kuyruğu (heapq) oluşturulur ve başlangıç istasyonu bu kuyruğa eklenir.
    2.  Ziyaret edilen istasyonları takip etmek için bir küme (set) kullanılır.
    3.  Kuyruk boş olmadığı sürece, en düşük maliyetli istasyon kuyruktan alınır.
    4.  Alınan istasyonun komşu istasyonları ziyaret edilir.
    5.  Her komşu istasyon için bir maliyet hesaplanır (gerçek maliyet + sezgisel maliyet).
    6.  Sezgisel fonksiyon, hedef istasyona olan uzaklığı tahmin etmek için kullanılır (örneğin, Öklid mesafesi).
    7.  En düşük maliyetli komşu istasyon, öncelik kuyruğuna eklenir.
    8.  Hedef istasyona ulaşılana kadar bu işlem tekrarlanır.
    9.  En hızlı rota bulunduğunda, rota ve toplam süre döndürülür.
- **Neden Kullanıldı**: Gerçekçi süre optimizasyonu sağlar ve navigasyon sistemlerinde sıkça kullanılır.

---
## GUI Ekranı Özellikleri:
- İstasyon seçimi (`Start`, `End`) 
- Rota türü seçimi (`Fastest`, `Minimum Transfers`)
- Canlı animasyon ve güzergah vurgulama
- Zoom, dark/light mode
- Kenar sayılarını kaldırma
- İstasyon arama, highlight'lama
- İstasyon bilgilerini gösterme
- Hat bilgilerini gösterme

---

## 📊 Örnek Kullanım & Test Sonuçları
### Örnek Test 1:
- **Başlangıç**: AŞTİ
- **Bitiş**: Sincan
- **Sonuç**:  
  `Fastest Route: AŞTİ -> Kızılay -> Ulus -> Demetevler -> OSB -> Sincan (35 dk)`
  ![image](https://github.com/user-attachments/assets/10b64cb6-0ce0-432f-b06f-8d0473199786)

  `Minimum Transfers Route: AŞTİ -> Kızılay -> Ulus -> Demetevler -> OSB -> Sincan`
  ![image](https://github.com/user-attachments/assets/b5272758-04a4-41e5-8424-1255304b1518)

### Örnek Test 2:
- **Başlangıç**: Dikmen
- **Bitiş**: Bostancı
- **Sonuç**:
   `Fastest Route: Dikmen -> Övençler -> Konukkent -> Bilkent -> Emek -> Bahçeliever -> AŞTİ -> Kızılay -> Moda -> Bostancı  (42 dk)`
  ![image](https://github.com/user-attachments/assets/d76daa62-5c7d-4541-86a7-ccf397a14cb1)

   `Minimum Transfers Route: Dikmen -> Övençler -> Konukkent -> Oran -> Kadıköy -> Moda -> Bostancı
  ![image](https://github.com/user-attachments/assets/4d50ee9f-df05-4da2-9845-33d1fd7e84ac)

  

---

## 💡 Geliştirme Fikirleri

- ✅ Metro haritası üzerinde gerçek zamanlı animasyon rotası
- ✅ Dark/Light mode
- ✅ İstasyon arama ve tıklayınca detayları gösterme
- 📌 Durak yoğunluk verisi entegrasyonu (örneğin saatlik yoğunluk)
- 📌 Mobil uyumlu web tabanlı sürüm (örnek: Streamlit, Flask)
- 📌 Hata toleranslı arama sistemi (yazım hatalarını algılama)
- 📌 JSON/CSV veri dosyasından metro verisi çekme

---

## 📁 Kurulum

```bash
# Gereksinimleri yükleyin
pip install matplotlib networkx

# Projeyi çalıştırın
python dosya_adi.py




















