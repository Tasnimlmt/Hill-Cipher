import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import string
from collections import Counter
import math

class HillCipherHologram:
    def __init__(self, root):
        self.root = root
        self.root.title("🌀 HOLOGRAPHIC HILL CIPHER CRYPTOSYSTEM v1.0 🌀")
        self.root.geometry("1400x950")
        self.root.configure(bg='#0a0010')  # Deep purple/black
        
        # Matrix size
        self.matrix_size = tk.IntVar(value=2)
        
        # Initialize attributes that will be created in UI
        self.matrix_entries = []
        self.matrix_grid = None
        self.validation_label = None
        self.status_label = None
        self.input_text = None
        self.output_text = None
        self.pairs_text = None
        self.attack_results = None
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container
        main_container = tk.Frame(self.root, bg='#0a0010')
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Top banner
        self.create_holographic_banner(main_container)
        
        # Notebook
        style = ttk.Style()
        style.theme_use('default')
        style.configure('Hologram.TNotebook', background='#0a0010', borderwidth=0)
        style.configure('Hologram.TNotebook.Tab', background='#1a0030', foreground='#ff00ff',
                       padding=[15, 8], font=('Orbitron', 10, 'bold'))
        style.map('Hologram.TNotebook.Tab',
                 background=[('selected', '#ff00ff'), ('active', '#2a0050')],
                 foreground=[('selected', '#0a0010'), ('active', '#ff00ff')])
        
        notebook = ttk.Notebook(main_container, style='Hologram.TNotebook')
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.tab1 = tk.Frame(notebook, bg='#0a0010')
        notebook.add(self.tab1, text="🌀 ENCRYPTION/DECRYPTION")
        self.setup_cipher_ops()
        
        self.tab2 = tk.Frame(notebook, bg='#0a0010')
        notebook.add(self.tab2, text="🔓 KNOWN-PLAINTEXT ATTACK")
        self.setup_known_plaintext()
        
        self.tab3 = tk.Frame(notebook, bg='#0a0010')
        notebook.add(self.tab3, text="⚡ SECURITY ANALYSIS")
        self.setup_security_analysis()
        
        # Status bar
        self.create_status_bar(main_container)
    
    def create_holographic_banner(self, parent):
        banner = tk.Frame(parent, bg='#0a0010', height=100)
        banner.pack(fill=tk.X, pady=(10, 0))
        
        banner_text = """
╔═══════════════════════════════════════════════════════════════════════════════════╗
║  ██╗  ██╗██╗██╗     ██╗     ██╗      ██████╗██████╗  █████╗ ██████╗ ██╗   ██╗     ║
║  ██║  ██║██║██║     ██║     ██║     ██╔════╝██╔══██╗██╔══██╗██╔══██╗╚██╗ ██╔╝     ║
║  ███████║██║██║     ██║     ██║     ██║     ██████╔╝███████║██████╔╝ ╚████╔╝      ║
║  ██╔══██║██║██║     ██║     ██║     ██║     ██╔══██╗██╔══██║██╔══██╗  ╚██╔╝       ║
║  ██║  ██║██║███████╗███████╗███████╗╚██████╗██║  ██║██║  ██║██║  ██║   ██║        ║
║  ╚═╝  ╚═╝╚═╝╚══════╝╚══════╝╚══════╝ ╚═════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝        ║
║                          HOLOGRAPHIC HILL CIPHER v1.0                               ║
╚═══════════════════════════════════════════════════════════════════════════════════╝
        """
        
        lbl = tk.Label(banner, text=banner_text, font=('Courier', 8), fg='#ff00ff',
                      bg='#0a0010', justify=tk.LEFT)
        lbl.pack()
    
    def create_status_bar(self, parent):
        status_frame = tk.Frame(parent, bg='#1a0030', height=30)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = tk.Label(status_frame, text="🟢 SYSTEM ONLINE | MATRIX SIZE: 2x2",
                                     font=('Consolas', 9), fg='#00ffff', bg='#1a0030')
        self.status_label.pack(side=tk.LEFT, padx=10)
        
        for i in range(3):
            dot = tk.Label(status_frame, text="●", font=('Consolas', 10), fg='#ff00ff', bg='#1a0030')
            dot.pack(side=tk.RIGHT, padx=5)
    
    # ==================== MATRIX OPERATIONS (Pure Python) ====================
    def text_to_numbers(self, text):
        """Convert text to numbers (A=0, B=1, ..., Z=25)"""
        text = ''.join([c.upper() for c in text if c.isalpha()])
        return [ord(c) - ord('A') for c in text]
    
    def numbers_to_text(self, numbers):
        """Convert numbers back to text"""
        return ''.join([chr((n % 26) + ord('A')) for n in numbers])
    
    def mod_inverse(self, a, m=26):
        """Calculate modular inverse using extended Euclidean algorithm"""
        a = a % m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        return None
    
    def determinant_2x2(self, matrix):
        """Calculate determinant of 2x2 matrix"""
        return (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % 26
    
    def determinant_3x3(self, matrix):
        """Calculate determinant of 3x3 matrix"""
        a, b, c = matrix[0]
        d, e, f = matrix[1]
        g, h, i = matrix[2]
        
        det = a * (e*i - f*h) - b * (d*i - f*g) + c * (d*h - e*g)
        return det % 26
    
    def adjugate_2x2(self, matrix):
        """Calculate adjugate of 2x2 matrix"""
        return [[matrix[1][1], -matrix[0][1]],
                [-matrix[1][0], matrix[0][0]]]
    
    def adjugate_3x3(self, matrix):
        """Calculate adjugate of 3x3 matrix"""
        a, b, c = matrix[0]
        d, e, f = matrix[1]
        g, h, i = matrix[2]
        
        adj = [
            [(e*i - f*h), -(b*i - c*h), (b*f - c*e)],
            [-(d*i - f*g), (a*i - c*g), -(a*f - c*d)],
            [(d*h - e*g), -(a*h - b*g), (a*e - b*d)]
        ]
        
        return adj
    
    def matrix_multiply(self, A, B):
        """Multiply two matrices"""
        size = len(A)
        result = [[0 for _ in range(size)] for _ in range(size)]
        
        for i in range(size):
            for j in range(size):
                total = 0
                for k in range(size):
                    total += A[i][k] * B[k][j]
                result[i][j] = total % 26
        return result
    
    def matrix_vector_multiply(self, matrix, vector):
        """Multiply matrix by vector"""
        size = len(matrix)
        result = []
        for i in range(size):
            total = 0
            for j in range(size):
                total += matrix[i][j] * vector[j]
            result.append(total % 26)
        return result
    
    def matrix_mod_inverse(self, matrix):
        """Calculate modular inverse of a matrix"""
        size = len(matrix)
        
        # Calculate determinant
        if size == 2:
            det = self.determinant_2x2(matrix)
            adj = self.adjugate_2x2(matrix)
        else:
            det = self.determinant_3x3(matrix)
            adj = self.adjugate_3x3(matrix)
        
        # Check if determinant is invertible
        det_inv = self.mod_inverse(det)
        if det_inv is None:
            return None
        
        # Multiply adjugate by determinant inverse
        for i in range(size):
            for j in range(size):
                adj[i][j] = (adj[i][j] * det_inv) % 26
        
        return adj
    
    def validate_matrix(self, matrix):
        """Validate if matrix is usable for Hill cipher"""
        size = len(matrix)
        if size == 2:
            det = self.determinant_2x2(matrix)
        else:
            det = self.determinant_3x3(matrix)
        return self.mod_inverse(det) is not None
    
    def hill_encrypt_block(self, block, key_matrix):
        """Encrypt a single block"""
        return self.matrix_vector_multiply(key_matrix, block)
    
    def hill_decrypt_block(self, block, key_matrix):
        """Decrypt a single block"""
        inv_key = self.matrix_mod_inverse(key_matrix)
        if inv_key is None:
            return None
        return self.matrix_vector_multiply(inv_key, block)
    
    def encrypt_hill(self, plaintext, key_matrix):
        """Encrypt full plaintext using Hill cipher"""
        numbers = self.text_to_numbers(plaintext)
        size = len(key_matrix)
        
        # Pad if necessary
        while len(numbers) % size != 0:
            numbers.append(23)  # 'X' as padding
        
        cipher_numbers = []
        for i in range(0, len(numbers), size):
            block = numbers[i:i+size]
            encrypted_block = self.hill_encrypt_block(block, key_matrix)
            cipher_numbers.extend(encrypted_block)
        
        return self.numbers_to_text(cipher_numbers)
    
    def decrypt_hill(self, ciphertext, key_matrix):
        """Decrypt full ciphertext using Hill cipher"""
        numbers = self.text_to_numbers(ciphertext)
        size = len(key_matrix)
        
        inv_key = self.matrix_mod_inverse(key_matrix)
        if inv_key is None:
            return None
        
        plain_numbers = []
        for i in range(0, len(numbers), size):
            block = numbers[i:i+size]
            decrypted_block = self.hill_decrypt_block(block, key_matrix)
            if decrypted_block is None:
                return None
            plain_numbers.extend(decrypted_block)
        
        return self.numbers_to_text(plain_numbers)
    
    # ==================== TAB 1: ENCRYPTION/DECRYPTION ====================
    def setup_cipher_ops(self):
        # Matrix size selector
        size_frame = tk.Frame(self.tab1, bg='#0a0010')
        size_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Label(size_frame, text="🌀 MATRIX DIMENSION:", font=('Orbitron', 11, 'bold'),
                fg='#ff00ff', bg='#0a0010').pack(side=tk.LEFT, padx=10)
        
        tk.Radiobutton(size_frame, text="2x2", variable=self.matrix_size, value=2,
                      command=self.update_matrix_input, bg='#0a0010', fg='#00ffff',
                      selectcolor='#0a0010', activebackground='#0a0010').pack(side=tk.LEFT, padx=10)
        
        tk.Radiobutton(size_frame, text="3x3", variable=self.matrix_size, value=3,
                      command=self.update_matrix_input, bg='#0a0010', fg='#00ffff',
                      selectcolor='#0a0010', activebackground='#0a0010').pack(side=tk.LEFT, padx=10)
        
        # Main content frame
        content_frame = tk.Frame(self.tab1, bg='#0a0010')
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # Left panel - Input
        left_panel = tk.Frame(content_frame, bg='#0a0010')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Matrix input
        matrix_frame = tk.LabelFrame(left_panel, text="🔑 KEY MATRIX (mod 26)", 
                                     font=('Orbitron', 10, 'bold'),
                                     fg='#ff00ff', bg='#0a0010', relief=tk.GROOVE, bd=2)
        matrix_frame.pack(fill=tk.X, pady=10)
        
        self.matrix_entries = []
        self.matrix_grid = tk.Frame(matrix_frame, bg='#0a0010')
        self.matrix_grid.pack(pady=10)
        
        # Create validation label AFTER matrix_grid
        self.validation_label = tk.Label(matrix_frame, text="⚡ Status: Validating...", 
                                        font=('Consolas', 9), fg='#ffff00', bg='#0a0010')
        self.validation_label.pack(pady=5)
        
        # Now update matrix input (this will use validation_label)
        self.update_matrix_input()
        
        # Text input
        text_frame = tk.LabelFrame(left_panel, text="📝 MESSAGE INPUT", 
                                   font=('Orbitron', 10, 'bold'),
                                   fg='#ff00ff', bg='#0a0010', relief=tk.GROOVE, bd=2)
        text_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.input_text = scrolledtext.ScrolledText(text_frame, height=8, font=('Consolas', 11),
                                                    bg='#1a0030', fg='#00ffff', insertbackground='#ff00ff')
        self.input_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.input_text.insert('1.0', "HELLO HILL CIPHER")
        
        # Buttons
        btn_frame = tk.Frame(left_panel, bg='#0a0010')
        btn_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(btn_frame, text="🌀 ENCRYPT", command=self.do_encrypt,
                 font=('Orbitron', 10, 'bold'), bg='#ff00ff', fg='#0a0010',
                 activebackground='#cc00cc', activeforeground='#0a0010',
                 relief=tk.RAISED, bd=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🔓 DECRYPT", command=self.do_decrypt,
                 font=('Orbitron', 10, 'bold'), bg='#00ffff', fg='#0a0010',
                 activebackground='#00cccc', activeforeground='#0a0010',
                 relief=tk.RAISED, bd=2).pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_frame, text="🗑️ CLEAR", command=self.clear_hill_output,
                 font=('Orbitron', 10, 'bold'), bg='#ff4444', fg='#0a0010',
                 activebackground='#cc0000', activeforeground='#0a0010',
                 relief=tk.RAISED, bd=2).pack(side=tk.LEFT, padx=5)
        
        # Right panel - Output
        right_panel = tk.Frame(content_frame, bg='#0a0010')
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        output_frame = tk.LabelFrame(right_panel, text="📤 RESULT", 
                                     font=('Orbitron', 10, 'bold'),
                                     fg='#ff00ff', bg='#0a0010', relief=tk.GROOVE, bd=2)
        output_frame.pack(fill=tk.BOTH, expand=True)
        
        self.output_text = scrolledtext.ScrolledText(output_frame, height=20, font=('Consolas', 11),
                                                     bg='#1a0030', fg='#00ffff')
        self.output_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def update_matrix_input(self):
        """Update matrix input grid based on selected size"""
        # Clear existing entries
        for widget in self.matrix_grid.winfo_children():
            widget.destroy()
        
        size = self.matrix_size.get()
        self.matrix_entries = []
        
        # Create title
        tk.Label(self.matrix_grid, text=" ", font=('Courier', 10), fg='#ff00ff', bg='#0a0010').grid(row=0, column=0)
        for j in range(size):
            tk.Label(self.matrix_grid, text=f"c{j+1}", font=('Courier', 10, 'bold'),
                    fg='#ff00ff', bg='#0a0010').grid(row=0, column=j+1)
        
        # Create entry grid
        for i in range(size):
            tk.Label(self.matrix_grid, text=f"r{i+1}", font=('Courier', 10, 'bold'),
                    fg='#ff00ff', bg='#0a0010').grid(row=i+1, column=0)
            
            row_entries = []
            for j in range(size):
                entry = tk.Entry(self.matrix_grid, width=5, font=('Consolas', 10),
                                bg='#1a0030', fg='#00ffff', insertbackground='#ff00ff',
                                justify='center')
                entry.grid(row=i+1, column=j+1, padx=2, pady=2)
                row_entries.append(entry)
            self.matrix_entries.append(row_entries)
        
        # Set default matrix values
        if size == 2:
            default_matrix = [[3, 3], [2, 5]]
        else:
            default_matrix = [[2, 4, 5], [1, 3, 6], [4, 2, 7]]
        
        for i in range(size):
            for j in range(size):
                self.matrix_entries[i][j].insert(0, str(default_matrix[i][j]))
        
        self.validate_matrix_input()
    
    def validate_matrix_input(self):
        """Validate the current matrix"""
        try:
            size = self.matrix_size.get()
            matrix = []
            for i in range(size):
                row = []
                for j in range(size):
                    val = int(self.matrix_entries[i][j].get())
                    row.append(val)
                matrix.append(row)
            
            if self.validate_matrix(matrix):
                self.validation_label.config(text="✅ VALID MATRIX (det invertible mod 26)", fg='#00ff00')
                self.status_label.config(text=f"🟢 SYSTEM ONLINE | MATRIX SIZE: {size}x{size} | VALID")
                return True
            else:
                self.validation_label.config(text="❌ INVALID MATRIX (det not invertible mod 26)", fg='#ff0000')
                self.status_label.config(text=f"🔴 INVALID MATRIX | SIZE: {size}x{size}")
                return False
        except Exception as e:
            self.validation_label.config(text="⚠️ Invalid matrix values", fg='#ffff00')
            return False
    
    def get_matrix(self):
        """Get current matrix as 2D list"""
        size = self.matrix_size.get()
        matrix = []
        for i in range(size):
            row = []
            for j in range(size):
                row.append(int(self.matrix_entries[i][j].get()))
            matrix.append(row)
        return matrix
    
    def do_encrypt(self):
        if not self.validate_matrix_input():
            messagebox.showerror("Error", "Invalid key matrix!")
            return
        
        text = self.input_text.get('1.0', tk.END).strip()
        if not text:
            messagebox.showerror("Error", "Please enter text to encrypt!")
            return
        
        matrix = self.get_matrix()
        result = self.encrypt_hill(text, matrix)
        
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert('1.0', "╔════════════════════════════════════════╗\n")
        self.output_text.insert(tk.END, "║        HILL CIPHER ENCRYPTION          ║\n")
        self.output_text.insert(tk.END, "╚════════════════════════════════════════╝\n\n")
        self.output_text.insert(tk.END, f"Original: {text}\n")
        self.output_text.insert(tk.END, f"Matrix: {matrix}\n\n")
        self.output_text.insert(tk.END, f"Ciphertext: {result}\n")
    
    def do_decrypt(self):
        if not self.validate_matrix_input():
            messagebox.showerror("Error", "Invalid key matrix!")
            return
        
        text = self.input_text.get('1.0', tk.END).strip()
        if not text:
            messagebox.showerror("Error", "Please enter text to decrypt!")
            return
        
        matrix = self.get_matrix()
        result = self.decrypt_hill(text, matrix)
        
        if result is None:
            messagebox.showerror("Error", "Decryption failed! Matrix not invertible.")
            return
        
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert('1.0', "╔════════════════════════════════════════╗\n")
        self.output_text.insert(tk.END, "║        HILL CIPHER DECRYPTION          ║\n")
        self.output_text.insert(tk.END, "╚════════════════════════════════════════╝\n\n")
        self.output_text.insert(tk.END, f"Ciphertext: {text}\n")
        self.output_text.insert(tk.END, f"Matrix: {matrix}\n\n")
        self.output_text.insert(tk.END, f"Plaintext: {result}\n")
    
    def clear_hill_output(self):
        self.output_text.delete('1.0', tk.END)
    
    # ==================== TAB 2: KNOWN-PLAINTEXT ATTACK ====================
    def setup_known_plaintext(self):
        main_frame = tk.Frame(self.tab2, bg='#0a0010')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Attack description
        desc_frame = tk.LabelFrame(main_frame, text="⚡ KNOWN-PLAINTEXT ATTACK SIMULATOR", 
                                   font=('Orbitron', 10, 'bold'),
                                   fg='#ff00ff', bg='#0a0010', relief=tk.GROOVE, bd=2)
        desc_frame.pack(fill=tk.X, pady=10)
        
        desc_text = """HOW IT WORKS:
        • If we know n² pairs of (plaintext, ciphertext) blocks, we can recover the key matrix
        • For 2x2: Need 2 known pairs (4 letters plaintext, 4 letters ciphertext)
        • For 3x3: Need 3 known pairs (9 letters each)
        • The attack solves: C = K * P mod 26 → K = C * P⁻¹ mod 26
        """
        
        desc_lbl = tk.Label(desc_frame, text=desc_text, font=('Consolas', 10),
                           fg='#00ffff', bg='#0a0010', justify=tk.LEFT)
        desc_lbl.pack(padx=10, pady=10)
        
        # Known pairs input
        pairs_frame = tk.LabelFrame(main_frame, text="📊 KNOWN PLAINTEXT-CIPHERTEXT PAIRS", 
                                    font=('Orbitron', 10, 'bold'),
                                    fg='#ff00ff', bg='#0a0010', relief=tk.GROOVE, bd=2)
        pairs_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.pairs_text = scrolledtext.ScrolledText(pairs_frame, height=8, font=('Consolas', 11),
                                                    bg='#1a0030', fg='#00ffff')
        self.pairs_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.pairs_text.insert('1.0', """Example for 2x2:
Plaintext:  HILL      -> Ciphertext:  AERB
Plaintext:  CIPHER    -> Ciphertext:  SXFY

(Each plaintext/ciphertext must be multiple of matrix size)""")
        
        # Attack button
        tk.Button(main_frame, text="🔓 LAUNCH KNOWN-PLAINTEXT ATTACK", command=self.known_plaintext_attack,
                 font=('Orbitron', 11, 'bold'), bg='#ff00ff', fg='#0a0010',
                 activebackground='#cc00cc', activeforeground='#0a0010',
                 relief=tk.RAISED, bd=2).pack(pady=10)
        
        # Results
        results_frame = tk.LabelFrame(main_frame, text="🎯 ATTACK RESULTS", 
                                      font=('Orbitron', 10, 'bold'),
                                      fg='#ff00ff', bg='#0a0010', relief=tk.GROOVE, bd=2)
        results_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.attack_results = scrolledtext.ScrolledText(results_frame, height=15, font=('Consolas', 10),
                                                        bg='#1a0030', fg='#00ffff')
        self.attack_results.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    def matrix_inverse_2x2(self, matrix):
        """Calculate inverse of 2x2 matrix modulo 26"""
        det = (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % 26
        det_inv = self.mod_inverse(det)
        
        if det_inv is None:
            return None
        
        inv = [
            [(matrix[1][1] * det_inv) % 26, ((-matrix[0][1]) * det_inv) % 26],
            [((-matrix[1][0]) * det_inv) % 26, (matrix[0][0] * det_inv) % 26]
        ]
        return inv
    
    def matrix_multiply_2x2(self, A, B):
        """Multiply 2x2 matrices"""
        result = [[0, 0], [0, 0]]
        for i in range(2):
            for j in range(2):
                for k in range(2):
                    result[i][j] += A[i][k] * B[k][j]
                result[i][j] %= 26
        return result
    
    def known_plaintext_attack(self):
        """Perform known-plaintext attack to recover key matrix"""
        text = self.pairs_text.get('1.0', tk.END).strip()
        self.attack_results.delete('1.0', tk.END)
        
        # Parse input
        lines = text.strip().split('\n')
        plaintexts = []
        ciphertexts = []
        
        for line in lines:
            if 'Plaintext:' in line and 'Ciphertext:' in line:
                parts = line.split('->')
                plain_part = parts[0].split('Plaintext:')[1].strip()
                cipher_part = parts[1].split('Ciphertext:')[1].strip()
                plaintexts.append(plain_part.upper())
                ciphertexts.append(cipher_part.upper())
        
        if len(plaintexts) < 2:
            self.attack_results.insert(tk.END, "⚠️ Need at least 2 plaintext-ciphertext pairs for 2x2 attack!\n")
            return
        
        # Check if it's 2x2
        block_size = len(plaintexts[0])
        
        if block_size == 2:
            # Build matrices P and C
            P = [[self.text_to_numbers(plaintexts[0])[0], self.text_to_numbers(plaintexts[1])[0]],
                 [self.text_to_numbers(plaintexts[0])[1], self.text_to_numbers(plaintexts[1])[1]]]
            
            C = [[self.text_to_numbers(ciphertexts[0])[0], self.text_to_numbers(ciphertexts[1])[0]],
                 [self.text_to_numbers(ciphertexts[0])[1], self.text_to_numbers(ciphertexts[1])[1]]]
            
            # Calculate P inverse
            P_inv = self.matrix_inverse_2x2(P)
            if P_inv is None:
                self.attack_results.insert(tk.END, "❌ Attack failed! P matrix not invertible modulo 26.\n")
                return
            
            # Recover key: K = C * P^(-1)
            K = self.matrix_multiply_2x2(C, P_inv)
            
            self.attack_results.insert(tk.END, "╔══════════════════════════════════════════════════╗\n")
            self.attack_results.insert(tk.END, "║         KEY RECOVERY SUCCESSFUL! 🎯              ║\n")
            self.attack_results.insert(tk.END, "╚══════════════════════════════════════════════════╝\n\n")
            self.attack_results.insert(tk.END, f"Recovered Key Matrix (2x2):\n")
            self.attack_results.insert(tk.END, f"[{K[0][0]:2d} {K[0][1]:2d}]\n")
            self.attack_results.insert(tk.END, f"[{K[1][0]:2d} {K[1][1]:2d}]\n\n")
            
            # Test the recovered key
            test_plain = self.text_to_numbers(plaintexts[0])
            test_result = self.hill_encrypt_block(test_plain, K)
            test_text = self.numbers_to_text(test_result)
            
            self.attack_results.insert(tk.END, f"Verification:\n")
            self.attack_results.insert(tk.END, f"  Known plaintext: {plaintexts[0]}\n")
            self.attack_results.insert(tk.END, f"  Known ciphertext: {ciphertexts[0]}\n")
            self.attack_results.insert(tk.END, f"  Encrypted with recovered key: {test_text}\n")
            
            if test_text == ciphertexts[0]:
                self.attack_results.insert(tk.END, "\n✅ VERIFICATION SUCCESSFUL! Key is correct.\n")
            else:
                self.attack_results.insert(tk.END, "\n⚠️ Verification failed. Check input format.\n")
                
        else:
            self.attack_results.insert(tk.END, "⚠️ Only 2x2 attack implemented in this version.\n")
            self.attack_results.insert(tk.END, "For 3x3, please use the provided example.\n")
    
    # ==================== TAB 3: SECURITY ANALYSIS ====================
    def setup_security_analysis(self):
        text_frame = tk.Frame(self.tab3, bg='#0a0010')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        security_text = scrolledtext.ScrolledText(text_frame, height=35, font=('Consolas', 10),
                                                  bg='#1a0030', fg='#00ffff')
        security_text.pack(fill=tk.BOTH, expand=True)
        
        security_content = """
╔══════════════════════════════════════════════════════════════════════════════════════════╗
║                    🔓 HILL CIPHER SECURITY ANALYSIS - KNOWN-PLAINTEXT ATTACK 🔓          ║
╚══════════════════════════════════════════════════════════════════════════════════════════╝

📌 QUESTION: Why is Hill cipher vulnerable to known-plaintext attack even for large matrices?
═══════════════════════════════════════════════════════════════════════════════════════════

THEORETICAL EXPLANATION:
───────────────────────────────────────────────────────────────────────────────────────────

1. LINEAR NATURE OF THE CIPHER:
   • Hill cipher is fundamentally a LINEAR transformation
   • Encryption: C = (K × P) mod 26
   • This is a system of linear equations in modular arithmetic
   • Linear systems are SOLVABLE with enough equations

2. MATHEMATICAL VULNERABILITY:
   • For an n×n matrix, we have n² unknown key elements
   • Each known plaintext-ciphertext block gives n equations
   • With n blocks (n² letters total), we have n² equations
   • This creates a uniquely solvable system!

3. REQUIRED KNOWLEDGE FOR ATTACK:
   • Need n² known pairs (plaintext, ciphertext) letters
   • For 2×2: Need 4 letter pairs → 2 blocks
   • For 3×3: Need 9 letter pairs → 3 blocks
   • For 10×10: Need 100 letter pairs → 10 blocks

WHY MATRIX SIZE DOESN'T HELP:
═══════════════════════════════════════════════════════════════════════════════════════════

Matrix Size     Unknowns (n²)    Blocks Needed    Attack Complexity
─────────────────────────────────────────────────────────────────
2×2             4                2                Trivial
3×3             9                3                Easy
5×5             25               5                Moderate
10×10           100              10               Feasible
26×26           676              26               Possible

KEY INSIGHT:
───────────────────────────────────────────────────────────────────────────────────────────
• The attack complexity grows POLYNOMIALLY (O(n³)), not exponentially!
• Even for n=26, only need 26 known blocks (676 letters)
• Modern computers can solve 676×676 linear systems instantly
• Size only adds LINEAR difficulty, not exponential security!

CONCLUSION:
───────────────────────────────────────────────────────────────────────────────────────────
• Hill cipher's LINEARITY is its fundamental weakness
• Larger matrices only multiply, not exponentiate, attack complexity
• Known-plaintext attack is ALWAYS possible with sufficient known pairs
• Hill cipher is UNSAFE for any serious cryptographic application
• Educational value only - demonstrates importance of non-linearity!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
                      🌀 HILL CIPHER CRYPTANALYSIS COMPLETE 🌀
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        security_text.insert('1.0', security_content)
        security_text.config(state='disabled')

def main():
    root = tk.Tk()
    app = HillCipherHologram(root)
    root.mainloop()

if __name__ == "__main__":
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║     HOLOGRAPHIC HILL CIPHER SYSTEM - INITIALIZING...        ║
    ║                                                              ║
    ║     Features:                                                ║
    ║     ✓ 2x2 and 3x3 matrix support                            ║
    ║     ✓ Modular matrix inversion (mod 26)                     ║
    ║     ✓ Known-plaintext attack simulation                     ║
    ║     ✓ Security analysis with mathematical proof             ║
    ║                                                              ║
    ║     Starting GUI...                                         ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    main()