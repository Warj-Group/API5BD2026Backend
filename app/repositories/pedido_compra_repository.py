from typing import List, Optional

from sqlalchemy.orm import Session

from app.models.postgres.models import (
    DimPedidoCompra,
)


def get_pedidos_compra(db: Session) -> List[DimPedidoCompra]:
    """Retorna todos os pedidos de compra cadastrados."""
    return db.query(DimPedidoCompra).order_by(DimPedidoCompra.id_pedido).all()


def get_pedido_by_id(db: Session, pedido_id: int) -> Optional[DimPedidoCompra]:
    """Retorna um pedido de compra pelo id_pedido. None se não existir."""
    return (
        db.query(DimPedidoCompra).filter(DimPedidoCompra.id_pedido == pedido_id).first()
    )


def get_pedido_by_numero(db: Session, numero_pedido: str) -> Optional[DimPedidoCompra]:
    """Retorna um pedido de compra pelo numero_pedido. None se não existir."""
    return (
        db.query(DimPedidoCompra)
        .filter(DimPedidoCompra.numero_pedido == numero_pedido)
        .first()
    )


def get_pedidos_by_fornecedor(db: Session, fornecedor_id: int) -> List[DimPedidoCompra]:
    """Filtra pedidos de compra por fornecedor."""
    return (
        db.query(DimPedidoCompra)
        .filter(DimPedidoCompra.fornecedor_id == fornecedor_id)
        .all()
    )


def get_pedidos_by_status(db: Session, status: str) -> List[DimPedidoCompra]:
    """Filtra pedidos de compra por status."""
    return (
        db.query(DimPedidoCompra)
        .filter(DimPedidoCompra.status == status)
        .order_by(DimPedidoCompra.id_pedido)
        .all()
    )
