import random
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from .models import RiwayatDeteksi

# ==========================================
# 1. LOGIKA LOGIN
# ==========================================
def halaman_login(request):
    # Jika sudah login, langsung lempar ke halaman deteksi
    if request.user.is_authenticated:
        return redirect('deteksi')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('deteksi')
    else:
        form = AuthenticationForm()
        
    return render(request, 'login.html', {'form': form})

# ==========================================
# 2. LOGIKA LOGOUT
# ==========================================
def halaman_logout(request):
    logout(request)
    return redirect('login')

# ==========================================
# 3. LOGIKA REGISTER (BUAT AKUN BARU)
# ==========================================
def halaman_register(request):
    # Jika sudah login, tidak perlu buat akun lagi
    if request.user.is_authenticated:
        return redirect('deteksi')
        
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Otomatis langsung login setelah sukses daftar!
            return redirect('deteksi')
    else:
        form = UserCreationForm()
        
    return render(request, 'register.html', {'form': form})

# ==========================================
# 4. HALAMAN UTAMA (DIGEMBOK!)
# ==========================================
@login_required(login_url='login') 
def halaman_deteksi(request):
    hasil = None
    
    if request.method == 'POST':
        # RADAR 1: Lacak siapa yang kirim form
        print(f"\n[RADAR] ---> Form dikirim oleh akun: {request.user.username}")
        
        nama = request.POST.get('nama_pasien')
        gejala = {
            'smoking': int(request.POST.get('smoking')),
            'mental_stress': int(request.POST.get('mental_stress')),
            'exposure_to_pollution': int(request.POST.get('exposure_to_pollution')),
            'energy_level': int(request.POST.get('energy_level')),
            'immune_weakness': int(request.POST.get('immune_weakness')),
            'breathing_issue': int(request.POST.get('breathing_issue')),
            'throat_discomfort': int(request.POST.get('throat_discomfort')),
            'family_history': int(request.POST.get('family_history')),
            'smoking_family_history': int(request.POST.get('smoking_family_history')),
            'stress_immune': int(request.POST.get('stress_immune')),
        }
        
        # Prediksi Dummy (Nanti diganti dengan model AI)
        hasil_dummy = random.choice([0, 1])
        
        # Simpan ke Database
        pasien_baru = RiwayatDeteksi(
            user=request.user, 
            nama_pasien=nama, 
            hasil_prediksi=hasil_dummy, 
            **gejala
        )
        pasien_baru.save()
        
        # RADAR 2: Lacak apakah sukses tersimpan
        print(f"[RADAR] ---> Data BERHASIL disimpan. Pemilik: {pasien_baru.user.username}\n")
        
        hasil = "RISIKO TINGGI (Segera periksa ke dokter!)" if hasil_dummy == 1 else "RISIKO RENDAH (Tetap jaga kesehatan!)"

    return render(request, 'deteksi.html', {'hasil_prediksi': hasil})

# ==========================================
# 5. HALAMAN PROFIL & KURVA HISTORI
# ==========================================
@login_required(login_url='login')
def halaman_profil(request):
    # RADAR 3: Lacak siapa yang buka profil
    print(f"\n[RADAR] ---> Buka halaman profil. Akun yang login: {request.user.username}")
    
    riwayat = RiwayatDeteksi.objects.filter(user=request.user).order_by('tanggal_tes')
    
    # RADAR 4: Berapa data yang ketemu?
    print(f"[RADAR] ---> Jumlah data yang ditemukan: {riwayat.count()}\n")
    
    labels = [r.tanggal_tes.strftime("%d/%m") for r in riwayat]
    data_poin = [r.hasil_prediksi for r in riwayat] 
    
    return render(request, 'profil.html', {
        'riwayat': riwayat,
        'labels': labels,
        'data_poin': data_poin
    })