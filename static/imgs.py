import os
from TOCProject import settings
def get_acgimgs():
    return os.listdir(os.path.join(settings.BASE_DIR,"static","acgimg"))
