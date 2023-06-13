from enum import Enum


class ProductCategory(Enum):
    BAG = 'BAG'
    CLOTH = 'CLOTH'
    FOOTWEAR = 'FOOTWEAR'

    @classmethod
    def choices(cls):
        return tuple((item.name, item.value) for item in cls)


class ProductSize(Enum):
    BIG = 'BIG'
    MEDIUM = 'MEDIUM'
    MINI = 'MINI'

    @classmethod
    def choices(cls):
        return tuple((item.name, item.value) for item in cls)


class ProductAvailability(Enum):
    IN_STOCK = 'IN_STOCK'
    SOLD_OUT = 'SOLD_OUT'

    @classmethod
    def choices(cls):
        return tuple((item.name, item.value) for item in cls)
