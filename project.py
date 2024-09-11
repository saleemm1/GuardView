import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from web3 import Web3
import subprocess
import json

e
AVALANCHE_RPC = "https://subnets.avax.network/pearl/testnet/rpc"
INTERSECT_RPC = "https://subnets.avax.network/pearl/testnet/rpc"


w3_intersect = Web3(Web3.HTTPProvider(INTERSECT_RPC))
w3_avalanche = Web3(Web3.HTTPProvider(AVALANCHE_RPC))


def check_network():
    if w3_intersect.is_connected() and w3_avalanche.is_connected():
        print("Connected to Intersect and Avalanche networks")
    else:
        print("Failed to connect to Intersect or Avalanche networks")

check_network()


root = tk.Tk()
root.title("GuardView - Cross-Chain Security Auditor")
root.geometry("1000x700")
root.configure(bg="#f5f5f5")


title_label = tk.Label(root, text="GuardView - Cross-Chain Security Auditor", font=("Arial", 18, "bold"), bg="#f5f5f5",
                       fg="#333")
title_label.pack(pady=20)


input_frame = tk.Frame(root, bg="#f5f5f5")
input_frame.pack(pady=10)

input_label = tk.Label(input_frame, text="Enter Smart Contract Code:", font=("Arial", 12), bg="#f5f5f5")
input_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

contract_input = scrolledtext.ScrolledText(input_frame, wrap=tk.WORD, width=80, height=15, font=("Arial", 10))
contract_input.grid(row=1, column=0, padx=10, pady=10)


analyze_button = tk.Button(root, text="Analyze Contract", font=("Arial", 12, "bold"), bg="#4CAF50", fg="#fff", width=20,
                           command=lambda: analyze_contract())
analyze_button.pack(pady=20)


results_frame = tk.Frame(root, bg="#f5f5f5")
results_frame.pack(pady=10)

results_label = tk.Label(results_frame, text="Analysis Results:", font=("Arial", 12), bg="#f5f5f5")
results_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

results_output = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD, width=80, height=15, font=("Arial", 10))
results_output.grid(row=1, column=0, padx=10, pady=10)


def analyze_contract():
    contract_code = contract_input.get("1.0", tk.END).strip()

    if not contract_code:
        messagebox.showwarning("Input Error", "Please enter the smart contract code to analyze.")
        return

    results_output.delete("1.0", tk.END)
    results_output.insert(tk.END, "Analyzing contract...\n")


   
    with open("temp_contract.sol", "w") as f:
        f.write(contract_code)

   
    slither_command = "slither temp_contract.sol"
    try:
        slither_results = subprocess.check_output(slither_command, shell=True).decode()
        results_output.insert(tk.END, "\n[Slither Analysis Results]\n" + slither_results)
    except subprocess.CalledProcessError as e:
        results_output.insert(tk.END, "\n[Error] Failed to analyze with Slither.\n" + str(e.output.decode()))

   
    mythril_command = "myth analyze temp_contract.sol --solv 0.8.18"
    try:
        mythril_results = subprocess.check_output(mythril_command, shell=True).decode()
        results_output.insert(tk.END, "\n[Mythril Analysis Results]\n" + mythril_results)
    except subprocess.CalledProcessError as e:
        results_output.insert(tk.END, "\n[Error] Failed to analyze with Mythril.\n" + str(e.output.decode()))

   
    subprocess.run("rm temp_contract.sol", shell=True)


def show_usage():
    usage_text = "1. Paste your smart contract code in the input area.\n"
    usage_text += "2. Click 'Analyze Contract' to analyze the code for vulnerabilities.\n"
    usage_text += "3. View the results in the results area."
    messagebox.showinfo("How to Use", usage_text)

usage_button = tk.Button(root, text="How to Use", font=("Arial", 10), bg="#2196F3", fg="#fff", command=show_usage)
usage_button.pack(side=tk.TOP, anchor="ne", padx=10, pady=10)


root.mainloop()
