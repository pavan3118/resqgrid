from datetime import datetime
from enum import StrEnum

from geoalchemy2 import Geography
from sqlalchemy import (
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
    func,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class IncidentStatus(StrEnum):
    CREATED = "CREATED"
    SEARCHING = "SEARCHING"
    ASSIGNED = "ASSIGNED"
    ACCEPTED = "ACCEPTED"
    EN_ROUTE = "EN_ROUTE"
    ON_SCENE = "ON_SCENE"
    RESOLVED = "RESOLVED"


class Base(DeclarativeBase):
    pass


class Responder(Base):
    __tablename__ = "responders"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        unique=True,
    )

    responder_type: Mapped[str] = mapped_column(
        Enum(
            "POLICE",
            "AMBULANCE",
            "FIRE",
            name="responder_type",
        ),
        nullable=False,
    )

    status: Mapped[str] = mapped_column(
        Enum(
            "AVAILABLE",
            "BUSY",
            "OFFLINE",
            name="responder_status",
        ),
        nullable=False,
        default="OFFLINE",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    location: Mapped["ResponderLocation | None"] = relationship(
        back_populates="responder",
        uselist=False,
        cascade="all, delete-orphan",
    )

    assignments: Mapped[list["IncidentAssignment"]] = relationship(
        back_populates="responder",
    )


class ResponderLocation(Base):
    __tablename__ = "responder_locations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    responder_id: Mapped[int] = mapped_column(
        ForeignKey(
            "responders.id",
            ondelete="CASCADE",
        ),
        unique=True,
        nullable=False,
    )

    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    location = mapped_column(
        Geography(
            geometry_type="POINT",
            srid=4326,
            spatial_index=True,
        ),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    responder: Mapped["Responder"] = relationship(
        back_populates="location",
    )


class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    title: Mapped[str] = mapped_column(
        String(150),
        nullable=False,
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    priority: Mapped[str] = mapped_column(
        Enum(
            "LOW",
            "MEDIUM",
            "HIGH",
            "CRITICAL",
            name="incident_priority",
        ),
        nullable=False,
        default="HIGH",
    )

    status: Mapped[str] = mapped_column(
        Enum(
            IncidentStatus,
            name="incident_status",
        ),
        nullable=False,
        default="CREATED",
    )

    latitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    longitude: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    location = mapped_column(
        Geography(
            geometry_type="POINT",
            srid=4326,
            spatial_index=True,
        ),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    assignments: Mapped[list["IncidentAssignment"]] = relationship(
        back_populates="incident",
        cascade="all, delete-orphan",
    )


class IncidentAssignment(Base):
    __tablename__ = "incident_assignments"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    incident_id: Mapped[int] = mapped_column(
        ForeignKey(
            "incidents.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    responder_id: Mapped[int] = mapped_column(
        ForeignKey(
            "responders.id",
            ondelete="CASCADE",
        ),
        nullable=False,
    )

    assigned_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    accepted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    incident: Mapped["Incident"] = relationship(
        back_populates="assignments",
    )

    responder: Mapped["Responder"] = relationship(
        back_populates="assignments",
    )
