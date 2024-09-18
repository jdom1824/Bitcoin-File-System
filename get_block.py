#get_block.py

'''
┌─────────────┬──────────────┬───────────────┬───────┬─────────────────────────────────────┐
│ Name        │ Example Data │ Format        │ Size  │ Example Bytes                       │
├─────────────┼──────────────┼───────────────┼───────┼─────────────────────────────────────┤
│ Magic Bytes │              │ bytes         │     4 │ F9 BE B4 D9                         │
│ Command     │ "getdata"    │ ascii bytes   │    12 │ 67 65 74 64 61 74 61 00 00 00 00 00 │
│ Payload Size│ 37           │ little-endian │     4 │ 25 00 00 00                         │
│ Checksum    │              │ bytes         │     4 │ 72 7D 5D 7F                         │
│ Payload     │              │               │       │                                     │
│   Count     │ 1            │ var_int       │     1 │ 01                                  │
│   Type      │ 2 (MSG_BLOCK)│ little-endian │     4 │ 02 00 00 00                         │
│   Block Hash│              │ little-endian │    32 │ 6F E2 8C 0A B6 F1 B3 72 C1 A6 A2 46 │
│             │              │               │       │ AE 63 F7 4F 31 E1 92 A1 00 00 00 00 │
│             │              │               │       │ 00 00 00 00 00 00 00 00             │
└─────────────┴──────────────┴───────────────┴───────┴─────────────────────────────────────┘
'''