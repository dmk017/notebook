MAX_CALLBACK_PACK_LENGTH = 64
MODEL_PREFIX = 2
OBJECT_ID_LENGTH = 24

def safetyCallbackKey(key: str):
  maxLength = MAX_CALLBACK_PACK_LENGTH - MODEL_PREFIX - OBJECT_ID_LENGTH
  return key[:maxLength - 1]