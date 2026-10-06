from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
import random

app = FastAPI(title="API Generator Angka v4")

class AngkaRequest(BaseModel):
    angka: str = Field(..., min_length=2, max_length=5, description="Masukkan 2-5 digit angka")

def generate_angka_rahasia(input_str: str) -> str:
    if not input_str.isdigit():
        raise ValueError("Input harus berupa angka murni.")

    if len(input_str) > 1:
        shifted_str = input_str[-1] + input_str[:-1]
    else:
        shifted_str = input_str

    hasil_akhir = []
    for digit in shifted_str:
        num = int(digit)
        is_tambah = random.choice([True, False])
        operator_value = random.randint(0, 5)
        
        if is_tambah:
            angka_baru = (num + operator_value) % 10
        else:
            angka_baru = (num - operator_value) % 10
            
        hasil_akhir.append(str(angka_baru))

    return "".join(hasil_akhir)

# --- INI BAGIAN UI (FRONTEND Sederhana) ---
@app.get("/", response_class=HTMLResponse)
def read_root():
    return """
    <!DOCTYPE html>
    <html lang="id">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
        <title>Generator Angka</title>
        <style>
            * { box-sizing: border-box; }
            body { 
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
                background-color: #f3f4f6; 
                display: flex; justify-content: center; align-items: center; 
                min-height: 100vh; margin: 0; padding: 20px;
            }
            .card { 
                background: white; padding: 30px 20px; border-radius: 16px; 
                box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); 
                width: 100%; max-width: 380px; text-align: center; 
            }
            h2 { margin-top: 0; color: #111827; font-size: 24px; margin-bottom: 20px;}
            input { 
                width: 100%; padding: 15px; margin-bottom: 15px; 
                border: 2px solid #e5e7eb; border-radius: 10px; 
                font-size: 18px; text-align: center; outline: none; transition: border 0.3s;
            }
            input:focus { border-color: #3b82f6; }
            button { 
                background-color: #3b82f6; color: white; border: none; 
                padding: 15px; font-size: 18px; border-radius: 10px; 
                cursor: pointer; width: 100%; font-weight: bold; 
                transition: background 0.3s;
            }
            button:active { background-color: #2563eb; }
            .result-box {
                margin-top: 25px; padding: 20px;
                background-color: #f0fdf4; border: 1px dashed #22c55e;
                border-radius: 10px; display: none;
            }
            .result-text { font-size: 32px; font-weight: 800; color: #16a34a; letter-spacing: 4px; }
            .error { color: #ef4444; font-size: 14px; margin-top: 10px; font-weight: 500;}
        </style>
    </head>
    <body>
        <div class="card">
            <h2>Generator Angka</h2>
            <input type="number" id="inputAngka" placeholder="Masukkan 2-5 digit" inputmode="numeric" />
            <button onclick="prosesGenerate()" id="btnGen">Generate Sekarang</button>
            
            <div id="resultBox" class="result-box">
                <div style="font-size: 12px; color: #15803d; margin-bottom: 5px;">HASIL:</div>
                <div id="resultText" class="result-text"></div>
            </div>
            <div id="errorMsg" class="error"></div>
        </div>

        <script>
            async function prosesGenerate() {
                const angka = document.getElementById('inputAngka').value;
                const resultBox = document.getElementById('resultBox');
                const resultText = document.getElementById('resultText');
                const errorDiv = document.getElementById('errorMsg');
                const btn = document.getElementById('btnGen');
                
                // Reset State
                errorDiv.innerText = '';
                resultBox.style.display = 'none';
                btn.innerText = 'Memproses...';
                
                try {
                    const response = await fetch('/generate', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ angka: String(angka) })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        resultText.innerText = data.hasil_generate;
                        resultBox.style.display = 'block';
                    } else {
                        // Ambil pesan error dari FastAPI (biasanya di data.detail)
                        let errorDetail = data.detail;
                        if (Array.isArray(errorDetail)) {
                            errorDiv.innerText = errorDetail[0].msg;
                        } else {
                            errorDiv.innerText = errorDetail;
                        }
                    }
                } catch (err) {
                    errorDiv.innerText = 'Koneksi gagal. Cek internet lo.';
                } finally {
                    btn.innerText = 'Generate Sekarang';
                }
            }
        </script>
    </body>
    </html>
    """

@app.post("/generate")
def generate_angka(req: AngkaRequest):
    try:
        hasil = generate_angka_rahasia(req.angka)
        return {
            "status": "success",
            "input_asli": req.angka,
            "hasil_generate": hasil
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))