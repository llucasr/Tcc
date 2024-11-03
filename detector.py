from ultralytics import YOLO
import cv2
from zona_de_perigo import ZonaDePerigo

# Carregando o modelo YOLOv8 pré-treinado n, s, m, l,x 
model = YOLO('yolov8s.pt')

# Inicializa a zona de perigo
raio_mm = (1600*0.364) + 200
print (raio_mm)
zona_de_perigo = ZonaDePerigo(int(raio_mm), mm_por_px=0.1789, resolucao_x=640, resolucao_y=480, distancia_camera_mm=2820)

# Função para listar as câmeras disponíveis
def listar_cameras_disponiveis(max_cameras=10):
    cameras_disponiveis = []
    for index in range(max_cameras):
        cap = cv2.VideoCapture(index)
        if cap.isOpened():
            cameras_disponiveis.append(index)
            cap.release()
    return cameras_disponiveis

# Listar as câmeras disponíveis
cameras = listar_cameras_disponiveis()

if not cameras:
    print("Nenhuma câmera encontrada.")
    exit()

print("Câmeras disponíveis:")
for i, cam in enumerate(cameras):
    print(f"[{i}] Câmera {cam}")

# Escolher a câmera
escolha = int(input("Escolha a câmera pelo número correspondente: "))

if escolha not in range(len(cameras)):
    print("Escolha inválida.")
    exit()

camera_escolhida = cameras[escolha]
print(f"Você escolheu a câmera {camera_escolhida}")

# Captura de vídeo da webcam
cap = cv2.VideoCapture(camera_escolhida)

# Verifique se a câmera foi aberta corretamente
if not cap.isOpened():
    print("Erro ao abrir a câmera.")
    exit()

while True:
    # Captura frame a frame
    ret, frame = cap.read()
    
    if not ret:
        print("Falha ao capturar a imagem da webcam.")
        break

    # Fazendo a detecção no frame capturado
    results = model(frame)

    # Extraindo as caixas delimitadoras das detecções
    boxes = results[0].boxes

    # Desenha o círculo delimitador na imagem
    zona_critica = zona_de_perigo.converter_raio_para_pixels(727)
    cv2.circle(frame, (zona_de_perigo.center_x, zona_de_perigo.center_y), zona_de_perigo.radius, (0, 255, 0), 2)
    cv2.circle(frame, (zona_de_perigo.center_x, zona_de_perigo.center_y), zona_critica, (0, 0, 255), 1)

    # Loop para desenhar as caixas delimitadoras das detecções de pessoas
    for box in boxes:
        class_id = int(box.cls[0])  # Pegando a classe da detecção
        if class_id == 0:  # Classe 0 corresponde a 'pessoa'
            # Desenhar a caixa delimitadora na imagem
            x1, y1, x2, y2 = map(int, box.xyxy[0])
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(frame, 'Pessoa', (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            # Calcula o centro da caixa delimitadora (posição da pessoa)
            center_person_x = (x1 + x2) // 2
            center_person_y = (y1 + y2) // 2
            person_position = (center_person_x, center_person_y)

            # Calcula a distância da pessoa até o centro do círculo
            distancia_da_pessoa = zona_de_perigo.calcular_distancia(person_position)

            # Verifica se a pessoa está dentro do círculo (zona de perigo)
            if distancia_da_pessoa < zona_de_perigo.radius:
                cv2.putText(frame, 'Alerta: Pessoa na zona de perigo!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    # Exibir o frame com as detecções
    cv2.imshow('Detecção de Pessoas - YOLOv8', frame)

    # Pressionar 'q' para sair
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar a captura de vídeo e fechar todas as janelas
cap.release()
cv2.waitKey(1)
cv2.destroyAllWindows()

