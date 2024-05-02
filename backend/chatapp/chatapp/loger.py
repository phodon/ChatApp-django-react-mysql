import os
import logging

# Định nghĩa class AddLogIdFilter
class AddLogIdFilter(logging.Filter):
    def filter(self, record):
        record.log_id = os.urandom(8).hex()
        return True

