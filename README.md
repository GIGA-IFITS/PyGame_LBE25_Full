# PyGame_LBE25_Full - Space Shooter Game

Sebuah game space shooter yang dibuat menggunakan PyGame untuk Learning by Example (LBE) course. Game ini menampilkan pesawat luar angkasa yang dapat menembak asteroid sambil menghindari tabrakan.

## Fitur Utama

### 🚀 Gameplay Dasar
- Kontrol pesawat dengan WASD atau Arrow Keys
- Tembak asteroid dengan Space bar
- Hindari tabrakan dengan asteroid
- Sistem scoring berdasarkan asteroid yang dihancurkan
- Background music otomatis
- Animasi ledakan saat asteroid hancur

### ✨ Fitur Pergantian Pesawat
Game ini mendukung **2 jenis pesawat** yang dapat dipilih di menu utama:

#### Jenis Pesawat:
1. **Blue Ship (Balanced)**
   - Kecepatan normal
   - Pesawat seimbang untuk pemain biasa

2. **Red Ship (Fast)**
   - Kecepatan +1 lebih cepat
   - Cocok untuk pemain yang suka bergerak cepat

### ⚙️ Menu Options
Menu pengaturan dengan fitur:
- **Brightness Control**: Mengatur kecerahan layar game (0-100%)
- Pengaturan tersimpan selama sesi bermain

## Kontrol Game

### Di Menu:
- **← →** (panah kiri/kanan): Memilih jenis pesawat
- **Mouse**: Klik tombol Play/Options/Quit
- **ESC**: Keluar dari game

### Di Menu Options:
- **Mouse**: Drag slider untuk mengatur brightness
- **ESC**: Kembali ke menu utama

### Saat Bermain:
- **WASD** atau **Arrow Keys**: Gerakkan pesawat
- **Space**: Tembak peluru
- **P**: Pause/Resume game
- **ESC**: Keluar ke menu utama

### Saat Game Over:
- **R**: Restart game
- **X**: Kembali ke menu utama

## Instalasi dan Menjalankan

### Persyaratan:
- Python 3.7+
- PyGame library

### Langkah Instalasi:
1. Clone atau download repository ini
2. Install PyGame:
   ```bash
   pip install pygame
   ```
3. Jalankan game:
   ```bash
   python game.py
   ```

## Struktur Project

```
PyGame_LBE25_Full/
├── game.py          # Main file untuk menjalankan game
├── core.py          # Logic utama game dan class-class
├── menu.py          # Menu utama dan UI
├── README.md        # Dokumentasi project
└── Assets/          # Folder berisi semua asset game
    ├── Background Music.mp3
    └── PixelSpaceRage/
        └── 256px/   # Sprite pesawat, asteroid, dll
```

## Fitur Tambahan

### 🎮 UI dan Visual
- Score display di bagian atas layar
- Pilihan pesawat di menu utama dengan visual indikator
- Menu Options dengan slider interaktif
- Brightness control yang mempengaruhi seluruh tampilan game
- Instruksi kontrol di menu utama

### 🔧 Sistem Game
- Pemilihan pesawat hanya di menu utama (tidak bisa diganti saat bermain)
- Setiap pesawat memiliki kecepatan gerakan yang berbeda
- Animasi rotasi asteroid yang realistis
- Collision detection menggunakan circle collision
- Respawn otomatis asteroid setelah hancur atau keluar layar
- Pengaturan brightness real-time

## Tips Bermain

1. **Pesawat Blue**: Pilihan terbaik untuk pemula, kecepatan seimbang
2. **Pesawat Red**: Untuk gameplay yang lebih menantang dan cepat
3. **Brightness**: Sesuaikan dengan kenyamanan mata Anda
4. Manfaatkan fitur pause (**P**) untuk istirahat sejenak

## Credits

Game ini dibuat untuk Learning by Example (LBE) PyGame course.

Asset grafis: PixelSpaceRage asset pack
Background Music: Included in Assets folder

---

**Selamat bermain! 🎮🚀**