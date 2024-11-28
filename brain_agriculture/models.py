from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)


@table_registry.mapped_as_dataclass
class Farmer:
    __tablename__ = 'farmers'

    ndoc: Mapped[str] = mapped_column(unique=True, primary_key=True)
    name: Mapped[str]
    farm_name: Mapped[str]
    city: Mapped[str]
    state: Mapped[str]
    total_area: Mapped[float]
    arable_area: Mapped[float]
    vegetation_area: Mapped[float]
    planted_crops: Mapped[str]
