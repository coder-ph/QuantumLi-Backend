import enum

class ShipmentStatusEnum(enum.Enum):
    PLANNED = 'planned'
    IN_TRANSIT = 'in transit'
    DELIVERED = 'delivered'
    CANCELED = 'canceled'

class ShippingMethodEnum(enum.Enum):
    ROAD = 'road'
    AIR = 'air'
    SEA = 'sea'
    RAIL = 'rail'