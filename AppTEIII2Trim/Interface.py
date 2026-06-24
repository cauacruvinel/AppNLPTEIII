import customtkinter
from tkinter import filedialog
from tkinter import messagebox
import AnalisadorNLP

class Interface:
	def __init__(self):
		self.analyser = AnalisadorNLP.AnalisadorNLP()
		self.homepage = None
		self._widgets = {}

	def clean_text(self):
		self._widgets["textbox"].delete("1.0", "end")
		self._widgets["result_box"].delete("1.0", "end")
		self._widgets["status"].configure(text="Texto limpo.")

	def clean_url(self):
		self._widgets["text_url"].delete(0, "end")

	def upload_file(self):
		self._widgets["status"].configure(
			text="📂 Abrindo seletor de arquivo..."
		)

		self.analyser = filedialog.askopenfilename(
			title="Selecione um Arquivo",
			filetypes=[("Texto", "*.txt"), ("Todos os arquivos", "*.*")]
		)
		if self.analyser:
			try:
				self.analyser.open_file(self)
			except Exception as e:
				messagebox.showwarning(f"Erro ao abrir o arquivo {e}")

	def open_homepage(self):
		customtkinter.set_default_color_theme("blue")
		customtkinter.set_appearance_mode("dark")

		self.homepage = customtkinter.CTk()
		self.homepage.title("Analisador de texto NLP - TextBlob + spaCy + NLTK")
		self.homepage.geometry("1080x720")
		self.homepage.minsize(800, 600)

		self.homepage.grid_columnconfigure(0, weight=0)
		self.homepage.grid_columnconfigure(1, weight=1)
		self.homepage.grid_rowconfigure(0, weight=1)

		self._build_sidebar()
		self._build_main()

		self.homepage.mainloop()

	def _build_sidebar(self):
		sidebar = customtkinter.CTkFrame(
			self.homepage, width=180, corner_radius=0
		)
		sidebar.grid(row=0, column=0, sticky="nsew")
		sidebar.grid_rowconfigure(5, weight=1)

		customtkinter.CTkLabel(
			sidebar, text="⚙ Analisador de Texto - NLP",
			font=("Arial", 16, "bold"), anchor="w"
		).grid(row=0, column=0, padx=16, pady=(20, 10), sticky="ew")

		customtkinter.CTkButton(
			sidebar, text="🔍 Analisar",
			command=self.analyser.analyse_text,
			font=("Arial", 13, "bold"),
			height=38, corner_radius=10
		).grid(row=1, column=0, padx=12, pady=6, sticky="ew")

		customtkinter.CTkButton(
			sidebar, text="📂 Carregar Arquivo",
			command=self.upload_file,
			font=("Arial", 12), height=34,
			corner_radius=10, fg_color="transparent",
			border_width=1
		).grid(row=2, column=0, padx=12, pady=6, sticky="ew")

		customtkinter.CTkButton(
			sidebar, text="🗑 Limpar",
			command=self.clean_text,
			font=("Arial", 12), height=34,
			corner_radius=10, fg_color="transparent",
			border_width=1
		).grid(row=3, column=0, padx=12, pady=6, sticky="ew")

	def _build_main(self):
		main = customtkinter.CTkFrame(self.homepage, fg_color="transparent")
		main.grid(row=0, column=1, sticky="nsew", padx=16, pady=16)

		main.grid_columnconfigure(0, weight=0)
		main.grid_columnconfigure(0, weight=1)
		main.grid_columnconfigure(1, weight=1)
		main.grid_columnconfigure(1, weight=0)
		main.grid_columnconfigure(2, weight=0)
		main.grid_rowconfigure(1, weight=1)
		main.grid_rowconfigure(4, weight=2)

		customtkinter.CTkLabel(
			main, text="Texto de Entrada",
			font=("Arial", 14, "bold"), anchor="w"
		).grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 4))

		textbox = customtkinter.CTkTextbox(
			main, corner_radius=12,
			border_width=2, border_color="#1F6AA5",
			font=("Arial", 13), wrap="word"
		)
		textbox.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=(0, 10))
		self._widgets["textbox"] = textbox

		customtkinter.CTkLabel(
			main, text="URL:",
			font=("Arial", 13, "bold"), anchor="w"
		).grid(row=2, column=0, sticky="w", pady=(0, 8))

		text_url = customtkinter.CTkEntry(
			main, height=32, corner_radius=10,
			border_width=2, border_color="#1F6AA5",
			font=("Arial", 13), placeholder_text="https://..."
		)
		text_url.grid(row=2, column=1, sticky="ew", padx=(0, 8), pady=(0, 8))
		self._widgets["text_url"] = text_url

		customtkinter.CTkButton(
			main, text="🌐 Buscar",
			command=self.analyser.self.search_url,
			height=32, corner_radius=10,
			font=("Arial", 12, "bold")
		).grid(row=2, column=2, sticky="ew", padx=(0, 8), pady=(0, 8))

		customtkinter.CTkButton(
			main, text="🗑 Limpar URL",
			command=self.clean_url,
			font=("Arial", 12), height=32,
			corner_radius=10
		).grid(row=2, column=3, pady=(0, 8), sticky="ew")

		customtkinter.CTkLabel(
			main, text="Resultado da Análise",
			font=("Arial", 14, "bold"), anchor="w"
		).grid(row=3, column=0, columnspan=3, sticky="w", pady=(4, 4))

		tabview = customtkinter.CTkTabview(main, corner_radius=12)
		tabview.grid(row=4, column=0, columnspan=3, sticky="nsew")

		for aba in ("Resumo", "Entidades", "Sentimento", "Tokens"):
			tabview.add(aba)

		result_box = customtkinter.CTkTextbox(
			tabview.tab("Resumo"),
			corner_radius=10, font=("Arial", 13),
			border_width=1, border_color="#1F6AA5",
			state="disabled"
		)
		result_box.pack(fill="both", expand=True, padx=8, pady=8)
		self._widgets["result_box"] = result_box

		status = customtkinter.CTkLabel(
			main, text="Pronto para análise.",
			font=("Arial", 11), anchor="w",
			text_color="gray"
		)
		status.grid(row=5, column=0, columnspan=3, sticky="w", pady=(6, 0))
		self._widgets["status"] = status

window = Interface()
window.open_homepage()