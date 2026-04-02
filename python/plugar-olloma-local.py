import subprocess
import time

def conectar_ollama():
    try:
        # Tenta iniciar o servidor Ollama em background
        process = subprocess.Popen(['ollama', 'serve'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
        print("Servidor Ollama iniciado com sucesso.")
        print("API disponível em: http://localhost:11434")
        print("Configure o VS Code ou Cursor para usar este endpoint para modelos de IA locais.")
        print("Por exemplo, no Cursor: Vá para Configurações > AI > API Base URL e defina para http://localhost:11434/v1")
        # Mantém o processo rodando em background
        return process
    except FileNotFoundError:
        print("Erro: Ollama não está instalado ou não está no PATH. Instale o Ollama primeiro.")
    except Exception as e:
        print(f"Erro ao iniciar Ollama: {e}")

if __name__ == "__main__":
    conectar_ollama()