# automatically generated by the FlatBuffers compiler, do not modify

# namespace: CustomAppProto

class MilkType(object):
    ONE_PERCENT = 0
    TWO_PERCENT = 1
    FAT_FREE = 2
    WHOLE = 3
    ALMOND = 4
    CASHEW = 5
    OAT = 6

def type_to_key(func): 
    return lambda input: next(
        key for key, value in func.__dict__.items() if value == input
    )

key = type_to_key(MilkType)(0)

print(key)
