from bitcoinlib.keys import Key
 # Generate a new Bitcoin key pair
key = Key()
 
# Extract the private key in different formats
private_key_hex = key.private_hex # 32 bytes (256-bit) in hexadecimal
private_key_wif = key.wif() # Wallet Import Format

print(f"Private Key (HEX): {private_key_hex}")
print(f"Private Key (WIF): {private_key_wif}")