from django.test import TestCase
from ..models import Equipo
from ..nomenclators import TipoMedio, TipoMarca, TipoEstadoMedio


class EquiposTestCase(TestCase):
    """ Test relacionados a Equipos"""
    
    @classmethod
    def setUp(self):
        marca = TipoMarca.objects.create(tipo='la marca')

        equipo = Equipo(
            tipo=TipoMedio.EQUIPO,
            serie="roar",
            marca=marca,
            modelo=None,
            estado=TipoEstadoMedio.BIEN,
            ubicacion=None,
            inventario='inventario'
            )
        equipo.save()

    def test_creation_of_components(self):
        """Verificar creacion de Equipos """
        total = Equipo.objects.count()
        self.assertEqual(total, 1)

    def test_deletion(self):
        Equipo.objects.get(id=1).delete()
        total = Equipo.objects.count()
        self.assertEqual(total, 0)


# class WhateverTest(TestCase):

#     def create_whatever(self, title="only a test", body="yes, this is only a test"):
#         return Whatever.objects.create(title=title, body=body, created_at=timezone.now())

#     def test_whatever_creation(self):
#         w = self.create_whatever()
#         self.assertTrue(isinstance(w, Whatever))
#         self.assertEqual(w.__unicode__(), w.title)