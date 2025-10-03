# PyGame_LBE25_Full - Advanced Space Shooter Game

Sebuah game space shooter yang dibuat menggunakan PyGame untuk Learning by Example (LBE) course. Game ini menampilkan pesawat luar angkasa yang dapat menembak asteroid sambil menghindari tabrakan, dilengkapi dengan sistem powerup, health, high score, dan berbagai fitur canggih lainnya.

## 🌟 Fitur Utama

### 🚀 Gameplay Inti
- Kontrol pesawat dengan WASD atau Arrow Keys
- Tembak asteroid dengan Space bar (dengan cooldown 0.25 detik)
- Hindari tabrakan dengan asteroid
- Sistem scoring berdasarkan asteroid yang dihancurkan
- Background music otomatis dengan sound effects
- Animasi ledakan saat asteroid hancur
- Resolusi game: **1000x700 pixel** untuk pengalaman visual yang lebih baik

### ✨ Sistem Pesawat
Game ini mendukung **2 jenis pesawat** yang dapat dipilih di menu utama:

#### Jenis Pesawat:
1. **Blue Ship (Balanced Fighter)**
   - Kecepatan standard dan seimbang
   - Pesawat ideal untuk pemain biasa
   - Ukuran: 70x70 pixel

2. **Red Ship (Fast Fighter)**
   - Kecepatan +1 lebih cepat dari Blue Ship
   - Cocok untuk pemain yang suka bergerak cepat
   - Ukuran: 70x70 pixel

**Fitur Animasi Pesawat:**
- 3 frame animasi untuk setiap pesawat (Frame_01, Frame_02, Frame_03)
- Animasi dinamis di menu selection dengan efek flip horizontal
- Arah pesawat berubah setiap 2 detik di menu

### 💖 Sistem Health & Survival
- **3 Health Points** untuk setiap pesawat
- **Visual Health Indicator**: Ikon pesawat kecil (30x30) di kanan bawah
- Health icon menggunakan asset pesawat sesuai warna yang dipilih
- Game over setelah health habis

### ⚡ Sistem Powerup Canggih
5 jenis powerup dengan efek unik:

1. **⚡ Energy Powerup (Hijau)**
   - Menghancurkan semua musuh di layar sekaligus
   - Bonus score +25 per musuh yang dihancurkan
   - Efek visual: Multiple explosions

2. **🚀 Rocket Powerup (Merah)**
   - Duration: 10 detik
   - Setiap musuh yang dihancurkan akan menembakkan 3 proyektil kecil
   - Proyektil bergerak ke arah 225°, 270°, 315° (kiri-atas, atas, kanan-atas)
   - Timer display: "Rocket: Xs"

3. **💚 Health Powerup (Pink)**
   - Menambah 1 health point
   - Maximum health: 3 points
   - Restoration instant

4. **🔫 Ammo Powerup (Biru)**
   - Duration: 15 detik  
   - Menghilangkan shooting cooldown
   - Bisa menembak dengan sangat cepat
   - Timer display: "Ammo: Xs"

5. **🛡️ Shield Powerup (Kuning)**
   - Duration: 8 detik
   - Memberikan invincibility sementara
   - Timer display: "Shield: Xs"

### 🏆 High Score System
Sistem high score lengkap dengan persistensi data:
- **Top 10 High Scores** tersimpan permanent di `highscores.json`
- **Input nama player** otomatis setelah game over (jika score masuk top 10)
- **High Scores menu** di menu utama untuk melihat hall of fame
- **Auto-sorting** berdasarkan score tertinggi
- **Real-time save** setiap kali ada score baru

### ⚙️ Menu & Options System
**Menu Utama:**
- Ship selection dengan preview animasi
- Play, High Scores, Options, Quit buttons
- UI yang clean dan responsive

**Options Menu:**
- **Brightness Control**: Slider untuk mengatur kecerahan (0-100%)
- **Complete Controls Guide**:
  - Movement: WASD atau Arrow Keys
  - Actions: SPACE (Shoot), P (Pause)  
  - Ship Selection: ← → Arrow Keys (di menu)
- Pengaturan tersimpan selama sesi bermain

**High Scores Menu:**
- Display ranking, nama player, dan score
- Format: "1. PLAYER1    2,500"
- Navigation dengan ESC atau ENTER

## 🎮 Kontrol Lengkap

### Di Menu Utama:
- **← →** (panah kiri/kanan): Memilih jenis pesawat
- **Mouse**: Klik tombol Play/High Scores/Options/Quit
- **ESC**: Keluar dari game

### Di High Scores:
- **ESC** atau **ENTER**: Kembali ke menu utama

### Di Menu Options:
- **Mouse**: Drag slider untuk mengatur brightness
- **ESC** atau **Back button**: Kembali ke menu utama

### Saat Bermain:
- **WASD** atau **Arrow Keys**: Gerakkan pesawat
- **Space**: Tembak peluru (cooldown 0.25 detik)
- **P**: Pause/Resume game
- **ESC**: Keluar ke menu utama

### Saat Game Over:
- **Input Nama** (jika high score): Type nama, ENTER save, ESC skip
- **R**: Restart game
- **X**: Kembali ke menu utama

### Saat Input High Score:
- **Type**: Masukkan nama (max 15 karakter)
- **ENTER**: Simpan score dan nama
- **ESC**: Skip input nama
- **BACKSPACE**: Hapus karakter

## 🛠️ Instalasi dan Menjalankan

### Persyaratan:
- Python 3.7+
- PyGame 2.6.1+

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

## 📁 Struktur Project

```
PyGame_LBE25_Full/
├── game.py            # Main file & state management
├── core.py            # Game logic, classes, dan gameplay systems
├── menu.py            # Menu system & UI components
├── highscore.py       # High score management system
├── highscores.json    # Persistent high scores data
├── README.md          # Dokumentasi lengkap
└── Assets/            # Folder berisi semua asset game
    ├── Background Music.mp3
    ├── Destroyed.mp3  # Sound effect
    └── PixelSpaceRage/
        ├── PixelBackgroundSeamless.png
        └── 256px/     # Sprites: ships, asteroids, powerups, dll
```

## 🎯 Fitur Advanced

### � Visual & Animation
- **Ship Animations**: 3-frame animation cycle untuk semua pesawat
- **Menu Ship Preview**: Animasi dinamis dengan directional flipping
- **Explosion Effects**: Multiple explosion types dan effects
- **Powerup Visual Feedback**: Timer displays untuk active powerups
- **Health Visualization**: Ship-colored health icons
- **Brightness System**: Real-time brightness adjustment

### 🔧 Sistem Game Advanced  
- **Asteroid Management**: Minimum 6 asteroids selalu di layar
- **Auto-spawn System**: Asteroid respawn setiap 2 detik jika kurang dari minimum
- **Collision Detection**: Circle collision untuk akurasi tinggi
- **Shooting Cooldown**: Preventing spam shooting (0.25s)
- **State Management**: MENU/OPTIONS/HIGHSCORES/PLAYING/PAUSED/GAME_OVER
- **Persistent Settings**: Brightness dan high scores tersimpan

### 📊 Scoring System
- **Asteroid destroyed**: +50 points
- **Powerup collected**: +25 points  
- **Energy powerup bonus**: +25 per enemy cleared
- **Rocket projectile hits**: +25 points
- **High score threshold**: Dynamic based on top 10

## 🏅 Tips & Strategi

### Pemilihan Pesawat:
- **Blue Ship**: Ideal untuk pemula, movement terkontrol
- **Red Ship**: Untuk advanced players, speed advantage

### Powerup Priority:
1. **Health** - Prioritas tertinggi untuk survival
2. **Shield** - Temporary invincibility untuk situasi bahaya  
3. **Energy** - Instant screen clear dan bonus score
4. **Ammo** - Untuk damage output maksimal
5. **Rocket** - Additional damage dan score

### Advanced Techniques:
- Manfaatkan **Ammo powerup** untuk maximum damage
- Gunakan **Shield** saat terlalu banyak asteroid
- **Energy powerup** optimal saat layar penuh asteroid
- **Rocket effect** memberikan additional projectiles

## 🏆 High Score Tips

- Fokus pada **survival** untuk score jangka panjang
- **Collect semua powerups** untuk bonus points
- **Energy powerup** di saat yang tepat = massive bonus
- **Ammo powerup** + banyak asteroid = score boost
- Patience > aggressive playing untuk high scores

## 📋 Changelog

### Latest Updates:
- ✅ Resolusi diperbesar ke 1000x700
- ✅ Health system dengan visual indicators  
- ✅ 5 jenis powerup dengan efek unik
- ✅ High score system dengan input nama
- ✅ Shooting cooldown system
- ✅ Enhanced ship animations
- ✅ Comprehensive controls di Options
- ✅ Asteroid auto-spawn management
- ✅ Sound effects integration

## 👨‍💻 Credits

Game ini dibuat untuk Learning by Example (LBE) PyGame course.

**Assets:**
- Graphics: PixelSpaceRage asset pack
- Background Music: Included in Assets folder  
- Sound Effects: Destroyed.mp3

**Development:**
- Framework: PyGame 2.6.1
- Language: Python 3.11.9
- Development Environment: VS Code

---

**🎮 Selamat bermain dan raih high score tertinggi! 🚀**