from sigeme_project import logger
from django.test import TestCase, RequestFactory, Client, tag
from ..models import Equipo, Computadora, Ubicacion, Periferico, Componente, \
      Movimiento, MovimientoComponente
from ..nomenclators import TipoPeriferico, TipoMarca, TipoModelo, \
       TipoDepartamento, TipoDivision, TipoSistemaOperativo, TipoEstadoSello, \
       TipoMunicipio, TipoProvincia, TipoUnidad, TipoPiso

# en caso de necesitar validacion para csrf, pasar parametro al client
# csrf_client = Client(enforce_csrf_checks=True)


@tag('core')
class ResponseFormatTestCase(TestCase):
    """ Test relacionados a Equipos"""

    def setUp(self):
        self.client = Client()

    def test_formato_respuesta(self):

        response = self.client.get("/api/medios/")

        content = response.content
        context = response.context
        code = response.status_code
        data = response.json()

        self.assertTrue(isinstance(content, bytes))
        self.assertEqual(code, 200)
        self.assertEqual(context, None)
        self.assertTrue('links' in data)
        self.assertTrue('items' in data)
        self.assertTrue('total' in data)


@tag('api')
class EquipoTestCase(TestCase):
    """Test sobre los endpoint de equipo"""

    path = 'equipos'
    data = {"tipo": "equipo", "estado": "bien",
    "serie": "la serie",
    "marca": 1,
    "modelo":  {
        "id": 1,
        "tipo": "ok",
        "marca": 1
    },
    "ubicacion": 1,
     "inventario": "el inventario"}
    _instance = None

    def setUp(self):
        marca = TipoMarca(tipo="primera marca")
        marca.save()
        modelo = TipoModelo(tipo="primer modelo", marca=marca)
        modelo.save()

        provincia = TipoProvincia(tipo="la habana")
        provincia.save()
        division = TipoDivision(tipo="oeste", provincia=provincia)
        division.save()
        municipio = TipoMunicipio(tipo="10 de octubre", provincia=provincia)
        municipio.save()
        unidad = TipoUnidad(tipo="unidad", division=division, municipio=municipio)
        unidad.save()
        departamento = TipoDepartamento(tipo="dpto", division=division)
        departamento.save()
        piso = TipoPiso(tipo="1ro", unidad=unidad)
        piso.save()

        ubicacion = Ubicacion(
            division=division,
            departamento=departamento,
            municipio=municipio,
            unidad=unidad,
            piso=piso)
        ubicacion.save()

        self._instance = Equipo(
        marca=marca,
        tipo=self.data['tipo'],
        estado=self.data['estado'],
        inventario="inventario1",
        serie="serie1",
        ubicacion=ubicacion,
        modelo=modelo
    	)
        self._instance.save()

        self.client = Client()

    def test_1_crear_equipo(self):
        response = self.client.post(f"/api/{self.path}/", self.data, content_type='application/json')
        item = response.json()

        self.assertTrue(item.get('tipo') == self.data.get('tipo'))
        self.assertTrue(item.get('marca') == self.data.get('marca'))
        self.assertTrue(Equipo.objects.count() == 2)

    def test_2_obtener_equipo(self):
        response = self.client.get(f"/api/{self.path}/1/", content_type='application/json')
        code = response.status_code
        item = response.json()

        self.assertEqual(code, 200)
        self.assertEqual(item['id'], 1)
        self.assertEqual(item['serie'], self._instance.serie)
        self.assertTrue(Equipo.objects.count() == 1)

    def test_3_actualizar_equipo(self):
        updated = {'id': 1, 'inventario': 'inventario actualizado'}
        self.data = {**self.data, **updated}
        response = self.client.put(f"/api/{self.path}/1/", self.data, content_type='application/json')
        code = response.status_code
        item = response.json()

        self.assertEqual(code, 200)
        self.assertTrue(item['inventario'], updated['inventario'])
        self.assertTrue(Equipo.objects.get(id=1).inventario, item['inventario'])
        self.assertTrue(Movimiento.objects.count() == 1)

    def test_4_eliminar_equipo(self):
        response = self.client.delete(f"/api/{self.path}/1/")
        code = response.status_code

        self.assertEqual(code, 204)
        try:
            Equipo.objects.get(id=1)
        except Equipo.DoesNotExist:
            self.assertTrue(1) 


    def test_5_listar_equipos(self):
        response = self.client.get(f"/api/{self.path}/")
        data = response.json()
        code = response.status_code

        self.assertEqual(code, 200)
        self.assertTrue(data['total'] == 1)

@tag('api')
class PerifericoTestCase(TestCase):
    """Test sobre los endpoint de perifericos"""

    path = 'perifericos'
    data = {"tipo": "periferico", "estado": "bien",
    "serie": "la serie",
    "marca": 1,
    "modelo":  {
        "id": 1,
        "tipo": "ok",
        "marca": 1
    },
    "ubicacion": 1,
    "sello": "# de sello",
    "conectado_a": None,
    "tipo_periferico": 1,
    }
    _instance = None

    def setUp(self):
        self.tipo_periferico = TipoPeriferico(tipo="linux")
        self.tipo_periferico.save()
        marca = TipoMarca(tipo="primera marca")
        marca.save()
        modelo = TipoModelo(tipo="primer modelo", marca=marca)
        modelo.save()

        provincia = TipoProvincia(tipo="la habana")
        provincia.save()
        division = TipoDivision(tipo="oeste", provincia=provincia)
        division.save()
        municipio = TipoMunicipio(tipo="10 de octubre", provincia=provincia)
        municipio.save()
        unidad = TipoUnidad(tipo="unidad", division=division, municipio=municipio)
        unidad.save()
        departamento = TipoDepartamento(tipo="dpto", division=division)
        departamento.save()
        piso = TipoPiso(tipo="1ro", unidad=unidad)
        piso.save()

        ubicacion = Ubicacion(
            division=division,
            departamento=departamento,
            municipio=municipio,
            unidad=unidad,
            piso=piso)
        ubicacion.save()

        self._instance = Periferico(
        marca=marca,
        tipo=self.data['tipo'],
        estado=self.data['estado'],
        serie="serie1",
        ubicacion=ubicacion,
        modelo=modelo,
        tipo_periferico=self.tipo_periferico,
        conectado_a=None
    	)
        self._instance.save()

        self.client = Client()
    
    def test_1_crear_periferico(self):
        response = self.client.post(f"/api/{self.path}/", self.data, content_type='application/json')
        item = response.json()
        
        self.assertTrue(item.get('tipo') == self.data.get('tipo'))
        self.assertTrue(item.get('marca') == self.data.get('marca'))
        self.assertTrue(Periferico.objects.count() == 2)

    def test_2_obtener_periferico(self):
        response = self.client.get(f"/api/{self.path}/1/", content_type='application/json')
        code = response.status_code
        item = response.json()

        self.assertEqual(code, 200)
        self.assertEqual(item['id'], 1)
        self.assertEqual(item['serie'], self._instance.serie)
        self.assertTrue(Periferico.objects.count() == 1)

    def test_3_actualizar_periferico(self):
        updated = {'id': 1, 'serie': 'la nueva serie'}
        self.data = {**self.data, **updated}
        response = self.client.put(f"/api/{self.path}/1/", self.data, content_type='application/json')
        code = response.status_code
        item = response.json()

        self.assertEqual(code, 200)
        self.assertTrue(item['serie'], updated['serie'])
        self.assertTrue(Periferico.objects.get(id=1).tipo_periferico, self.tipo_periferico)
        self.assertTrue(Movimiento.objects.count() == 1)
    
    def test_4_eliminar_periferico(self):
        response = self.client.delete(f"/api/{self.path}/1/")
        code = response.status_code

        self.assertEqual(code, 204)
        try:
            Periferico.objects.get(id=1)
        except Periferico.DoesNotExist:
            self.assertTrue(1) 
        
    def test_5_listar_Perifericos(self):
        response = self.client.get(f"/api/{self.path}/")
        data = response.json()
        code = response.status_code

        self.assertEqual(code, 200)
        self.assertTrue(data['total'] == 1)

@tag('api')
class ComputadoraTestCase(TestCase):
    """Test sobre los endpoint de computadoras"""

    path = 'computadoras'
    data = {"tipo": "computadora", "estado": "bien",
    "serie": "la serie",
    "marca": 1,
    "modelo":  {
        "id": 1,
        "tipo": "ok",
        "marca": 1
    },
    "ubicacion": 1,
    "sello": "# de sello",
    "estado_sello": TipoEstadoSello.BIEN,
    "ip": "40.40.40.40",
    "mac": "sjowl23pol32p23322",
    "nombrepc": "juancito",
    "usuario": "juan",
    "es_servidor": False,
    "sistema_operativo":1
    }
    _instance = None

    def setUp(self):
        so = TipoSistemaOperativo(tipo="linux")
        so.save()
        marca = TipoMarca(tipo="primera marca")
        marca.save()
        modelo = TipoModelo(tipo="primer modelo", marca=marca)
        modelo.save()

        provincia = TipoProvincia(tipo="la habana")
        provincia.save()
        division = TipoDivision(tipo="oeste", provincia=provincia)
        division.save()
        municipio = TipoMunicipio(tipo="10 de octubre", provincia=provincia)
        municipio.save()
        unidad = TipoUnidad(tipo="unidad", division=division, municipio=municipio)
        unidad.save()
        departamento = TipoDepartamento(tipo="dpto", division=division)
        departamento.save()
        piso = TipoPiso(tipo="1ro", unidad=unidad)
        piso.save()

        ubicacion = Ubicacion(
            division=division,
            departamento=departamento,
            municipio=municipio,
            unidad=unidad,
            piso=piso)
        ubicacion.save()

        self._instance = Computadora(
        marca=marca,
        tipo=self.data['tipo'],
        estado=self.data['estado'],
        sello=self.data['sello'],
        estado_sello=self.data['estado_sello'],
        serie="serie1",
        ubicacion=ubicacion,
        modelo=modelo,
        sistema_operativo=so,
        nombrepc=self.data['nombrepc'],
        ip=self.data['ip'],
        mac=self.data['mac'],
        usuario=self.data['usuario'],
    	)
        self._instance.save()

        self.client = Client()
    
    def test_1_crear_computadora(self):
        response = self.client.post(f"/api/{self.path}/", self.data, content_type='application/json')
        item = response.json()
        
        self.assertTrue(item.get('tipo') == self.data.get('tipo'))
        self.assertTrue(item.get('marca') == self.data.get('marca'))
        self.assertTrue(Computadora.objects.count() == 2)

    def test_2_obtener_computadora(self):
        response = self.client.get(f"/api/{self.path}/1/", content_type='application/json')
        code = response.status_code
        item = response.json()

        self.assertEqual(code, 200)
        self.assertEqual(item['id'], 1)
        self.assertEqual(item['serie'], self._instance.serie)
        self.assertTrue(Computadora.objects.count() == 1)

    def test_3_actualizar_computadora(self):
        updated = {'id': 1, 'estado_sello': TipoEstadoSello.SIN_SELLO}
        self.data = {**self.data, **updated}
        response = self.client.put(f"/api/{self.path}/1/", self.data, content_type='application/json')
        code = response.status_code
        item = response.json()

        self.assertEqual(code, 200)
        self.assertTrue(item['estado_sello'], updated['estado_sello'])
        self.assertTrue(Computadora.objects.get(id=1).estado_sello, item['estado_sello'])
        self.assertTrue(Movimiento.objects.count() == 1)
    
    def test_4_eliminar_computadora(self):
        response = self.client.delete(f"/api/{self.path}/1/")
        code = response.status_code

        self.assertEqual(code, 204)
        try:
            Computadora.objects.get(id=1)
        except Computadora.DoesNotExist:
            self.assertTrue(1)
        
    def test_5_listar_computadoras(self):
        response = self.client.get(f"/api/{self.path}/")
        data = response.json()
        code = response.status_code

        self.assertEqual(code, 200)
        self.assertTrue(data['total'] == 1)


@tag('api')
class ComponenteTestCase(TestCase):
    """Test sobre los endpoint de computadoras"""

    path = 'componentes'

    data = {"tipo": "componente", "estado": "bien",
    "serie": "la serie",
    "marca": 1,
    "modelo":  {
        "id": 1,
        "tipo": "ok",
        "marca": 1
    },
    "ubicacion": 1,
    "sello": "# de sello",
    "medio": 1,
    "tipo_componente": "disco",

    }

    data_computadora = {"tipo": "computadora", "estado": "bien",
    "serie": "la serie comp",
    "marca": 1,
    "modelo":  {
        "id": 1,
        "tipo": "ok",
        "marca": 1
    },
    "ubicacion": 1,
    "sello": "# de sello",
    "estado_sello": TipoEstadoSello.BIEN,
    "ip": "40.40.40.40",
    "mac": "sjowl23pol32p23322",
    "nombrepc": "juancito",
    "usuario": "juan",
    "es_servidor": False,
    "sistema_operativo":1
    }
    _instance = None

    def setUp(self):
        so = TipoSistemaOperativo(tipo="linux")
        so.save()
        marca = TipoMarca(tipo="primera marca")
        marca.save()
        modelo = TipoModelo(tipo="primer modelo", marca=marca)
        modelo.save()

        provincia = TipoProvincia(tipo="la habana")
        provincia.save()
        division = TipoDivision(tipo="oeste", provincia=provincia)
        division.save()
        municipio = TipoMunicipio(tipo="10 de octubre", provincia=provincia)
        municipio.save()
        unidad = TipoUnidad(tipo="unidad", division=division, municipio=municipio)
        unidad.save()
        departamento = TipoDepartamento(tipo="dpto", division=division)
        departamento.save()
        piso = TipoPiso(tipo="1ro", unidad=unidad)
        piso.save()

        ubicacion = Ubicacion(
            division=division,
            departamento=departamento,
            municipio=municipio,
            unidad=unidad,
            piso=piso)
        ubicacion.save()

        self._instance_computadora = Computadora(
        marca=marca,
        tipo=self.data_computadora['tipo'],
        estado=self.data_computadora['estado'],
        sello=self.data_computadora['sello'],
        estado_sello=self.data_computadora['estado_sello'],
        serie="serie1",
        ubicacion=ubicacion,
        modelo=modelo,
        sistema_operativo=so,
        nombrepc=self.data_computadora['nombrepc'],
        ip=self.data_computadora['ip'],
        mac=self.data_computadora['mac'],
        usuario=self.data_computadora['usuario'],
    	)

        self._instance_computadora2 = Computadora(
        marca=marca,
        tipo=self.data_computadora['tipo'],
        estado=self.data_computadora['estado'],
        sello=self.data_computadora['sello']+"2",
        estado_sello=self.data_computadora['estado_sello'],
        serie="serie2",
        ubicacion=ubicacion,
        modelo=modelo,
        sistema_operativo=so,
        nombrepc=self.data_computadora['nombrepc'],
        ip=self.data_computadora['ip'],
        mac=self.data_computadora['mac'],
        usuario=self.data_computadora['usuario'],
        )
        self._instance = Componente(
        	medio=self._instance_computadora,
            tipo_componente=self.data['tipo_componente'],

    		)

        self._instance_computadora.save()
        self._instance_computadora2.save()
        self._instance.save()

        self.client = Client()
    
    def test_1_crear_componente(self):
        response = self.client.post(f"/api/{self.path}/", self.data, content_type='application/json')
        item = response.json()
        
        self.assertTrue(item.get('tipo') == self.data.get('tipo'))
        self.assertTrue(item.get('marca') == self.data.get('marca'))
        self.assertTrue(Computadora.objects.count() == 2)
        self.assertTrue(Componente.objects.count() == 2)

    def test_2_obtener_componente(self):
        response = self.client.get(f"/api/{self.path}/3/", content_type='application/json')
        code = response.status_code
        item = response.json()

        self.assertEqual(code, 200)
        self.assertEqual(item['id'], 3)
        self.assertEqual(item['serie'], self._instance.serie)
        self.assertTrue(Componente.objects.count() == 1)

    def test_3_actualizar_componente(self):
        updated = {'id': 2, 'capacidad': '2TB'}
        self.data = {**self.data, **updated}
        response = self.client.put(f"/api/{self.path}/3/", self.data, content_type='application/json')
        code = response.status_code
        item = response.json()
        logger.info('tremendo')
        self.assertEqual(code, 200)
        self.assertTrue(item['capacidad'], updated['capacidad'])
        self.assertTrue(Componente.objects.get(id=3).capacidad, item['capacidad'])

    def test_3_actualizar_medio_asociada(self):
        logger.info('test_3_actualizar_computadora_asociada')
        updated = {'id': 3, 'medio': 2}
        self.data = {**self.data, **updated}
        response = self.client.put(f"/api/{self.path}/3/", self.data, content_type='application/json')
        code = response.status_code
        item = response.json()
        
        self.assertEqual(code, 200)
        self.assertTrue(item['medio'], updated['medio'])
        self.assertTrue(Componente.objects.get(id=3).medio, item['medio'])
        self.assertTrue(MovimientoComponente.objects.count() == 1)
    
    def test_4_eliminar_componente(self):
        response = self.client.delete(f"/api/{self.path}/3/")
        code = response.status_code

        self.assertEqual(code, 204)
        try:
            Componente.objects.get(id=2)
        except Componente.DoesNotExist:
            self.assertTrue(1) 
        
    def test_5_listar_componentes(self):
        response = self.client.get(f"/api/{self.path}/")
        data = response.json()
        code = response.status_code

        self.assertEqual(code, 200)
        self.assertTrue(data['total'] == 1)
