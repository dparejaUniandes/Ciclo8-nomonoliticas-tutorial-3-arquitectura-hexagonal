from aeroalpes.config.db import db
from aeroalpes.modulos.vuelos.dominio.repositorios import RepositorioReservas, RepositorioProveedores
from aeroalpes.modulos.vuelos.dominio.objetos_valor import NombreAero, Odo, Leg, Segmento, Itinerario, CodigoIATA
from aeroalpes.modulos.vuelos.dominio.entidades import Proveedor, Aeropuerto, Reserva
from aeroalpes.modulos.vuelos.dominio.fabricas import FabricaVuelos
from .dto import Reserva as ReservaDTO
from .mapeadores import MapeadorReserva
from uuid import UUID

class RepositorioProveedoresSQLite(RepositorioProveedores):

    def obtener_por_id(self, id: UUID) -> Reserva:
        ...

    def obtener_todos(self) -> list[Reserva]:
        origen=Aeropuerto(codigo="CPT", nombre="Cape Town International")
        destino=Aeropuerto(codigo="JFK", nombre="JFK International Airport")
        legs=[Leg(origen=origen, destino=destino)]
        segmentos = [Segmento(legs)]
        odos=[Odo(segmentos=segmentos)]

        proveedor = Proveedor(codigo=CodigoIATA(codigo="AV"), nombre=NombreAero(nombre= "Avianca"))
        proveedor.itinerarios = [Itinerario(odos=odos, proveedor=proveedor)]
        return [proveedor]

    def agregar(self, entity: Reserva):
        ...

    def actualizar(self, entity: Reserva):
        ...

    def eliminar(self, entity_id: UUID):
        ...


class RepositorioReservasSQLite(RepositorioReservas):

    def __init__(self):
        self._fabrica_vuelos: FabricaVuelos = FabricaVuelos()

    @property
    def fabrica_vuelos(self):
        return self._fabrica_vuelos

    def obtener_por_id(self, id: UUID) -> Reserva:
        reserva_dto = db.session.query(ReservaDTO).filter_by(id=str(id)).one()
        return self.fabrica_vuelos.crear_objeto(reserva_dto, MapeadorReserva())

    def obtener_todos(self) -> list[Reserva]:
        ...

    def agregar(self, reserva: Reserva):
        reserva_dto = self.fabrica_vuelos.crear_objeto(reserva, MapeadorReserva())
        db.session.add(reserva_dto)
        db.session.commit()

    def actualizar(self, reserva: Reserva):
        ...

    def eliminar(self, reserva_id: UUID):
        ...