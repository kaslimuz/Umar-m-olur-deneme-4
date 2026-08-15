import pygame
import random
import math

# --- KURULUM VE SABİTLER ---
pygame.init()

GENISLIK = 1060
YUKSEKLIK = 2010
ekran = pygame.display.set_mode((GENISLIK, YUKSEKLIK))
pygame.display.set_caption("Space Shooter")

SAAT = pygame.time.Clock()
FPS = 60

# RENKLER
SIYAH = (10, 10, 20)
BEYAZ = (255, 255, 255)
SARI = (255, 235, 59)
KIRMIZI = (244, 67, 54)
GRI = (158, 158, 158)
ACIK_GRI = (220, 220, 220)

# SKIN RENKLERİ
SKINLER = [
    {"ad": "NEON MAVİ", "renk": (0, 229, 255), "kilitli": False},
    {"ad": "ALEV KIRMIZI", "renk": (255, 87, 34), "kilitli": False},
    {"ad": "ZÜMRÜT YEŞİL", "renk": (0, 230, 118), "kilitli": False}
]
secili_skin_idx = 0

FONT_BUYUK = pygame.font.SysFont("Arial", 80, bold=True)
FONT_ORTA = pygame.font.SysFont("Arial", 50, bold=True)
FONT_KUCUK = pygame.font.SysFont("Arial", 35)

# --- SIFIRLAMA VE DEĞİŞKENLER ---
durum = "MENU"  # MENU, OYUN, SKIN_SECI
skor = 0
yuksek_skor = 0

# Oyuncu Ayarları
GEMI_GENISLIK = 90
GEMI_YUKSEKLIK = 110
gemi_x = (GENISLIK - GEMI_GENISLIK) // 2
gemi_y = YUKSEKLIK - 250
GEMI_HIZI = 16  # Sağa-sola gitme hızı (dengeli)

mermiler = []
MERMI_HIZI = 28
ates_bekleme = 0

dusmanlar = []
DUSMAN_HIZI = 7
dusman_üretim_suresi = 0

patlamalar = []

# Arka Plan Yıldızları (Parallaks Efekti)
yildizlar = []
for _ in range(80):
    yildizlar.append([
        random.randint(0, GENISLIK),
        random.randint(0, YUKSEKLIK),
        random.randint(1, 4),
        random.randint(2, 6)
    ])

def oyunu_sifirla():
    global gemi_x, gemi_y, mermiler, dusmanlar, patlamalar, skor, DUSMAN_HIZI
    gemi_x = (GENISLIK - GEMI_GENISLIK) // 2
    gemi_y = YUKSEKLIK - 250
    mermiler.clear()
    dusmanlar.clear()
    patlamalar.clear()
    skor = 0
    DUSMAN_HIZI = 7

# --- ÇİZİM FONKSİYONLARI ---
def gemi_ciz(x, y, renk):
    # Motor Alevi
    alevi_y = y + GEMI_YUKSEKLIK
    pygame.draw.polygon(ekran, SARI, [
        (x + 25, alevi_y),
        (x + GEMI_GENISLIK - 25, alevi_y),
        (x + GEMI_GENISLIK // 2, alevi_y + random.randint(20, 40))
    ])
    # Ana Gövde
    noktalar = [
        (x + GEMI_GENISLIK // 2, y),
        (x, y + GEMI_YUKSEKLIK),
        (x + GEMI_GENISLIK // 2, y + GEMI_YUKSEKLIK - 20),
        (x + GEMI_GENISLIK, y + GEMI_YUKSEKLIK)
    ]
    pygame.draw.polygon(ekran, renk, noktalar)
    pygame.draw.polygon(ekran, BEYAZ, noktalar, 4)
    # Kokpit
    pygame.draw.ellipse(ekran, ACIK_GRI, (x + GEMI_GENISLIK // 2 - 12, y + 35, 24, 35))

def buton_ciz(metin, x, y, w, h, pasif_renk, aktif_renk, dokunuldu):
    renk = aktif_renk if dokunuldu else pasif_renk
    pygame.draw.rect(ekran, renk, (x, y, w, h), border_radius=20)
    pygame.draw.rect(ekran, BEYAZ, (x, y, w, h), width=4, border_radius=20)
    
    yazi = FONT_ORTA.render(metin, True, BEYAZ)
    yazi_kutusu = yazi.get_rect(center=(x + w // 2, y + h // 2))
    ekran.blit(yazi, yazi_kutusu)

# --- ANA DÖNGÜ ---
calisiyor = True
surukleniyor = False

while calisiyor:
    SAAT.tick(FPS)
    dokunma_pos = None

    # OLAYLAR (EVENTS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            calisiyor = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            surukleniyor = True
            dokunma_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            surukleniyor = False

        elif event.type == pygame.MOUSEMOTION and surukleniyor and durum == "OYUN":
            # Parmağı takip ederek sağa-sola gitme
            parmak_x = event.pos[0]
            hedef_x = parmak_x - GEMI_GENISLIK // 2
            
            # Yumuşak ve hızlı takip
            if abs(hedef_x - gemi_x) > 5:
                if hedef_x > gemi_x:
                    gemi_x += min(GEMI_HIZI, hedef_x - gemi_x)
                else:
                    gemi_x -= min(GEMI_HIZI, gemi_x - hedef_x)

    # Ekran Sınır Kontrolü
    gemi_x = max(20, min(GENISLIK - GEMI_GENISLIK - 20, gemi_x))

    # ARKA PLAN (YILDIZLAR)
    ekran.fill(SIYAH)
    for yildiz in yildizlar:
        yildiz[1] += yildiz[3]
        if yildiz[1] > YUKSEKLIK:
            yildiz[1] = 0
            yildiz[0] = random.randint(0, GENISLIK)
        pygame.draw.circle(ekran, BEYAZ, (yildiz[0], yildiz[1]), yildiz[2])

    # --- DURUM: ANA MENÜ ---
    if durum == "MENU":
        baslik = FONT_BUYUK.render("SPACE SHOOTER", True, SKINLER[secili_skin_idx]["renk"])
        ekran.blit(baslik, baslik.get_rect(center=(GENISLIK // 2, 400)))

        skor_yazisi = FONT_ORTA.render(f"EN YÜKSEK SKOR: {yuksek_skor}", True, SARI)
        ekran.blit(skor_yazisi, skor_yazisi.get_rect(center=(GENISLIK // 2, 550)))

        # Butonlar
        basla_b = pygame.Rect(GENISLIK // 2 - 250, 900, 500, 120)
        skin_b = pygame.Rect(GENISLIK // 2 - 250, 1080, 500, 120)

        dokun_basla = dokunma_pos and basla_b.collidepoint(dokunma_pos)
        dokun_skin = dokunma_pos and skin_b.collidepoint(dokunma_pos)

        buton_ciz("OYUNA BAŞLA", basla_b.x, basla_b.y, basla_b.w, basla_b.h, (0, 150, 0), (0, 200, 0), dokun_basla)
        buton_ciz("SKİNLER GARAJI", skin_b.x, skin_b.y, skin_b.w, skin_b.h, (150, 100, 0), (200, 130, 0), dokun_skin)

        # Seçili Gemi Önizleme
        gemi_ciz(GENISLIK // 2 - GEMI_GENISLIK // 2, 1400, SKINLER[secili_skin_idx]["renk"])

        if dokunma_pos:
            if basla_b.collidepoint(dokunma_pos):
                oyunu_sifirla()
                durum = "OYUN"
            elif skin_b.collidepoint(dokunma_pos):
                durum = "SKIN_SECI"

    # --- DURUM: SKİN SEÇİMİ ---
    elif durum == "SKIN_SECI":
        baslik = FONT_BUYUK.render("SKİN GARAJI", True, BEYAZ)
        ekran.blit(baslik, baslik.get_rect(center=(GENISLIK // 2, 300)))

        # Aktif Skin Önizleme
        gemi_ciz(GENISLIK // 2 - GEMI_GENISLIK // 2, 550, SKINLER[secili_skin_idx]["renk"])
        
        ad_yazisi = FONT_ORTA.render(SKINLER[secili_skin_idx]["ad"], True, SKINLER[secili_skin_idx]["renk"])
        ekran.blit(ad_yazisi, ad_yazisi.get_rect(center=(GENISLIK // 2, 720)))

        # Değiştirme Butonları
        sol_b = pygame.Rect(150, 570, 120, 120)
        sag_b = pygame.Rect(GENISLIK - 270, 570, 120, 120)
        ana_menu_b = pygame.Rect(GENISLIK // 2 - 250, 1300, 500, 120)

        buton_ciz("<", sol_b.x, sol_b.y, sol_b.w, sol_b.h, GRI, ACIK_GRI, False)
        buton_ciz(">", sag_b.x, sag_b.y, sag_b.w, sag_b.h, GRI, ACIK_GRI, False)
        buton_ciz("ANA MENÜ", ana_menu_b.x, ana_menu_b.y, ana_menu_b.w, ana_menu_b.h, (150, 0, 0), (200, 0, 0), False)

        if dokunma_pos:
            if sol_b.collidepoint(dokunma_pos):
                secili_skin_idx = (secili_skin_idx - 1) % len(SKINLER)
            elif sag_b.collidepoint(dokunma_pos):
                secili_skin_idx = (secili_skin_idx + 1) % len(SKINLER)
            elif ana_menu_b.collidepoint(dokunma_pos):
                durum = "MENU"

    # --- DURUM: OYNANIŞ ---
    elif durum == "OYUN":
        # Otomatik Ateş
        ates_bekleme += 1
        if ates_bekleme >= 12:
            mermiler.append([gemi_x + GEMI_GENISLIK // 2 - 6, gemi_y])
            ates_bekleme = 0

        # Mermileri İlerlet
        for mermi in mermiler[:]:
            mermi[1] -= MERMI_HIZI
            if mermi[1] < -20:
                mermiler.remove(mermi)
            else:
                pygame.draw.rect(ekran, SARI, (mermi[0], mermi[1], 12, 30), border_radius=6)

        # Düşman Üretimi
        dusman_üretim_suresi += 1
        if dusman_üretim_suresi >= 35:
            r = random.randint(35, 65)
            dusmanlar.append([random.randint(r, GENISLIK - r), -r, r])
            dusman_üretim_suresi = 0

        # Düşmanları İlerlet ve Çarpışmaları Kontrol Et
        for dusman in dusmanlar[:]:
            dusman[1] += DUSMAN_HIZI
            # Düşman Çizimi (Göktaşı)
            pygame.draw.circle(ekran, GRI, (dusman[0], dusman[1]), dusman[2])
            pygame.draw.circle(ekran, BEYAZ, (dusman[0], dusman[1]), dusman[2], 4)

            # Mermi - Düşman Çarpışması
            for mermi in mermiler[:]:
                mesafe = math.hypot(mermi[0] - dusman[0], mermi[1] - dusman[1])
                if mesafe < dusman[2]:
                    # Patlama Parçacıkları
                    for _ in range(12):
                        patlamalar.append([dusman[0], dusman[1], random.randint(-8, 8), random.randint(-8, 8), 15])
                    
                    if mermi in mermiler: mermiler.remove(mermi)
                    if dusman in dusmanlar: dusmanlar.remove(dusman)
                    skor += 10
                    if skor > yuksek_skor: yuksek_skor = skor
                    # Zorlaştırma
                    if skor % 100 == 0: DUSMAN_HIZI += 1
                    break

            # Gemi - Düşman Çarpışması veya Alt Sınıra Ulaşma (Game Over)
            gemi_merkez = (gemi_x + GEMI_GENISLIK // 2, gemi_y + GEMI_YUKSEKLIK // 2)
            if math.hypot(gemi_merkez[0] - dusman[0], gemi_merkez[1] - dusman[1]) < dusman[2] + 35 or dusman[1] > YUKSEKLIK + 50:
                durum = "MENU"

        # Patlamaları Güncelle ve Çiz
        for p in patlamalar[:]:
            p[0] += p[2]
            p[1] += p[3]
            p[4] -= 1
            if p[4] <= 0:
                patlamalar.remove(p)
            else:
                pygame.draw.circle(ekran, KIRMIZI, (p[0], p[1]), p[4])

        # Oyuncu Gemisini Çiz
        gemi_ciz(gemi_x, gemi_y, SKINLER[secili_skin_idx]["renk"])

        # Skor Arayüzü (UI)
        skor_t = FONT_ORTA.render(f"SKOR: {skor}", True, BEYAZ)
        ekran.blit(skor_t, (40, 60))

    pygame.display.flip()

pygame.quit()
