"""
This module defines all the byte values to be used as variable names for readability and ease of use
"""

# Data
ON = b'\x01'
OFF = b'\x00'

# Packetization
SYNC_PATTERN = b'5.\xf8S'
SEED = b'\xff\xff'

# Housekeeping
CDH_HK_REQUEST = b'\x55'
VRUM_HK_OUT_OP = b'\x56'

# Science
CDH_SCI_REQUEST = b'\x5c'
VRUM_SCI_OUT_OP = b'\x5d'

# Configuration
CDH_CONFIG_REQUEST = b'\x5e'
CDH_CONFIG_OP = b'\x95'
VRUM_CONFIG_OUT_OP = b'\x5f'
VRUM_CONFIG_ACK_OP = b'\x96'

# Analog
CDH_ANALOG_CTRL = b'\xa5'
VRUM_ANALOG_OP = b'\xa6'

# Scalar 1
CDH_SCALAR1_CTRL = b'\xa7'
VRUM_SCALAR1_OP = b'\xa9'

# Scalar 2
CDH_SCALAR2_CTRL = b'\xaa'
VRUM_SCALAR2_OP = b'\xab'

# Star Tracker 1
CDH_STAR_TRACK1_CTRL = b'\xac'
VRUM_STAR_TRACK1_OP = b'\xad'

# Star Tracker 2
CDH_STAR_TRACK2_CTRL = b'\xae'
VRUM_STAR_TRACK2_OP = b'\xaf'

# Time of Tone
CDH_TIME_OF_TONE = b'\xc5'
VRUM_TIME_ACK_OP = b'\xc6'

# Science Stream
CDH_SCIENCE_STREAM_CTRL = b'\xc7'
VRUM_SCIENCE_STREAM_OP = b'\xc9'

# Gain Enable/Disable
CDH_MAG_GAIN_CTRL = b'\xf5'
VRUM_MAG_GAIN_OP = b'\xf6'

# Gain Configuration
CDH_MAG_GAIN_CONFIG = b'\xf7'
VRUM_MAG_GAIN_CONFIG = b'\xf9'
