def format_jawaban(results, pertanyaan):
    if not results:
        return {
            "jawaban": "Maaf, tidak ditemukan ketentuan yang relevan dalam Permenpar No. 6 Tahun 2025.",
            "referensi": []
        }

    utama = results[0]["data"]

    jawaban = (
        f"Berdasarkan {utama.regulasi} "
        f"Pasal {utama.pasal}"
    )

    if utama.sub_pasal:
        jawaban += f" Ayat {utama.sub_pasal}"

    jawaban += f", disebutkan bahwa:\n\n{utama.teks}"

    referensi = []
    for r in results:
        d = r["data"]
        referensi.append({
            "pasal": d.pasal,
            "sub_pasal": d.sub_pasal,
            "kategori": d.kategori,
            "score": r["score"]
        })

    return {
        "jawaban": jawaban,
        "referensi": referensi
    }
