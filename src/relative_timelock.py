# Example 3: Create CSV timelock script
# Reference: code/chapter03/03_create_csv_script.py
from bitcoinutils.setup import setup
from bitcoinutils.keys import PrivateKey, P2pkhAddress, P2shAddress
from bitcoinutils.script import Script
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, Sequence
from bitcoinutils.utils import to_satoshis
from bitcoinutils.constants import TYPE_RELATIVE_TIMELOCK
setup('testnet')
sk_csv = PrivateKey('cRxebG1hY6vVgS9CSLNaEbEJaXkpZvc6nFeqqGT7v6gcW7MbzKNT')
pk_csv = sk_csv.get_public_key()
seq = Sequence(TYPE_RELATIVE_TIMELOCK, 3)
redeem_csv = Script([seq.for_script(), 'OP_CHECKSEQUENCEVERIFY', 'OP_DROP',
    'OP_DUP', 'OP_HASH160', pk_csv.get_address().to_hash160(), 'OP_EQUALVERIFY', 'OP_CHECKSIG'])
p2sh_csv = P2shAddress.from_script(redeem_csv)
print(f"P2SH Address: {p2sh_csv.to_string()}")
print(f"Time Lock: 3 blocks")



# Example 4: Spend CSV timelock script
# Reference: code/chapter03/04_spend_csv_script.py

txin_csv = TxInput('34f5bf0cf328d77059b5674e71442ded8cdcfc723d0136733e0dbf180861906f', 0, sequence=seq.for_input_sequence())
txout_csv = TxOutput(to_satoshis(0.00001), P2pkhAddress('myYHJtG3cyoRseuTwvViGHgP2efAvZkYa4').to_script_pub_key())
tx_csv = Transaction([txin_csv], [txout_csv])
sig_csv = sk_csv.sign_input(tx_csv, 0, redeem_csv)
txin_csv.script_sig = Script([sig_csv, pk_csv.to_hex(), redeem_csv.to_hex()])
print(f"Transaction size: {tx_csv.get_size()} bytes")