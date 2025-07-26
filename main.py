from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__, template_folder='./', static_folder='assets', static_url_path='/assets')
app.secret_key = 'bansos_score_secret_key'  # Digunakan untuk session

# NIK dummy untuk pengujian
VERIFIED_NIK = "1234567890123456"  # NIK untuk hasil terverifikasi
PROCESSING_NIK = "3456789012345678"  # NIK untuk hasil dalam proses

@app.route('/')
def index():
    """Route untuk halaman utama/landing page"""
    return render_template('landing_page.html')

@app.route('/cek-status')
def check_status():
    """Route untuk halaman pengecekan status pendaftaran"""
    return render_template('cek_pendaftaran.html')

@app.route('/submit-check', methods=['POST'])
def submit_check():
    """Route untuk memproses pengecekan NIK"""
    nik = request.form.get('nik', '')
    
    if nik == VERIFIED_NIK:
        # Jika NIK sesuai dengan NIK terverifikasi
        return redirect(url_for('verified_result'))
    elif nik == PROCESSING_NIK:
        # Jika NIK sesuai dengan NIK dalam proses
        return redirect(url_for('in_process_result'))
    else:
        # Jika NIK tidak ditemukan, kembali ke halaman cek status dengan pesan error
        # Dalam implementasi sebenarnya, ini bisa menampilkan pesan error
        return redirect(url_for('check_status'))

@app.route('/hasil-verifikasi')
def verified_result():
    """Route untuk halaman hasil verifikasi selesai"""
    return render_template('success_verification.html')

@app.route('/dalam-proses')
def in_process_result():
    """Route untuk halaman hasil verifikasi dalam proses"""
    return render_template('onprocess_verification.html')

@app.route('/pendaftaran')
def registration():
    """Route untuk halaman pendaftaran peserta"""
    return render_template('pendaftaran.html')

@app.route('/submit-registration', methods=['POST'])
def submit_registration():
    """Route untuk memproses pendaftaran"""
    # Logika untuk memproses form pendaftaran
    # Dalam contoh ini, kita langsung arahkan ke halaman hasil dalam proses
    return redirect(url_for('in_process_result'))

@app.route('/lembaga')
def agency_data():
    """Route untuk halaman pengambilan data lembaga"""
    # Biasanya akan ada autentikasi di sini
    return render_template('download_data.html')

@app.route('/login-lembaga', methods=['GET', 'POST'])
def agency_login():
    """Route untuk login lembaga"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Verifikasi dummy
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('agency_data'))
        else:
            # Tampilkan pesan error
            return render_template('login.html', error='Username atau password salah')
    
    return render_template('lembaga_login.html')

@app.route('/logout')
def logout():
    """Route untuk logout"""
    session.pop('logged_in', None)
    return redirect(url_for('index'))

@app.context_processor
def inject_nik_samples():
    """Menyediakan NIK sampel ke semua template"""
    return {
        'verified_nik': VERIFIED_NIK,
        'processing_nik': PROCESSING_NIK
    }

if __name__ == '__main__':
    app.run(debug=True)