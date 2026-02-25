# Chapter environment: bitcoinutils (load once, reuse in subsequent code cells)
from bitcoinutils.setup import setup
from bitcoinutils.keys import PrivateKey, P2pkhAddress, P2wpkhAddress
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, TxWitnessInput
from bitcoinutils.utils import to_satoshis
from bitcoinutils.script import Script
setup('testnet')


# Example 1: Legacy vs SegWit signature comparison
# Reference: code/chapter04/01_legacy_vs_segwit_comparison.py

sk = PrivateKey('cPeon9fBsW2BxwJTALj3hGzh9vm8C52Uqsce7MzXGS1iFJkPF4AT')

# Legacy: sig in scriptSig
prev = Script(["OP_DUP","OP_HASH160", sk.get_public_key().get_address().to_hash160(), "OP_EQUALVERIFY","OP_CHECKSIG"])
tx_legacy = Transaction([TxInput('5e4a294028ea8cb0e156dac36f4444e2c445c7b393e87301b12818b06cee49e0', 0)],
    [TxOutput(to_satoshis(0.00000866), P2pkhAddress('myYHJtG3cyoRseuTwvViGHgP2efAvZkYa4').to_script_pub_key())])
sig = sk.sign_input(tx_legacy, 0, prev)
tx_legacy.inputs[0].script_sig = Script([sig, sk.get_public_key().to_hex()])

# SegWit: sig in witness
pk = sk.get_public_key()
script_code = pk.get_address().to_script_pub_key()
txin = TxInput('1454438e6f417d710333fbab118058e2972127bdd790134ab74937fa9dddbc48', 0)
txout = TxOutput(to_satoshis(0.00000666), P2wpkhAddress('tb1qckeg66a6jx3xjw5mrpmte5ujjv3cjrajtvm9r4').to_script_pub_key())
tx_sw = Transaction([txin], [txout], has_segwit=True)
sig_sw = sk.sign_segwit_input(tx_sw, 0, script_code, to_satoshis(0.00001))
txin.script_sig = Script([])
tx_sw.witnesses.append(TxWitnessInput([sig_sw, pk.to_hex()]))

print("Legacy scriptSig contains signature; SegWit witness contains signature, scriptSig empty")

# Example 2: SegWit transaction setup
# Reference: code/chapter04/02_create_segwit_transaction.py

sk = PrivateKey('cPeon9fBsW2BxwJTALj3hGzh9vm8C52Uqsce7MzXGS1iFJkPF4AT')
pk = sk.get_public_key()
script_code = pk.get_address().to_script_pub_key()
to_addr = P2wpkhAddress('tb1qckeg66a6jx3xjw5mrpmte5ujjv3cjrajtvm9r4')

utxo_txid = '1454438e6f417d710333fbab118058e2972127bdd790134ab74937fa9dddbc48'
txin = TxInput(utxo_txid, 0)
txout = TxOutput(to_satoshis(0.00000666), to_addr.to_script_pub_key())
tx = Transaction([txin], [txout], has_segwit=True)
print(f"From: {to_addr.to_string()}\nTo:   {to_addr.to_string()}")