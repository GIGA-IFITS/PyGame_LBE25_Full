# PyGame_LBE25_Full - Space Shooter Game

Sebuah game space shooter yang dibuat menggunakan PyGame untuk Learning by Example (LBE) course. Game ini menampilkan pesawat luar angkasa yang dapat menembak asteroid sambil menghindari tabrakan.

## Fitur Utama

### 🚀 Gameplay Dasar
- Kontrol pesawat dengan WASD atau Arrow Keys
- Tembak asteroid dengan Space bar
- Hindari tabrakan dengan asteroid
- Sistem scoring berdasarkan asteroid yang dihancurkan
- Background music dan sound effects
- Animasi ledakan saat asteroid hancur

### ✨ Fitur Pergantian Pesawat
Game ini mendukung **3 jenis pesawat** yang berbeda dengan karakteristik unik:

#### Jenis Pesawat:
1. **Blue Ship (Balanced)**
   - Kecepatan normal
   - Pesawat seimbang untuk pemain biasa

2. **Red Ship (Fast)**
   - Kecepatan +1 lebih cepat
   - Cocok untuk pemain yang suka bergerak cepat

3. **Shadow Ship (Stealth)**
   - Kecepatan -1 lebih lambat
   - Pesawat dengan tampilan unik

## Kontrol Game

### Di Menu:
- **← →** (panah kiri/kanan): Memilih jenis pesawat
- **Mouse**: Klik tombol Play/Quit
- **ESC**: Keluar dari game

### Saat Bermain:
- **WASD** atau **Arrow Keys**: Gerakkan pesawat
- **Space**: Tembak peluru
- **C**: Ganti pesawat secara real-time
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
- Informasi pesawat aktif ditampilkan di pojok kiri atas
- Deskripsi karakteristik pesawat (Balanced/Fast/Stealth)
- Instruksi kontrol di menu utama
- Indikator visual pesawat yang dipilih di menu
- Real-time score display

### 🔧 Sistem Game
- Pergantian pesawat dapat dilakukan kapan saja saat bermain
- Setiap pesawat memiliki kecepatan gerakan yang berbeda
- Animasi rotasi asteroid yang realistis
- Collision detection menggunakan circle collision
- Respawn otomatis asteroid setelah hancur atau keluar layar

## Tips Bermain

1. **Pesawat Blue**: Pilihan terbaik untuk pemula, kecepatan seimbang
2. **Pesawat Red**: Untuk gameplay yang lebih menantang dan cepat
3. **Pesawat Shadow**: Untuk gaya bermain yang lebih strategis
4. Gunakan tombol **C** untuk berganti pesawat sesuai situasi
5. Manfaatkan fitur pause (**P**) untuk istirahat sejenak

## Credits

Game ini dibuat untuk Learning by Example (LBE) PyGame course.

Asset grafis: PixelSpaceRage asset pack
Background Music: Included in Assets folder

---

**Selamat bermain! 🎮🚀**