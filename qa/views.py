from rest_framework.decorators import api_view
from rest_framework.response import Response

from qa.ai.semantic import SemanticSearchAI
from qa.ai.detect_kbli import KBLIDetector
from qa.ai.formatter import format_jawaban

from django.shortcuts import render

def chat_ui(request):
    return render(request, "chat.html")

# Inisialisasi engine (sekali saja)
ai_engine = SemanticSearchAI()
kbli_detector = KBLIDetector()




@api_view(["POST"])
def tanya_ai(request):
    pertanyaan = request.data.get("pertanyaan")
    kbli = request.data.get("kbli")

    # 1️⃣ Validasi pertanyaan
    if not pertanyaan:
        return Response(
            {"error": "Pertanyaan tidak boleh kosong"},
            status=400
        )

    auto_detect = False

    # 2️⃣ Auto-detect KBLI jika tidak dikirim
    if not kbli:
        kbli = kbli_detector.detect(pertanyaan)
        auto_detect = True

    # 3️⃣ Jika tetap tidak ketemu KBLI
    if not kbli:
        return Response(
            {
                "error": "KBLI tidak dapat dideteksi dari pertanyaan",
                "saran": "Mohon sertakan KBLI atau jelaskan jenis usahanya"
            },
            status=400
        )

    # 4️⃣ Jalankan AI semantic search
    results = ai_engine.search(
        query=pertanyaan,
        kbli=kbli
    )

    # 5️⃣ Format jawaban (diambil dari field `teks`)
    output = format_jawaban(results, pertanyaan)

    # 6️⃣ Tambahkan metadata
    output["kbli"] = kbli
    output["auto_detect"] = auto_detect

    return Response(output)
