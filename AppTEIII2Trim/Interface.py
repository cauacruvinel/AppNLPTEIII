import json
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from AnalisadorNLP import AnalisadorNLP


class Interface:
    """Interface gráfica para operações NLP."""

    def __init__(self):
        self.analyser = AnalisadorNLP()
        self.homepage = None
        self._widgets = {}

    def _set_status(self, text: str):
        self._widgets["status"].configure(text=text)

    def _input_text(self) -> str:
        return self._widgets["textbox"].get("1.0", "end").strip()

    def clean_text(self):
        self._widgets["textbox"].delete("1.0", "end")
        self._widgets["compare_text"].delete("1.0", "end")
        self._widgets["result_global"].configure(state="normal")
        self._widgets["result_global"].delete("1.0", "end")
        self._widgets["result_global"].configure(state="disabled")
        self._set_status("Texto limpo.")

    def clean_url(self):
        self._widgets["text_url"].delete(0, "end")

    def upload_file(self):
        self._set_status("📂 Abrindo seletor de arquivo...")
        file_path = filedialog.askopenfilename(
            title="Selecione um Arquivo",
            filetypes=[("Texto", "*.txt"), ("Todos os arquivos", "*.*")],
        )
        if not file_path:
            self._set_status("Operação cancelada.")
            return
        try:
            file_text = self.analyser.open_file(file_path)
            self._widgets["textbox"].delete("1.0", "end")
            self._widgets["textbox"].insert("1.0", file_text)
            self._set_status("Arquivo carregado com sucesso.")
        except Exception as exc:
            messagebox.showwarning("Erro", f"Erro ao abrir o arquivo: {exc}")

    def load_url(self):
        try:
            url = self._widgets["text_url"].get()
            text = self.analyser.search_url(url)
            self._widgets["textbox"].delete("1.0", "end")
            self._widgets["textbox"].insert("1.0", text)
            self._set_status("Conteúdo da URL carregado.")
        except Exception as exc:
            messagebox.showwarning("Erro", f"Falha ao buscar URL: {exc}")

    def _render_tab(self, key: str, payload):
        box = self._widgets[key]
        box.configure(state="normal")
        box.delete("1.0", "end")
        box.insert("1.0", json.dumps(payload, indent=2, ensure_ascii=False))
        box.configure(state="disabled")

    def _run_block_a(self):
        try:
            self._render_tab("result_a", self.analyser.analyze_block_a(self._input_text()))
            self._set_status("Bloco A finalizado.")
        except Exception as exc:
            messagebox.showwarning("Validação", str(exc))

    def _run_block_b(self):
        try:
            self._render_tab("result_b", self.analyser.analyze_block_b(self._input_text()))
            self._set_status("Bloco B finalizado.")
        except Exception as exc:
            messagebox.showwarning("Validação", str(exc))

    def _run_block_c(self):
        try:
            self._render_tab("result_c", self.analyser.analyze_block_c(self._input_text()))
            self._set_status("Bloco C finalizado.")
        except Exception as exc:
            messagebox.showwarning("Validação", str(exc))

    def _run_block_d(self):
        try:
            payload = self.analyser.analyze_block_d(
                self._input_text(),
                word_for_wordnet=self._widgets["wordnet_word"].get(),
                n_value=self._widgets["ngram_n"].get(),
                top_n=self._widgets["top_n"].get(),
            )
            self._render_tab("result_d", payload)
            self._set_status("Bloco D finalizado.")
        except Exception as exc:
            messagebox.showwarning("Validação", str(exc))

    def _run_block_e(self):
        try:
            payload = self.analyser.analyze_block_e(
                self._input_text(),
                self._widgets["compare_text"].get("1.0", "end").strip(),
            )
            self._render_tab("result_e", payload)
            self._set_status("Bloco E finalizado.")
        except Exception as exc:
            messagebox.showwarning("Validação", str(exc))

    def analyse_all(self):
        try:
            payload = self.analyser.analyse_text(
                self._input_text(),
                comparison_text=self._widgets["compare_text"].get("1.0", "end").strip(),
                word_for_wordnet=self._widgets["wordnet_word"].get(),
            )
            self._render_tab("result_global", payload)
            self._set_status("Análise completa finalizada.")
        except Exception as exc:
            messagebox.showwarning("Validação", str(exc))

    def open_homepage(self):
        self.homepage = tk.Tk()
        self.homepage.title("Analisador de texto NLP - TextBlob + spaCy + NLTK")
        self.homepage.geometry("1180x760")
        self.homepage.minsize(900, 650)

        self.homepage.grid_columnconfigure(0, weight=0)
        self.homepage.grid_columnconfigure(1, weight=1)
        self.homepage.grid_rowconfigure(0, weight=1)

        self._build_sidebar()
        self._build_main()
        self.homepage.mainloop()

    def _build_sidebar(self):
        sidebar = ttk.Frame(self.homepage, width=220)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(10, weight=1)

        ttk.Label(
            sidebar,
            text="⚙ NLP por Blocos",
            font=("Arial", 16, "bold"),
            anchor="w"
        ).grid(row=0, column=0, padx=16, pady=(20, 10), sticky="ew")

        buttons = [
            ("▶ Executar Tudo", self.analyse_all),
            ("A - TextBlob", self._run_block_a),
            ("B - Sentimento", self._run_block_b),
            ("C - Palavras", self._run_block_c),
            ("D - Léxico", self._run_block_d),
            ("E - spaCy", self._run_block_e),
            ("📂 Carregar Arquivo", self.upload_file),
            ("🗑 Limpar Texto", self.clean_text),
        ]
        for index, (label, callback) in enumerate(buttons, start=1):
            ttk.Button(
                sidebar,
                text=label,
                command=callback
            ).grid(row=index, column=0, padx=12, pady=6, sticky="ew")

    def _build_main(self):
        main = ttk.Frame(self.homepage)
        main.grid(row=0, column=1, sticky="nsew", padx=16, pady=16)
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(7, weight=1)

        ttk.Label(main, text="Texto de Entrada", font=("Arial", 14, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w"
        )

        textbox = tk.Text(main, font=("Arial", 13), wrap="word")
        textbox.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(4, 8))
        self._widgets["textbox"] = textbox

        ttk.Label(main, text="URL para coleta").grid(row=2, column=0, columnspan=2, sticky="w")

        self._widgets["text_url"] = ttk.Entry(main, font=("Arial", 12))
        self._widgets["text_url"].grid(row=3, column=0, sticky="ew", pady=(4, 6))

        ttk.Button(main, text="🌐 Buscar URL", command=self.load_url).grid(
            row=3, column=1, sticky="ew", padx=(8, 0), pady=(4, 6)
        )

        controls = ttk.Frame(main)
        controls.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        controls.grid_columnconfigure((0, 1, 2), weight=1)

        ttk.Label(controls, text="Palavra para WordNet").grid(row=0, column=0, padx=4, pady=(0, 2), sticky="w")
        ttk.Label(controls, text="Top N (padrão 10)").grid(row=0, column=1, padx=4, pady=(0, 2), sticky="w")
        ttk.Label(controls, text="N-grama n (padrão 2)").grid(row=0, column=2, padx=4, pady=(0, 2), sticky="w")

        self._widgets["wordnet_word"] = ttk.Entry(controls)
        self._widgets["wordnet_word"].grid(row=1, column=0, padx=4, pady=4, sticky="ew")

        self._widgets["top_n"] = ttk.Entry(controls)
        self._widgets["top_n"].grid(row=1, column=1, padx=4, pady=4, sticky="ew")

        self._widgets["ngram_n"] = ttk.Entry(controls)
        self._widgets["ngram_n"].grid(row=1, column=2, padx=4, pady=4, sticky="ew")

        ttk.Label(main, text="Texto para Similaridade (Bloco E)").grid(
            row=5, column=0, columnspan=2, sticky="w"
        )

        self._widgets["compare_text"] = tk.Text(main, height=10)
        self._widgets["compare_text"].grid(row=6, column=0, columnspan=2, sticky="ew", pady=(4, 8))

        notebook = ttk.Notebook(main)
        notebook.grid(row=7, column=0, columnspan=2, sticky="nsew")

        tabs = {
            "Resumo": "result_global",
            "Bloco A": "result_a",
            "Bloco B": "result_b",
            "Bloco C": "result_c",
            "Bloco D": "result_d",
            "Bloco E": "result_e",
        }
        for tab_name, key in tabs.items():
            tab_frame = ttk.Frame(notebook)
            notebook.add(tab_frame, text=tab_name)
            box = tk.Text(tab_frame, state="disabled", font=("Arial", 12), wrap="word")
            box.pack(fill="both", expand=True, padx=8, pady=8)
            self._widgets[key] = box

        status = ttk.Label(main, text="Pronto para análise.", font=("Arial", 11), anchor="w")
        status.grid(row=8, column=0, columnspan=2, sticky="w", pady=(6, 0))
        self._widgets["status"] = status


if __name__ == "__main__":
    window = Interface()
    window.open_homepage()
