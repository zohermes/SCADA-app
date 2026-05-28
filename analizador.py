class Sensor:
    def __init__(self, nombre):
        self.nombre = nombre
        self.valor  = None

    def medir(self, v):
        self.valor = v 
    def estado(self):
        return "SIN CLASIFICAR"  


class SensorVrms(Sensor):
    def __init__(self):
        super().__init__("Vrms")

    def estado(self):
        if 209 <= self.valor <= 231:
            return "NORMAL"
        else: 
            return "FUERA DE RANGO"


class SensorIrms(Sensor):
    def __init__(self):
        super().__init__("Irms")

    def estado(self):
        if 0<= self.valor <=16:
            return "NORMAL"
        else: 
            return "SOBRECARGA"

class SensorTHD(Sensor):
    def __init__(self):
        super().__init__("THD")

    def estado(self):
        if self.valor < 5.0:
            return "THD OK"
        else: 
            return "THD ALTA"
    


class SensorFP(Sensor):
    def __init__(self):
        super().__init__("FP")

    def estado(self):
        if self.valor >= 0.9:
            return "FP OPTIMO"
        else:
            return "FP BAJO"# completar: "FP OPTIMO" si valor >= 0.9, si no "FP BAJO"
        pass


class AnalizadorRed:
    def __init__(self):
        self.sensores  = []
        self.historial = []   # lista de diccionarios, uno por ciclo
        self.alarmas_totales = 0

    def agregar(self, sensor):
        self.sensores.append(sensor)

    def ciclo(self, lecturas):
        alarmas_ciclo = 0
        vrms_val = 0
        potencia = 0

        for s, v in zip(self.sensores, lecturas):
            s.medir(v)
            est = s.estado()
            print(f"  {s.nombre:5}: {v} -> {est}")
            if "FUERA" in est or "ALTA" in est or "BAJO" in est or "SOBRECARGA" in est:
                alarmas_ciclo += 1
            if s.nombre == "Vrms": vrms_val = v

        # Calcular potencia activa: Vrms * Irms * FP
        potencia = lecturas[0] * lecturas[1] * lecturas[3]
        print(f"  Potencia activa: {potencia:.1f} W")

        if alarmas_ciclo > 0:
            print(f"  ⚠ {alarmas_ciclo} alarma(s) en este ciclo.")
            self.alarmas_totales += 1

        # Guardar este ciclo en el historial
        registro = {
            "vrms"    : vrms_val,
            "potencia": potencia,
            "alarmas" : alarmas_ciclo
        }
        self.historial.append(registro)  # completar: usar append para guardar registro