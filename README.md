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
### Örnek Test:
- **Başlangıç**: AŞTİ
- **Bitiş**: Sincan
- **Sonuç**:  
  `Fastest Route: AŞTİ -> Kızılay -> Ulus -> Demetevler -> OSB -> Sincan (X dk)`  
  `Minimum Transfers Route: AŞTİ -> Kızılay -> Ulus -> Demetevler -> OSB -> Sincan`

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


























# Sürücüsüz Metro Simülasyonu (Rota Optimizasyonu)

Bu proje, bir metro ağında en hızlı ve en az aktarmalı rotaları bulan bir simülasyon geliştirmeyi amaçlar. Proje, gerçek dünya problemlerini algoritmik düşünce ile çözmeyi hedefler.

## Kullanılan Teknolojiler ve Kütüphaneler

*   **Python:** Projenin temel geliştirme dili olarak kullanılmıştır. Python, basit sözdizimi ve geniş kütüphane desteği sayesinde hızlı ve etkili bir geliştirme süreci sunar.

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

## Algoritmaların Çalışma Mantığı

### BFS Algoritması (En Az Aktarmalı Rota Bulma)

BFS (Breadth-First Search) algoritması, bir graf üzerinde en kısa yolu bulmak için kullanılan bir arama algoritmasıdır. Bu projede, iki istasyon arasındaki en az aktarmalı rotayı bulmak için kullanılmıştır.

*   **Çalışma Mantığı:**
    1.  Bir kuyruk (deque) oluşturulur ve başlangıç istasyonu bu kuyruğa eklenir.
    2.  Ziyaret edilen istasyonları takip etmek için bir küme (set) kullanılır.
    3.  Kuyruk boş olmadığı sürece, kuyruğun başındaki istasyon alınır.
    4.  Alınan istasyonun komşu istasyonları ziyaret edilir.
    5.  Komşu istasyonlar ziyaret edilmemişse, rotaya eklenir ve kuyruğa eklenir.
    6.  Hat geçişleri maliyetli (1) ve aynı hatta kalmak ücretsiz (0) olarak değerlendirilir.
    7.  Hedef istasyona ulaşılana kadar bu işlem tekrarlanır.
    8.  En kısa rota bulunduğunda, rota döndürülür.

### A\* Algoritması (En Hızlı Rota Bulma)

A\* algoritması, bir graf üzerinde en kısa yolu bulmak için kullanılan bir arama algoritmasıdır. BFS'ye benzer ancak ek olarak bir "sezgisel" (heuristic) fonksiyon kullanır. Bu projede, iki istasyon arasındaki en hızlı rotayı bulmak için kullanılmıştır.

*   **Çalışma Mantığı:**
    1.  Bir öncelik kuyruğu (heapq) oluşturulur ve başlangıç istasyonu bu kuyruğa eklenir.
    2.  Ziyaret edilen istasyonları takip etmek için bir küme (set) kullanılır.
    3.  Kuyruk boş olmadığı sürece, en düşük maliyetli istasyon kuyruktan alınır.
    4.  Alınan istasyonun komşu istasyonları ziyaret edilir.
    5.  Her komşu istasyon için bir maliyet hesaplanır (gerçek maliyet + sezgisel maliyet).
    6.  Sezgisel fonksiyon, hedef istasyona olan uzaklığı tahmin etmek için kullanılır (örneğin, Öklid mesafesi).
    7.  En düşük maliyetli komşu istasyon, öncelik kuyruğuna eklenir.
    8.  Hedef istasyona ulaşılana kadar bu işlem tekrarlanır.
    9.  En hızlı rota bulunduğunda, rota ve toplam süre döndürülür.

### Neden Bu Algoritmalar Kullanıldı?

*   BFS, en az aktarmalı rotayı bulmak için uygundur çünkü her adımda en yakın istasyonları ziyaret eder ve hat geçişlerini minimize etmeye odaklanır.
*   A\*, en hızlı rotayı bulmak için uygundur çünkü sezgisel fonksiyon sayesinde daha bilinçli bir arama yapar ve daha hızlı sonuçlar elde edebilir.

## Örnek Kullanım ve Test Sonuçları

Proje, örnek bir metro ağı üzerinde test edilmiştir. Örnek kullanım ve test sonuçları aşağıda verilmiştir:

### Örnek Metro Ağı
    ![image](https://github.com/user-attachments/assets/1869c931-b40e-487e-b7eb-e9c29b15d246)
