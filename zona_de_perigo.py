import numpy as np

class ZonaDePerigo:
    def __init__(self, raio_mm, mm_por_px, resolucao_x, resolucao_y, distancia_camera_mm):
        """
        Inicializa a zona de perigo, convertendo o raio físico em mm para pixels
        e define a posição central do círculo.
        
        :param raio_mm: Raio da área de perigo em milímetros.
        :param mm_por_px: Relação de conversão base (para uma distância de referência).
        :param resolucao_x: Resolução horizontal da câmera em pixels.
        :param resolucao_y: Resolução vertical da câmera em pixels.
        :param distancia_camera_mm: Distância da câmera para a máquina em milímetros.
        """
        self.raio_mm = raio_mm
        self.mm_por_px = mm_por_px
        self.resolucao_x = resolucao_x
        self.resolucao_y = resolucao_y
        self.distancia_camera_mm = distancia_camera_mm

        # Definindo a posição do centro do círculo como o centro da imagem
        self.center_x = resolucao_x // 2
        self.center_y = resolucao_y // 2

        # Calculando o fator de escala com base na distância
        self.fator_escala = self.calcular_fator_escala()

        # Convertendo o raio de mm para pixels ajustado pela distância da câmera
        self.radius = int(self.raio_mm * self.mm_por_px * self.fator_escala)

    def calcular_fator_escala(self):
        """
        Calcula o fator de escala com base na distância da câmera para a máquina.
        Quanto mais distante a câmera, menor será o tamanho do raio projetado.
        
        Supondo que o raio é proporcionalmente menor com o aumento da distância da câmera.
        Por exemplo, dobrar a distância da câmera reduz o raio pela metade.
        """
        # Distância de referência para cálculo do fator (exemplo: 1000 mm)
        distancia_referencia_mm = 1000.0
        
        # O fator de escala é a proporção entre a distância de referência e a distância atual
        fator_escala = distancia_referencia_mm / self.distancia_camera_mm
        return fator_escala

    def calcular_distancia(self, ponto1):
        """
        Calcula a distância entre o centro do círculo e um ponto dado (como a posição de uma pessoa).
        :param ponto1: Posição da pessoa (x, y).
        :return: Distância entre o ponto1 e o centro do círculo.
        """
        return np.sqrt((ponto1[0] - self.center_x) ** 2 + (ponto1[1] - self.center_y) ** 2)
