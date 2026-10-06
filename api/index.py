from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import random

app = FastAPI(title="API Generator Angka v4")

class AngkaRequest(BaseModel):
    angka: str = Field(..., min_length=2, max_length=5, description="Masukkan 2-5 digit angka")

def generate_angka_rahasia(input_str: str) -> str:
    if not input_str.isdigit():
        raise ValueError("Input harus berupa angka murni.")

    # Langkah 2: Geser 1 angka paling belakang jadi ke depan
    # Contoh input "12345" menjadi "51234"
    if len(input_str) > 1:
        shifted_str = input_str[-1] + input_str[:-1]
    else:
        shifted_str = input_str

    hasil_akhir = []

    # Langkah 3 - 6: Eksekusi digit by digit (dari index 0 sampai index terakhir)
    for digit in shifted_str:
        num = int(digit)
        
        # Langkah 3: Generate random untuk operasi (True = Tambah, False = Kurang)
        is_tambah = random.choice([True, False])
        
        # Langkah 4: Generate random untuk angka pengurang/penambah (0-5)
        # Sesuai request: rentang nilai operator adalah 0 sampai 5
        operator_value = random.randint(0, 5)
        
        # Langkah 5: Eksekusi menggunakan sistem Modulo 10
        if is_tambah:
            angka_baru = (num + operator_value) % 10
        else:
            angka_baru = (num - operator_value) % 10
            
        hasil_akhir.append(str(angka_baru))

    return "".join(hasil_akhir)

@app.get("/")
def read_root():
    return {"message": "API Generator Angka v4 Aktif! Buka /docs untuk testing."}

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