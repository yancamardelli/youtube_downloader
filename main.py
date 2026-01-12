from __future__ import annotations

from pathlib import Path
from yt_dlp import YoutubeDL


def ensure_downloads_folder() -> Path:
    """Cria a pasta downloads/ se não existir e retorna o caminho."""
    downloads_dir = Path(__file__).parent / "downloads"
    downloads_dir.mkdir(exist_ok=True)
    return downloads_dir


def download_video(url: str, output_dir: Path) -> None:
    """Baixa vídeo (mp4) na melhor qualidade disponível."""
    ydl_opts = {
        "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
        "format": "bv*+ba/best",  # melhor vídeo + melhor áudio, ou "best"
        "noplaylist": False,
        "quiet": False,
        "no_warnings": True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def download_audio_mp3(url: str, output_dir: Path) -> None:
    """
    Baixa áudio e converte para MP3.
    Requer FFmpeg instalado no sistema.
    """
    ydl_opts = {
        "outtmpl": str(output_dir / "%(title)s.%(ext)s"),
        "format": "bestaudio/best",
        "noplaylist": False,
        "quiet": False,
        "no_warnings": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
    }
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def ask_choice() -> str:
    print("\nO que você quer baixar?")
    print("1 - Vídeo (MP4)")
    print("2 - Áudio (MP3)")
    choice = input("Digite 1 ou 2 e pressione Enter: ").strip()
    return "audio" if choice == "2" else "video"


def main() -> None:
    print("=== YouTube Downloader (Python) ===\n")

    url = input("Cole a URL do vídeo (ou playlist) e pressione Enter: ").strip()
    if not url:
        print("Você não colocou nenhuma URL. Encerrando.")
        return

    output_dir = ensure_downloads_folder()
    mode = ask_choice()

    print("\nPreparando o download…")
    print(f"Pasta de saída: {output_dir}")

    try:
        if mode == "audio":
            print("Modo: Áudio (MP3)")
            print("Obs.: para MP3, você precisa ter o FFmpeg instalado.")
            download_audio_mp3(url, output_dir)
        else:
            print("Modo: Vídeo (MP4)")
            download_video(url, output_dir)

        print("\n✅ Download concluído com sucesso!")
        print(f"Arquivos salvos em: {output_dir}")

    except Exception as e:
        print("\n❌ Deu erro durante o download.")
        print("Mensagem do erro:")
        print(e)
        print("\nDicas rápidas:")
        print("- Confira se a URL está correta.")
        print("- Tente outro vídeo para testar.")
        print("- Se for MP3, instale o FFmpeg e tente novamente.")


if __name__ == "__main__":
    main()
