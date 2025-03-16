# lunar-rover-project

## Client - Server Flow

1. Prepare Data:
   ➤ Add sequence number → Compress → Encrypt
2. Add Integrity Checks:
   ➤ Generate CRC checksum → Append HMAC
3. Transmit:
   ➤ Send packet via UDP
4. On Receiving Side:
   ➤ Verify HMAC → Decrypt → Decompress → Verify Checksum → Process Data
