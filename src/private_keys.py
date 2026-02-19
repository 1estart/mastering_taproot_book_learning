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

# Taproot uses x-only public keys (32 bytes)
taproot_pubkey = key.public_hex[2:] # Remove the 02/03 prefix
print(f"X-only Public Key: {taproot_pubkey}")

# Generate different address types from the same key
legacy_address = key.address()# P2PKH
segwit_native = key.address(encoding='bech32') # P2WPKH
segwit_p2sh = key.address(encoding='base58', script_type='p2sh') # P2SH-P2WPKH
taproot_address = key.address(script_type='p2tr') # P2TR



print(f"Legacy (P2PKH): {legacy_address}")
print(f"SegWit Native: {segwit_native}")
print(f"SegWit P2SH: {segwit_p2sh}")
print(f"Taproot: {taproot_address}")