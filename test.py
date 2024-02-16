# Importa la libreria web3 e il modulo time
from web3 import Web3
import time

# Crea un oggetto web3 con il provider HTTP dell'RPC di ethereum
w3 = Web3(Web3.HTTPProvider('https://eth1.lava.build/lava-referer-cb6f2521-d467-40d9-a3a6-091bc7783813/'))

# Definisci una funzione che calcola le fee medie o mediane per diversi percentili di priorità
def get_fee_estimates():
    # Ottieni la storia delle fee per gli ultimi 20 blocchi, inclusi il blocco corrente e il blocco in attesa
    fee_history = w3.eth.fee_history(20, 'pending', [10, 25, 50, 75, 90])
    # Estrai i valori di baseFeePerGas e priorityFeePerGas per ogni blocco
    base_fees = fee_history.baseFeePerGas
    priority_fees = fee_history.reward
    # Calcola le fee medie o mediane per ogni percentile di priorità
    fee_estimates = {}
    for i, percentile in enumerate([10, 25, 50, 75, 90]):
        # Usa la media aritmetica per il blocco in attesa e la mediana per gli altri blocchi
        if i == 0:
            fee_estimates[percentile] = int(sum(priority_fees[i]) / len(priority_fees[i]))
        else:
            fee_estimates[percentile] = int(sorted(priority_fees[i])[len(priority_fees[i]) // 2])
    # Aggiungi il valore di baseFeePerGas per il blocco in attesa
    fee_estimates['base'] = base_fees[-1]
    # Restituisci le fee stimate
    return fee_estimates

# Definisci una funzione che stampa le fee stimate in un formato leggibile
def print_fee_estimates():
    # Ottieni le fee stimate
    fee_estimates = get_fee_estimates()
    # Stampa il valore di baseFeePerGas per il blocco in attesa
    print(f"Base fee per gas for pending block: {fee_estimates['base']} wei")
    # Stampa le fee medie o mediane per ogni percentile di priorità
    for percentile in [10, 25, 50, 75, 90]:
        print(f"Priority fee per gas for {percentile}th percentile: {fee_estimates[percentile]} wei")
        print(f"Total fee per gas for {percentile}th percentile: {fee_estimates['base'] + fee_estimates[percentile]} wei")
    # Stampa una riga vuota per separare le fee successive
    print()

# Esegui un ciclo infinito che stampa le fee stimate ogni 5 secondi
while True:
    print_fee_estimates()
    time.sleep(5)
