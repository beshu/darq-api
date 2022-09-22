from enum import Enum


class Role(str, Enum):
    admin = "admin"
    dev = "dev"
    simple_mortal = "simple_mortal"