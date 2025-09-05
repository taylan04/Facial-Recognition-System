import cv2

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao abrir a câmera!")
    exit()

print("Pressione G para salvar a foto.")
print("Pressione Q para salvar a foto.")

contador = 0

while True:
    ret, frame = cap.read()
    if not ret:
        print("Não foi possível capturar o frame!")
        break

    cv2.imshow('Camera', frame)

    tecla = cv2.waitKey(1) & 0xFF
    if tecla == ord('g'):
        nome_arquivo = f"foto_{contador}.png"
        cv2.imwrite(nome_arquivo, frame)
        print(f"Foto salva como: {nome_arquivo}")
        contador += 1
    elif tecla == ord('q'):
        print("Saindo do programa!")
        break

cap.release()
cv2.destroyAllWindows()