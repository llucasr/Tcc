readme_content = """
# Detector de Pessoas em Zona de Perigo com YOLOv8

Este projeto utiliza o modelo YOLOv8 para detetar pessoas em tempo real através de uma câmara e alerta caso uma pessoa entre numa "zona de perigo" predefinida em torno de um ponto central.

## Funcionalidades

- Detecção de Pessoas em Tempo Real: Utiliza o modelo YOLOv8 para identificar pessoas no feed da câmara.
- Definição de Zona de Perigo: Permite configurar um raio (em milímetros) que define uma zona de perigo circular.
- Cálculo de Distância Dinâmico: Ajusta o tamanho aparente da zona de perigo com base na distância da câmara ao objeto de referência e na conversão de milímetros para pixels.
- Seleção de Câmara: Lista as câmaras disponíveis no sistema e permite ao utilizador escolher qual utilizar.
- Alerta Visual: Desenha as caixas delimitadoras das pessoas detetadas, um círculo representando a zona de perigo, um círculo representando uma zona crítica e exibe um alerta no ecrã se uma pessoa entrar na zona de perigo.

## Pré-requisitos

Certifique-se de que tem o Python instalado no seu sistema. As seguintes bibliotecas são necessárias:

- ultralytics: Para o modelo YOLOv8
- opencv-python: Para processamento de imagem e captura de vídeo
- numpy: Para cálculos numéricos, especialmente na classe `ZonaDePerigo`

## Instalação

1. Clone o repositório (se aplicável) ou crie os ficheiros:
   - Guarde o primeiro bloco de código como `main.py` (ou o nome que preferir para o script principal).
   - Guarde o segundo bloco de código como `zona_de_perigo.py`.

2. Instale as dependências:
   pip install ultralytics opencv-python numpy

3. Descarregue o modelo YOLOv8 (se ainda não o fez):
   O script principal utiliza `yolov8s.pt`. O YOLO normalmente descarrega o modelo automaticamente na primeira execução se não o encontrar localmente. Pode escolher outros modelos YOLOv8 (n, m, l, x) alterando a linha:
   model = YOLO('yolov8s.pt')  # Altere para 'yolov8n.pt', 'yolov8m.pt', etc., se desejar

## Utilização

1. Execute o script principal:
   python main.py

2. Seleção da Câmara:
   - O script listará as câmaras disponíveis detetadas no seu sistema.
   - Introduza o número correspondente à câmara que deseja utilizar e pressione Enter.

3. Visualização:
   - Uma janela será aberta mostrando o feed da câmara.
   - As pessoas detetadas serão contornadas por uma caixa verde.
   - A zona de perigo será desenhada como um círculo verde.
   - Uma zona crítica (menor) será desenhada como um círculo vermelho.
   - Se uma pessoa entrar na zona de perigo (círculo verde maior), uma mensagem de alerta "Alerta: Pessoa na zona de perigo!" será exibida em vermelho no canto superior esquerdo.

4. Sair:
   - Pressione a tecla 'q' para fechar a janela de visualização e terminar o programa.

## Estrutura dos Ficheiros

- `main.py`:
  - Contém a lógica principal para carregar o modelo YOLO, capturar o vídeo da câmara, realizar deteções, interagir com a classe `ZonaDePerigo` e exibir os resultados.
  - Responsável pela seleção da câmara e pelo loop principal de processamento de frames.

- `zona_de_perigo.py`:
  - Define a classe `ZonaDePerigo`.
  - Responsável por calcular o raio da zona de perigo em pixels com base em medições físicas (mm), resolução da câmara e distância da câmara.
  - Calcula a distância de um ponto (centro de uma pessoa detetada) ao centro da zona de perigo.

## Configuração

Pode ajustar os seguintes parâmetros no início do ficheiro `main.py` e na classe `ZonaDePerigo`:

Em `main.py`:

- `model = YOLO('yolov8s.pt')`: Mude para outros tamanhos de modelo YOLOv8 (`yolov8n.pt`, `yolov8m.pt`, `yolov8l.pt`, `yolov8x.pt`) para diferentes equilíbrios entre velocidade e precisão.
- `raio_mm = (1600*0.364) + 200`: Fórmula para definir o raio físico da zona de perigo em milímetros. Ajuste conforme necessário.
- `mm_px = 25.4/142`: Relação de conversão de milímetros para pixels, baseada na densidade de pixels por polegada (PPI) do ecrã de referência. Ajuste se tiver um valor mais preciso para o seu sistema de calibração.
- `resolucao_x=640, resolucao_y=480`: Resolução esperada da câmara. A classe `ZonaDePerigo` usa estes valores para definir o centro. O OpenCV tentará configurar a câmara para esta resolução, mas pode variar.
- `distancia_camera_mm=2820`: Distância física da lente da câmara até ao plano onde a zona de perigo está a ser projetada (por exemplo, o chão ou uma máquina).
- `results = model(frame, conf=0.5)`: Altere o valor de `conf` (0.0 a 1.0) para ajustar a sensibilidade da deteção (valores mais altos são mais rigorosos).
- `zona_critica = zona_de_perigo.converter_raio_para_pixels(727)`: Define o raio (em mm) para um segundo círculo (zona crítica) desenhado a vermelho.

Em `zona_de_perigo.py` (dentro da classe `ZonaDePerigo`):

- `distancia_referencia_mm = 1050.0`: Usado no `calcular_fator_escala`. Este é um valor de referência para o cálculo do fator de escala. A lógica pressupõe que o tamanho aparente de um objeto (e, portanto, o raio projetado) é inversamente proporcional à distância.

## Como Funciona

1. Inicialização:
   - O modelo YOLOv8 é carregado.
   - Um objeto `ZonaDePerigo` é instanciado. Este objeto calcula:
     - O centro da zona de perigo (assumido como o centro do frame da câmara).
     - Um `fator_escala` baseado na `distancia_camera_mm` e numa `distancia_referencia_mm`. Este fator tenta ajustar o tamanho do raio em pixels para compensar a distância da câmara ao plano de interesse.
     - O `radius` da zona de perigo em pixels, usando o `raio_mm` fornecido, a conversão `mm_por_px` e o `fator_escala`.

2. Seleção da Câmara:
   - O programa procura por câmaras conectadas e permite que o utilizador selecione uma.

3. Loop de Processamento por Frame:
   - Um frame é capturado da câmara selecionada.
   - O frame é passado para o modelo YOLOv8, que retorna as deteções.
   - A zona de perigo e a zona crítica são desenhadas no frame como círculos.
   - Para cada deteção:
     - Se a classe detetada for 'pessoa' (ID de classe 0) e a confiança da deteção for superior ao limiar (`conf=0.5`):
       - Uma caixa delimitadora é desenhada ao redor da pessoa.
       - O centro da caixa delimitadora da pessoa é calculado.
       - A distância entre o centro da pessoa e o centro da zona de perigo é calculada (em milímetros) pelo método `calcular_distancia` da classe `ZonaDePerigo`. Este método converte a distância em pixels de volta para milímetros usando o `mm_por_px` e o `fator_escala`.
       - Se esta distância calculada (em mm) for menor que o `raio_mm` original da zona de perigo, um alerta é exibido no frame.

4. Exibição:
   - O frame processado, com as deteções e alertas, é exibido.

5. Término:
   - O loop continua até que a tecla 'q' seja pressionada.
   - Os recursos da câmara são libertados e as janelas são fechadas.

## Limitações e Considerações

- Calibração: A precisão da conversão mm/pixel e do fator de escala é crucial para que a zona de perigo corresponda a uma área física real. A atual `mm_px = 25.4/142` é uma estimativa baseada num PPI. Para maior precisão, seria necessária uma calibração da câmara mais rigorosa.
- Perspectiva: O sistema assume uma projeção 2D. A "distância" calculada para a pessoa é no plano da imagem. A profundidade real da pessoa em relação à câmara não é diretamente medida de forma precisa sem técnicas de visão estéreo ou sensores de profundidade. O `fator_escala` tenta compensar a distância da câmara ao plano da máquina/zona de perigo, não a distância individual de cada pessoa.
- Oclusões: Se uma pessoa estiver parcialmente ocluída, a deteção YOLO pode falhar ou a caixa delimitadora pode não ser precisa.
- Performance: Modelos YOLO maiores (l, x) são mais precisos, mas mais lentos. Modelos menores (n, s) são mais rápidos, mas menos precisos. A performance também depende do hardware (CPU/GPU).
"""
