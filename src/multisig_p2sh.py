from bitcoinutils.setup import setup
from bitcoinutils.keys import PrivateKey, P2shAddress
from bitcoinutils.script import Script
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, SIGHASH_ALL
from bitcoinutils.utils import to_satoshis

def setup_multisig():
    """Генерирует ключи и создает P2SH адрес"""
    setup('testnet')

    # 1. Генерируем приватные ключи (в реальности они должны храниться в секрете!)
    alice_sk = PrivateKey()
    bob_sk = PrivateKey()
    carol_sk = PrivateKey()

    # 2. Получаем соответствующие публичные ключи
    alice_pk = alice_sk.get_public_key().to_hex()
    bob_pk = bob_sk.get_public_key().to_hex()
    carol_pk = carol_sk.get_public_key().to_hex()

    print(f"Alice PK: {alice_pk}")
    print(f"Bob PK:   {bob_pk}")
    print(f"Carol PK: {carol_pk}")

    # 3. Создаем Multisig 2-of-3 Redeem Script
    redeem_script = Script([
        'OP_2',        # Нужно 2 подписи
        alice_pk,      # Ключ Alice
        bob_pk,        # Ключ Bob
        carol_pk,      # Ключ Carol
        'OP_3',        # Всего 3 ключа
        'OP_CHECKMULTISIG'
    ])

    # 4. Генерируем P2SH адрес
    p2sh_addr = P2shAddress.from_script(redeem_script)
    print(f"P2SH Address: {p2sh_addr.to_string()}")

    return alice_sk, bob_sk, redeem_script, p2sh_addr

def spend_multisig_p2sh(alice_sk, bob_sk, redeem_script, recipient_address):
    """Создает и подписывает транзакцию"""
    
    # ⚠️ ВНИМАНИЕ: Этот TXID должен реально существовать в Testnet!
    # Вам нужно получить тестовые биткоины на адрес multisig, а затем взять ID транзакции
    utxo_txid = '4b869865bc4a156d7e0ba14590b5c8971e57b8198af64d88872558ca88a8ba5f'
    utxo_vout = 0
    utxo_amount = 0.00001600  # 1,600 сатоши

    # Создаем выходы и входы
    txout = TxOutput(to_satoshis(0.00000888), recipient_address.to_script_pub_key())
    txin = TxInput(utxo_txid, utxo_vout)
    
    # Создаем транзакцию
    tx = Transaction([txin], [txout])

    # 5. Подписываем вход приватными ключами (Alice + Bob)
    # sign_input требует доступ к приватному ключу
    alice_sig = alice_sk.sign_input(tx, 0, redeem_script)
    bob_sig = bob_sk.sign_input(tx, 0, redeem_script)

    # 6. Создаем ScriptSig для разблокировки UTXO
    txin.script_sig = Script([
        'OP_0',              # Баг OP_CHECKMULTISIG (требуется пустой элемент)
        alice_sig,           # Подпись Alice
        bob_sig,             # Подпись Bob
        redeem_script.to_hex()  # Сам скрипт (Redeem Script)
    ])

    return tx

if __name__ == "__main__":
    # Инициализация
    alice_sk, bob_sk, redeem_script, p2sh_addr = setup_multisig()
    
    # Получатель (можно создать новый адрес)
    recipient_sk = PrivateKey()
    recipient_addr = recipient_sk.get_public_key().get_address()
    
    # Подписание транзакции
    tx = spend_multisig_p2sh(alice_sk, bob_sk, redeem_script, recipient_addr)
    
    print("\n=== Signed Transaction ===")
    print(tx.to_hex())

