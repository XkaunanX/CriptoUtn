from dataclasses import dataclass, field
from typing import List, Dict, Tuple
from collections import Counter
import math

@dataclass
class Simbolo:
    caracter: str
    frecuencia: int
    probabilidad: float = 0.0
    imutua: float = 0.0
    entropia: float = 0.0
    codigo: str = ''
    bits_totales: int = 0
    longitud_promedio: float = 0.0

    def calcular_info(self, total: int):
        self.probabilidad = self.frecuencia / total
        self.imutua = -math.log2(self.probabilidad)
        self.entropia = self.probabilidad * self.imutua


class ShannonFanoEncoder:
    def __init__(self, texto: str):
        self.texto = texto
        self.simbolos: List[Simbolo] = []
        self.total_simbolos = 0
        self.entropia_total = 0.0
        self.longitud_promedio = 0.0
        self.eficiencia = 0.0
        self.codigos: Dict[str, str] = {}
        self.texto_codificado = ""

    def analizar_texto(self):
        contador = Counter(self.texto)
        self.total_simbolos = sum(contador.values())

        self.simbolos = [
            Simbolo(car, freq) for car, freq in contador.items()
        ]

        for simbolo in self.simbolos:
            simbolo.calcular_info(self.total_simbolos)

        self.simbolos.sort(key=lambda s: s.frecuencia, reverse=True)
        self.entropia_total = sum(s.entropia for s in self.simbolos)

    def dividir_simbolos(self, simbolos: List[Simbolo]) -> Tuple[List[Simbolo], List[Simbolo]]:
        total_prob = sum(s.probabilidad for s in simbolos)
        mitad = total_prob / 2
        acumulado = 0.0
        mejor_idx = 0
        mejor_diff = float('inf')

        for i in range(len(simbolos) - 1):
            acumulado += simbolos[i].probabilidad
            diff = abs(mitad - acumulado)
            if diff < mejor_diff:
                mejor_diff = diff
                mejor_idx = i

        return simbolos[:mejor_idx + 1], simbolos[mejor_idx + 1:]

    def asignar_codigos(self, simbolos: List[Simbolo], prefijo: str = ""):
        if len(simbolos) == 1:
            simbolos[0].codigo = prefijo or "0"
            self.codigos[simbolos[0].caracter] = simbolos[0].codigo
            return

        izquierda, derecha = self.dividir_simbolos(simbolos)
        self.asignar_codigos(izquierda, prefijo + "0")
        self.asignar_codigos(derecha, prefijo + "1")

    def codificar(self):
        self.analizar_texto()
        self.asignar_codigos(self.simbolos)

        self.texto_codificado = "".join(self.codigos[char] for char in self.texto)

        total_bits = 0
        for s in self.simbolos:
            longitud = len(s.codigo)
            s.bits_totales = s.frecuencia * longitud
            s.longitud_promedio = s.probabilidad * longitud
            total_bits += s.bits_totales
            self.longitud_promedio += s.longitud_promedio

        self.eficiencia = self.entropia_total / self.longitud_promedio if self.longitud_promedio else 0

    def resumen(self) -> Dict:
        return {
            "Texto original": self.texto,
            "Total símbolos": self.total_simbolos,
            "Entropía total": self.entropia_total,
            "Longitud promedio": self.longitud_promedio,
            "Eficiencia": self.eficiencia,
            "Codigos": self.codigos,
            "Texto codificado": self.texto_codificado,
            "Símbolos": [
                {
                    "Caracter": s.caracter,
                    "Frecuencia": s.frecuencia,
                    "Probabilidad": s.probabilidad,
                    "IMutua": s.imutua,
                    "Entropía": s.entropia,
                    "Código": s.codigo,
                    "BitsTotales": s.bits_totales,
                    "LongitudPromedio": s.longitud_promedio,
                }
                for s in self.simbolos
            ]
        }
