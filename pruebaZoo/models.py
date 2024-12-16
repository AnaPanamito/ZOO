from django.db import models

# Create your models here.
# Clase zoologico que hereda de models.Model
class Zoologico (models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    direccion = models.CharField('Direccion', max_length=100)
    hora_apertura = models.TimeField()
    hora_cierre = models.TimeField()
    capacidad_maxima = models.IntegerField()

    def __str__(self):
        return f"{self.nombre} {self.direccion}"

    def horario(self):
        return f"Abierto de {self.hora_apertura.strftime('%H:%M')} a {self.hora_cierre.strftime('%H:%M')}"

class Persona (models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    apellido = models.CharField('Apellido', max_length=100)
    direccion = models.CharField('Direccion', max_length=100)
    fecha_nacimiento = models.DateField()
    telefono = models.IntegerField()
    def __str__(self):
        return f"{self.nombre} {self.apellido}"
class Boleteria (Persona):
    ventas_disponibles = models.IntegerField()
    entradas_adquiridas = models.IntegerField()
    def usa_los_servicios(self):
        pass

class Veterinario (Persona):
    cedula = models.IntegerField()
    especialidad = models.CharField('Especialidad', max_length=100)
    chequeo_realizado = models.BooleanField(default=False)
    tratamiento_prescrito = models.BooleanField(default=False)
    def realizar_chequeo(self):
        self.chequeo_realizado = True
        self.save()
    def prescribir_tratamiento(self):
        self.tratamiento_prescrito = True
        self.save()
    def resetear_chequeo(self):
        self.chequeo_realizado = False
        self.save()
    def resetear_tratamiento(self):
        self.tratamiento_prescrito = False
        self.save()
    def __str__(self):
        return f"{self.nombre} - {self.especialidad}"


class Cuidador(Persona):
    alimentar = models.BooleanField(default=False)
    limpiar_jaula = models.BooleanField(default=False)
    agregar_animal = models.BooleanField(default=False)
    consultar_historial_salud = models.BooleanField(default=False)

    def realizar_alimentacion(self):
        self.alimentar = True
        self.save()

    def limpiar_jaulas(self):
        self.limpiar_jaula = True
        self.save()

    def agregar_nuevo_animal(self, animal):
        self.agregar_animal = True
        self.animales.add(animal)
        self.save()

    def consultar_salud_animales(self):
        self.consultar_historial_salud = True
        self.save()

    def resetear_tareas(self):
        self.alimentar = False
        self.limpiar_jaula = False
        self.agregar_animal = False
        self.consultar_historial_salud = False
        self.save()

    def __str__(self):
        return f"Cuidador: {self.nombre} {self.apellido} "


class Jaula(models.Model):
    numero_jaula = models.IntegerField(unique=True)
    capacidad = models.IntegerField()
    ubicacion = models.CharField(max_length=100)

    esta_limpia = models.BooleanField(default=True)
    capacidad_verificada = models.BooleanField(default=False)

    def asignar_animal(self, animal):
        # Verificar si hay espacio en la jaula
        if self.animales.count() < self.capacidad:
            animal.jaula = self
            animal.save()
            return True
        else:
            raise ValidationError("La jaula está en su capacidad máxima")

    def limpiar_jaula(self):
        # Marcar la jaula como limpia
        self.esta_limpia = True
        self.save()

    def verificar_capacidad(self):
        # Verificar y actualizar el estado de capacidad
        animales_actuales = self.animales.count()
        self.capacidad_verificada = animales_actuales <= self.capacidad
        self.save()
        return self.capacidad_verificada

    def __str__(self):
        return f"Jaula #{self.numero_jaula} - {self.ubicacion} (Capacidad: {self.capacidad})"

    def estado_jaula(self):
        # Método para obtener un resumen del estado de la jaula
        return {
            'numero_jaula': self.numero_jaula,
            'ubicacion': self.ubicacion,
            'capacidad_total': self.capacidad,
            'animales_actuales': self.animales.count(),
            'esta_limpia': self.esta_limpia,
            'capacidad_verificada': self.capacidad_verificada
        }

    class Meta:
        ordering = ['numero_jaula']  # Ordenar por número de jaula

class Animal(models.Model):
    ESTADOS_SALUD = [
        ('EXCELENTE', 'Excelente'),
        ('BUENO', 'Bueno'),
        ('REGULAR', 'Regular'),
        ('CRITICO', 'Crítico')
    ]

    nombre = models.CharField(max_length=100)
    nombre_cientifico = models.CharField(max_length=100)
    edad = models.IntegerField()
    estado_salud = models.CharField(
        max_length=20,
        choices=ESTADOS_SALUD,
        default='BUENO'
    )

    jaula = models.ForeignKey(
        'Jaula',
        on_delete=models.SET_NULL,
        related_name='animales',
        null=True,
        blank=True
    )

    fecha_ingreso = models.DateField(auto_now_add=True)
    requiere_atencion_especial = models.BooleanField(default=False)

    def actualizar_estado_salud(self, nuevo_estado):
        # actualizar el estado de salud
        if nuevo_estado in dict(self.ESTADOS_SALUD):
            self.estado_salud = nuevo_estado
            self.save()

    def necesita_atencion_veterinaria(self):
        # Ver  si necesita atención veterinaria
        return self.estado_salud in ['REGULAR', 'CRITICO']

    def __str__(self):
        return f"{self.nombre} ({self.nombre_cientifico})"

    def informacion_completa(self):
        return {
            'nombre': self.nombre,
            'nombre_cientifico': self.nombre_cientifico,
            'edad': self.edad,
            'estado_salud': self.get_estado_salud_display(),
            'jaula': self.jaula.ubicacion if self.jaula else 'Sin asignar',
            'requiere_atencion_especial': self.requiere_atencion_especial
        }

    class Meta:
        verbose_name_plural = "Animales"


class TipoAlimento(models.Model):
    CATEGORIAS_ALIMENTO = [
        ('HERBIVORO', 'Alimento para Herbívoros'),
        ('CARNIVORO', 'Alimento para Carnívoros'),
        ('OMNIVORO', 'Alimento para Omnívoros'),
        ('ESPECIAL', 'Dieta Especial')
    ]

    nombre = models.CharField(max_length=100)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS_ALIMENTO, default='ESPECIAL')


    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()})"


class Alimentacion(models.Model):
    ESTADO_ALIMENTACION = [
        ('PROGRAMADA', 'Alimentación Programada'),
        ('REALIZADA', 'Alimentación Realizada'),
        ('INCOMPLETA', 'Alimentación Incompleta'),
        ('CANCELADA', 'Alimentación Cancelada')
    ]

    animal = models.ForeignKey('Animal', on_delete=models.CASCADE, related_name='alimentaciones')
    tipo_alimento = models.ForeignKey(TipoAlimento, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return f"{self.animal} {self.tipo_alimento}"

    fecha_programada = models.DateTimeField()
    fecha_realizada = models.DateTimeField(null=True, blank=True)

    cantidad = models.FloatField()  # Cantidad de alimento en kg o unidades
    estado = models.CharField(
        max_length=20,
        choices=ESTADO_ALIMENTACION,
        default='PROGRAMADA'
    )

    observaciones = models.TextField(blank=True, null=True)

    alimentacion_completa = models.BooleanField(default=False)
    requiere_supervision_especial = models.BooleanField(default=False)

    def realizar_alimentacion(self, observaciones=None):
        """
        Método para registrar que la alimentación se ha realizado
        """
        self.fecha_realizada = timezone.now()
        self.estado = 'REALIZADA'
        self.alimentacion_completa = True

        if observaciones:
            self.observaciones = observaciones

        self.save()
        return True

    def cancelar_alimentacion(self, razon=None):
        """
        Método para cancelar una alimentación programada
        """
        self.estado = 'CANCELADA'

        if razon:
            self.observaciones = razon

        self.save()
        return True

    def verificar_necesidades_especiales(self):
        """
      Verificar si el animal requiere alimentación especial
        """
        if self.animal.estado_salud in ['REGULAR', 'CRITICO']: self.requiere_supervision_especial = Trueself.save()


def __str__(self):
    return f"Alimentación de {self.animal.nombre} - {self.fecha_programada}"


class Meta:
    verbose_name_plural = "Alimentaciones"
    ordering = ['-fecha_programada']



