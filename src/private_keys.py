from bitcoinlib.keys import Key
 # Generate a new Bitcoin key pair
key = Key()
 
# Extract the private key in different formats
private_key_hex = key.private_hex # 32 bytes (256-bit) in hexadecimal
private_key_wif = key.wif() # Wallet Import Format

print(f"Private Key (HEX): {private_key_hex}")
print(f"Private Key (WIF): {private_key_wif}")

# Generate public keys in both formats
public_key_compressed = key.public_hex # 33 bytes
public_key_uncompressed = key.public_uncompressed_hex # 65 bytes

print(f"Compressed: {public_key_compressed}")
print(f"Uncompressed: {public_key_uncompressed[:70]}...")
 # Truncated for display