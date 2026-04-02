import subprocess

def desconectar_ollama():
    try:
        # Verifica se o processo do Ollama está rodando
        check_result = subprocess.run(['tasklist', '/fi', 'imagename eq ollama.exe'], capture_output=True, text=True)
        if 'ollama.exe' in check_result.stdout:
            # Mata o processo do Ollama
            result = subprocess.run(['taskkill', '/im', 'ollama.exe', '/f'], capture_output=True, text=True)
            if result.returncode == 0:
                print("Servidor Ollama parado com sucesso.")
            else:
                print("Erro ao parar o servidor Ollama.")
                print("Saída:", result.stdout, result.stderr)
        else:
            print("O servidor Ollama não está rodando.")
    except Exception as e:
        print(f"Erro ao parar Ollama: {e}")

if __name__ == "__main__":
    desconectar_ollama()