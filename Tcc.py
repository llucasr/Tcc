import cv2

# Inicializa a webcam (0 é o índice da webcam)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Não foi possível acessar a webcam.")
    exit()

# Loop para capturar quadro a quadro
while True:
    ret, frame = cap.read()  # Captura um quadro
    if not ret:
        print("Não foi possível capturar quadro.")
        break

    # Exibe o quadro na janela chamada 'Webcam'
    cv2.imshow('Webcam', frame)

    # Pressione 'q' para sair do loop e fechar a janela
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Libera a captura da webcam e fecha as janelas
cap.release()
cv2.destroyAllWindows()
