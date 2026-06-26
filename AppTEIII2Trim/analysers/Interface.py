import json
from tkinter import filedialog, messagebox
import customtkinter

class Interface:
    def __init__(self):
        self.homepage = None
        self._widgets = {}
        self.analyser = None

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
            with open(file_path, "r", encoding="utf-8") as f:
                file_text = f.read()
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
            self._render_tab("result_a", self.analyser.analyse_block_a(self._input_text()))
            self._set_status("Bloco A finalizado.")
        except Exception as exc:
            messagebox.showwarning("Validação", str(exc))

    def _run_block_b(self):
        try:
            self._render_tab("result_b", self.analyser.analyse_block_b(self._input_text()))
            self._set_status("Bloco B finalizado.")
        except Exception as exc:
            messagebox.showwarning("Validação", str(exc))

    def _run_block_c(self):
        try:
            self._render_tab("result_c", self.analyser.analyse_block_c(self._input_text()))
            self._set_status("Bloco C finalizado.")
        except Exception as exc:
            messagebox.showwarning("Validação", str(exc))

    def _run_block_d(self):
        try:
            payload = self.analyser.analyse_block_d(
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
            payload = self.analyser.analyse_block_e(
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
        customtkinter.set_default_color_theme("blue")
        customtkinter.set_appearance_mode("dark")

        self.homepage = customtkinter.CTk()
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
        sidebar = customtkinter.CTkFrame(self.homepage, width=220, corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_rowconfigure(10, weight=1)

        customtkinter.CTkLabel(
            sidebar,
            text="⚙ NLP por Blocos",
            font=("Arial", 16, "bold"),
            anchor="w",
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
            customtkinter.CTkButton(
                sidebar,
                text=label,
                command=callback,
                font=("Arial", 12, "bold" if index <= 6 else "normal"),
                height=34,
                corner_radius=10,
            ).grid(row=index, column=0, padx=12, pady=6, sticky="ew")

    def _build_main(self):
        main = customtkinter.CTkFrame(self.homepage, fg_color="transparent")
        main.grid(row=0, column=1, sticky="nsew", padx=16, pady=16)
        main.grid_columnconfigure(0, weight=1)
        main.grid_columnconfigure(1, weight=1)
        main.grid_rowconfigure(5, weight=1)

        customtkinter.CTkLabel(main, text="Texto de Entrada", font=("Arial", 14, "bold")).grid(
            row=0, column=0, columnspan=2, sticky="w"
        )

        textbox = customtkinter.CTkTextbox(main, font=("Arial", 13), wrap="word")
        textbox.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=(4, 8))
        self._widgets["textbox"] = textbox

        self._widgets["text_url"] = customtkinter.CTkEntry(
            main, placeholder_text="https://...", font=("Arial", 12)
        )
        self._widgets["text_url"].grid(row=2, column=0, sticky="ew", pady=(0, 6))

        customtkinter.CTkButton(main, text="🌐 Buscar URL", command=self.load_url).grid(
            row=2, column=1, sticky="ew", padx=(8, 0), pady=(0, 6)
        )

        controls = customtkinter.CTkFrame(main)
        controls.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 8))
        controls.grid_columnconfigure((0, 1, 2), weight=1)

        self._widgets["wordnet_word"] = customtkinter.CTkEntry(
            controls, placeholder_text="Palavra para WordNet"
        )
        self._widgets["wordnet_word"].grid(row=0, column=0, padx=4, pady=4, sticky="ew")

        self._widgets["top_n"] = customtkinter.CTkEntry(controls, placeholder_text="Top N (padrão 10)")
        self._widgets["top_n"].grid(row=0, column=1, padx=4, pady=4, sticky="ew")

        self._widgets["ngram_n"] = customtkinter.CTkEntry(controls, placeholder_text="N-grama n (padrão 2)")
        self._widgets["ngram_n"].grid(row=0, column=2, padx=4, pady=4, sticky="ew")

        customtkinter.CTkLabel(main, text="Texto para Similaridade (Bloco E)").grid(
            row=4, column=0, columnspan=2, sticky="w"
        )

        self._widgets["compare_text"] = customtkinter.CTkTextbox(main, height=80)
        self._widgets["compare_text"].grid(row=5, column=0, columnspan=2, sticky="ew", pady=(4, 8))

        tabview = customtkinter.CTkTabview(main)
        tabview.grid(row=6, column=0, columnspan=2, sticky="nsew")
        main.grid_rowconfigure(6, weight=1)

        tabs = {
            "Resumo": "result_global",
            "Bloco A": "result_a",
            "Bloco B": "result_b",
            "Bloco C": "result_c",
            "Bloco D": "result_d",
            "Bloco E": "result_e",
        }
        for tab_name, key in tabs.items():
            tabview.add(tab_name)
            box = customtkinter.CTkTextbox(tabview.tab(tab_name), state="disabled", font=("Arial", 12))
            box.pack(fill="both", expand=True, padx=8, pady=8)
            self._widgets[key] = box

        status = customtkinter.CTkLabel(
            main, text="Pronto para análise.", font=("Arial", 11), anchor="w", text_color="gray"
        )
        status.grid(row=7, column=0, columnspan=2, sticky="w", pady=(6, 0))
        self._widgets["status"] = status


if __name__ == "__main__":
    from NLPAnalyser import NLPAnalyser
    window = Interface()
    window.analyser = NLPAnalyser()
    window.open_homepage()