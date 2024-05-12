-- PowerShell Command:
-- Get-Content ".\sqlite.sql" | & sqlite3.exe ".\db.sqlite3"

-- Bash Command:
-- sqlite3 db.sqlite3 < sqlite.sql



PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS musteriler;
CREATE TABLE musteriler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    musteri_tckn VARCHAR(11) NOT NULL UNIQUE, -- 11 haneli
    musteri_telefon VARCHAR(11) NOT NULL, -- 5331234567
    musteri_cinsiyet VARCHAR(1) NOT NULL, -- E: Erkek, K: Kadın D: Diğer
    musteri_dogum DATE NOT NULL, -- YYYY-MM-DD
    musteri_email VARCHAR(255) DEFAULT NULL,
    musteri_sifre VARCHAR(255) NOT NULL,
    musteri_adres VARCHAR(255) NOT NULL,
    musteri_ad VARCHAR(50) NOT NULL,
    musteri_soyad VARCHAR(50) NOT NULL,
    musteri_profil VARCHAR(255) DEFAULT '/static/img/profile.svg',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

DROP TABLE IF EXISTS abonmanlar;
CREATE TABLE abonmanlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    musteri_id INT NOT NULL,
    abonman_no VARCHAR(16) NOT NULL, -- 1111-2222-3333-4444
    abonman_bas_tarih DATETIME NOT NULL,
    abonman_son_tarih DATETIME NOT NULL,
    abonman_active BOOLEAN NOT NULL DEFAULT 0, -- 0: Pasif, 1: Aktif
    abonman_bakiye DECIMAL(10, 2) DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (musteri_id) REFERENCES musteriler(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS kategoriler;
CREATE TABLE kategoriler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kategori_ad VARCHAR(255) NOT NULL,
    kategori_resim VARCHAR(255) DEFAULT 'assets/icon/urun.svg',
    kategori_aciklama VARCHAR(255) NOT NULL
);

DROP TABLE IF EXISTS urunler;
CREATE TABLE urunler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    kategori_id INT NOT NULL,
    urun_ad VARCHAR(255) NOT NULL,
    urun_fiyat DECIMAL(10, 2) NOT NULL,
    urun_stok INT NOT NULL DEFAULT 0,
    urun_aciklama VARCHAR(255) DEFAULT NULL,
    urun_durum BOOLEAN NOT NULL DEFAULT 0,
    urun_resim VARCHAR(255) DEFAULT 'assets/icon/urun.svg',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (kategori_id) REFERENCES kategoriler(id)
);

DROP TABLE IF EXISTS otomatlar;
CREATE TABLE otomatlar (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    otomat_ad VARCHAR(255) NOT NULL,
    otomat_konum VARCHAR(255) NOT NULL,
    otomat_kapasite INT NOT NULL,
    otomat_durum BOOLEAN NOT NULL DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
);


DROP TABLE IF EXISTS otomat_envanter;
CREATE TABLE otomat_envanter (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    otomat_id INT NOT NULL,
    urun_id INT NOT NULL,
    envanter_adet INT NOT NULL DEFAULT 0, -- Sırada kaç adet ürün var
    envanter_sira VARCHAR(4) NOT NULL, -- A1, A2, A3, A4, B1, B2, B3, B4
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (otomat_id) REFERENCES otomatlar(id) ON DELETE CASCADE,
    FOREIGN KEY (urun_id) REFERENCES urunler(id) ON DELETE CASCADE
);

DROP TABLE IF EXISTS odemeler;
CREATE TABLE odemeler (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    envanter_id INT NOT NULL,
    abonman_id INT DEFAULT NULL,
    odeme_tutar DECIMAL(10, 2) DEFAULT 0,
    odeme_tarih DATETIME NOT NULL, -- YYYY-MM-DD HH:MM:SS
    odeme_durum BOOLEAN NOT NULL DEFAULT 0, -- 0: Başarısız, 1: Başarılı
    odeme_turu VARCHAR(255) NOT NULL, -- Kredi Kartı, Abonman, Nakit
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (envanter_id) REFERENCES otomat_envanter(id) ON DELETE CASCADE,
    FOREIGN KEY (abonman_id) REFERENCES abonmanlar(id) ON DELETE CASCADE
);

INSERT INTO auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) VALUES
(1, 'pbkdf2_sha256$720000$XQopeIn8TTtcOU4fWt4IEr$vK064gdeyDe40qJ3Wsqxes3UbsZdcUbnoa16/zN54xk=', NULL, 1, 'admin', 'ADMIN', 'ACCOUNT', 'admin@guray.local', 1, 1, '2024-04-01 00:00:00');


INSERT INTO musteriler (musteri_tckn, musteri_sifre, musteri_telefon, musteri_cinsiyet, musteri_dogum, musteri_adres, musteri_ad, musteri_soyad)
VALUES
('01234567800', '12345678' ,'5310122366', 'E', '1998-02-18', 'Bursa', 'GÜRAY', 'ALIN'),
('45678901234', '12345678' ,'5443456789', 'E', '1978-03-20', 'Bursa', 'Fatma', 'Can'),
('01234567890', '12345678' ,'5320123456', 'K', '1998-10-20', 'İstanbul', 'Ayşe', 'Yılmaz'),
('12345678901', '12345678' ,'5331234567', 'E', '1990-05-15', 'İstanbul', 'Ahmet', 'Yılmaz'),
('23456789012', '12345678' ,'5552345678', 'K', '1985-08-25', 'Ankara', 'Ayşe', 'Kara'),
('56789012345', '12345678' ,'5304567890', 'K', '1995-11-05', 'Ankara', 'Mehmet', 'Koç'),
('01234567890', '12345678' ,'5379012345', 'D', '1975-06-22', 'İzmir', 'Gülsüm', 'Güler'),
('34567890123', '12345678' ,'5323456789', 'D', '2000-12-10', 'İzmir', 'Ali', 'Demir'),
('67890123456', '12345678' ,'5315678901', 'E', '1980-07-12', 'Kütahya', 'Zeynep', 'Şahin'),
('78901234567', '12345678' ,'5346789012', 'K', '1992-04-30', 'Kütahya', 'Mustafa', 'Aydın'),
('89012345678', '12345678' ,'5387890123', 'E', '1987-09-18', 'Eskişehir', 'Hatice', 'Çelik'),
('90123456789', '12345678' ,'5368901234', 'K', '2002-01-08', 'Eskişehir', 'Hasan', 'Arslan');

INSERT INTO abonmanlar (musteri_id, abonman_no, abonman_bas_tarih, abonman_son_tarih, abonman_active, abonman_bakiye)
VALUES
(1, '1111-2222-3333-4441', '2024-03-01', '2024-04-01', 1, 500.00),
(2, '2222-3333-4444-5551', '2024-03-01', '2024-04-01', 1, 750.00),
(3, '3333-4444-5555-6661', '2024-03-01', '2024-04-01', 1, 300.00),
(4, '4444-5555-6666-7771', '2024-03-01', '2024-04-01', 1, 600.00),
(5, '5555-6666-7777-8881', '2024-03-01', '2024-04-01', 1, 400.00),
(6, '6666-7777-8888-9991', '2024-03-01', '2024-04-01', 1, 800.00),
(7, '7777-8888-9999-0001', '2024-03-01', '2024-04-01', 1, 350.00),
(8, '8888-9999-0000-1111', '2024-03-01', '2024-04-01', 1, 900.00),
(9, '9999-0000-1111-2221', '2024-03-01', '2024-04-01', 1, 450.00),
(10, '0000-1111-2222-3331', '2024-03-01', '2024-04-01', 1, 700.00),
(11, '1111-2222-3333-4442', '2024-03-01', '2024-04-01', 1, 550.00),
(12, '2222-3333-4444-5552', '2024-03-01', '2024-04-01', 1, 850.00);


INSERT INTO kategoriler (kategori_ad, kategori_aciklama) VALUES
('İçecek', 'Soğuk ve Sıcak İçecekler'),
('Atıştırmalık', 'Çerez ve Atıştırmalıklar'),
('Tatlı', 'Çikolata ve Şekerlemeler'),
('Kuruyemiş', 'Kuruyemiş ve Kuru Meyveler');

INSERT INTO urunler (kategori_id, urun_ad, urun_fiyat, urun_stok, urun_aciklama, urun_durum, urun_resim) VALUES
(1, 'Kola', 5.00, 100, 'Kola İçecek', 1, 'assets/icon/kola.svg'),
(1, 'Fanta', 5.00, 100, 'Fanta İçecek', 1, 'assets/icon/fanta.svg'),
(1, 'Sprite', 5.00, 100, 'Sprite İçecek', 1, 'assets/icon/sprite.svg'),
(1, 'Ayran', 3.00, 100, 'Ayran İçecek', 1, 'assets/icon/ayran.svg'),
(1, 'Su', 1.00, 100, 'Su İçecek', 1, 'assets/icon/su.svg'),
(2, 'Cips', 2.00, 100, 'Cips Atıştırmalık', 1, 'assets/icon/cips.svg'),
(2, 'Çikolata', 3.00, 100, 'Çikolata Atıştırmalık', 1, 'assets/icon/cikolata.svg'),
(2, 'Kurabiye', 2.00, 100, 'Kurabiye Atıştırmalık', 1, 'assets/icon/kurabiye.svg'),
(2, 'Kek', 3.00, 100, 'Kek Atıştırmalık', 1, 'assets/icon/kek.svg'),
(2, 'Kuruyemiş', 4.00, 100, 'Kuruyemiş Atıştırmalık', 1, 'assets/icon/kuruyemis.svg'),
(3, 'Çikolata', 3.00, 100, 'Çikolata Tatlı', 1, 'assets/icon/cikolata.svg'),
(3, 'Şekerleme', 2.00, 100, 'Şekerleme Tatlı', 1, 'assets/icon/sekerleme.svg'),
(3, 'Pasta', 5.00, 100, 'Pasta Tatlı', 1, 'assets/icon/pasta.svg'),
(3, 'Kek', 3.00, 100, 'Kek Tatlı', 1, 'assets/icon/kek.svg'),
(4, 'Fındık', 4.00, 100, 'Fındık Kuruyemiş', 1, 'assets/icon/findik.svg'),
(4, 'Badem', 4.00, 100, 'Badem Kuruyemiş', 1, 'assets/icon/badem.svg'),
(4, 'Ceviz', 4.00, 100, 'Ceviz Kuruyemiş', 1, 'assets/icon/ceviz.svg'),
(4, 'Kaju', 4.00, 100, 'Kaju Kuruyemiş', 1, 'assets/icon/kaju.svg'),
(4, 'Kuru Üzüm', 4.00, 100, 'Kurutulmuş Üzüm Kuruyemiş', 1, 'assets/icon/uzum.svg');


INSERT INTO otomatlar (otomat_ad, otomat_konum, otomat_kapasite, otomat_durum) VALUES
('Otomat 1', 'İstanbul', 100, 1),
('Otomat 2', 'Ankara', 100, 1),
('Otomat 3', 'İzmir', 100, 1),
('Otomat 4', 'Bursa', 100, 1),
('Otomat 5', 'Eskişehir', 100, 1)
('Otomat 6', 'Kütahya', 100, 1);

INSERT INTO otomat_envanter (otomat_id, urun_id, envanter_adet, envanter_sira) VALUES
(1, 1, 10, 'A1'),
(1, 2, 10, 'A2'),
(1, 3, 10, 'A3'),
(1, 4, 10, 'A4'),
(1, 5, 10, 'B1'),
(1, 6, 10, 'B2'),
(1, 7, 10, 'B3'),
(1, 8, 10, 'B4'),
(1, 9, 10, 'C1'),
(1, 10, 10, 'C2'),
(1, 11, 10, 'C3'),
(1, 12, 10, 'C4'),
(1, 13, 10, 'D1'),
(1, 14, 10, 'D2'),
(1, 15, 10, 'D3'),
(1, 16, 10, 'D4'),
(2, 1, 10, 'A1'),
(2, 2, 10, 'A2'),
(2, 3, 10, 'A3'),
(2, 4, 10, 'A4'),
(2, 5, 10, 'B1'),
(2, 6, 10, 'B2'),
(2, 7, 10, 'B3'),
(2, 8, 10, 'B4'),
(2, 9, 10, 'C1'),
(2, 10, 10, 'C2'),
(2, 11, 10, 'C3'),
(2, 12, 10, 'C4'),
(2, 13, 10, 'D1'),
(2, 14, 10, 'D2'),
(2, 15, 10, 'D3'),
(2, 16, 10, 'D4'),
(3, 1, 10, 'A1'),
(3, 2, 10, 'A2'),
(3, 3, 10, 'A3'),
(3, 4, 10, 'A4'),
(3, 5, 10, 'B1'),
(3, 6, 10, 'B2'),
(3, 7, 10, 'B3'),
(3, 8, 10, 'B4'),
(3, 9, 10, 'C1'),
(3, 10, 10, 'C2'),
(3, 11, 10, 'C3'),
(3, 12, 10, 'C4'),
(3, 13, 10, 'D1'),
(3, 14, 10, 'D2'),
(3, 15, 10, 'D3'),
(3, 16, 10, 'D4'),
(4, 1, 10, 'A1'),
(4, 2, 10, 'A2'),
(4, 3, 10, 'A3'),
(4, 4, 10, 'A4'),
(4, 5, 10, 'B1'),
(4, 6, 10, 'B2'),
(4, 7, 10, 'B3'),
(4, 8, 10, 'B4'),
(4, 9, 10, 'C1'),
(4, 10, 10, 'C2'),
(4, 11, 10, 'C3'),
(4, 12, 10, 'C4'),
(4, 13, 10, 'D1'),
(4, 14, 10, 'D2'),
(4, 15, 10, 'D3'),
(4, 16, 10, 'D4'),
(5, 1, 10, 'A1'),
(5, 2, 10, 'A2'),
(5, 3, 10, 'A3'),
(5, 4, 10, 'A4'),
(5, 5, 10, 'B1'),
(5, 6, 10, 'B2'),
(5, 7, 10, 'B3'),
(5, 8, 10, 'B4'),
(5, 9, 10, 'C1'),
(5, 10, 10, 'C2'),
(5, 11, 10, 'C3'),
(5, 12, 10, 'C4'),
(5, 13, 10, 'D1'),
(5, 14, 10, 'D2'),
(5, 15, 10, 'D3'),
(5, 16, 10, 'D4'),
(6, 1, 10, 'A1'),
(6, 2, 10, 'A2'),
(6, 3, 10, 'A3'),
(6, 4, 10, 'A4'),
(6, 5, 10, 'B1'),
(6, 6, 10, 'B2'),
(6, 7, 10, 'B3'),
(6, 8, 10, 'B4'),
(6, 9, 10, 'C1'),
(6, 10, 10, 'C2'),
(6, 11, 10, 'C3'),
(6, 12, 10, 'C4'),
(6, 13, 10, 'D1'),
(6, 14, 10, 'D2'),
(6, 15, 10, 'D3'),
(6, 16, 10, 'D4');
