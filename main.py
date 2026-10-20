import flet as ft
from alert import AlertManager
from deposito_strumenti import DepositoStrumenti
from deposito_strumenti import DepositoStrumenti
from strumento import Strumento

FILE_STRUMENTI = "strumenti.csv"

def main(page: ft.Page):
    page.title = "Lab05"
    page.horizontal_alignment = "center"
    page.theme_mode = ft.ThemeMode.DARK

    # --- ALERT ---
    alert = AlertManager(page)

    # --- LA LOGICA DELL'APPLICAZIONE E' PRESA DAL DEPOSITO DI STRUMENTI DEL LAB03 ---
    deposito = DepositoStrumenti("Deposito Strumenti Musicali", "Alessandro Visconti")
    try:
        deposito.carica_file_strumenti(FILE_STRUMENTI)  # Carica il file
    except FileNotFoundError as e:
        alert.show_alert(f"❌ {e}")  # Fa apparire una finestra che mostra l'errore

    # --- UI ELEMENTI ---

    # Text per mostrare il nome e il responsabile del deposito
    txt_titolo = ft.Text(value=deposito.nome, size=38, weight=ft.FontWeight.BOLD)
    txt_responsabile = ft.Text(
        value=f"Responsabile: {deposito.get_responsabile()}",
        size=16,
        weight=ft.FontWeight.BOLD
    )

    # TextField per responsabile
    input_responsabile = ft.TextField(value=deposito.get_responsabile(), label="Responsabile")

    # ListView per mostrare la lista di strumenti aggiornata
    lista_strumenti = ft.ListView(expand=True, spacing=5, padding=10, auto_scroll=True)

    # Tutti i TextField per le info necessarie per aggiungere un nuovo strumento (tipo, marca, anno, contatore posti)
    input_tipo = ft.TextField(label="Tipo di strumento", width=200)
    input_marca = ft.TextField(label="Marca", width=200)
    input_anno = ft.TextField(label="Anno di acquisto", width=150)
    input_valore = ft.TextField(value="0", text_align=ft.TextAlign.RIGHT, width=100)

    # --- FUNZIONI APP ---
    def aggiorna_lista_strumenti():
        lista_strumenti.controls.clear()
        for strumento in deposito.strumenti_ordinati_per_marca():
            stato = "✅" if strumento.disponibile else "⛔"
            lista_strumenti.controls.append(ft.Text(f"{stato} {strumento}"))
        page.update()

    # --- HANDLERS APP ---
    def cambia_tema(e):
        page.theme_mode = ft.ThemeMode.DARK if toggle_cambia_tema.value else ft.ThemeMode.LIGHT
        toggle_cambia_tema.label = "Tema scuro" if toggle_cambia_tema.value else "Tema chiaro"
        page.update()

    def conferma_responsabile(e):
        deposito.set_responsabile(input_responsabile.value)
        txt_responsabile.value = f"Responsabile: {deposito.get_responsabile()}"
        page.update()

    # Handlers per la gestione dei pulsanti utili all'inserimento di un nuovo strumento
    def decrementa_valore(e):
        currentVal = int(input_valore.value)
        if currentVal > 0:
            input_valore.value = currentVal - 1
            input_valore.update()

    def incrementa_valore(e):
        currentVal = int(input_valore.value)
        input_valore.value = currentVal + 1
        input_valore.update()

    def aggiungi_nuovo_strumento(e):
        if not input_tipo.value or not input_marca.value or not input_anno.value:
            alert.show_alert("Compilare tutti i campi!")
            return

        try:
            anno_int = int(str(input_anno.value).strip())
            valore_int = int(str(input_valore.value).strip())
        except (ValueError, TypeError):
            alert.show_alert("Valore non numerico per il campo anno o valore!")
            return

        nuovo = Strumento(input_tipo.value, input_marca.value, anno_int, valore_int)
        deposito.aggiungi_strumento(nuovo)

        input_tipo.value = ""
        input_marca.value = ""
        input_anno.value = ""
        input_valore.value = "0"
        input_valore.update()

        aggiorna_lista_strumenti()

    # --- EVENTI ---
    toggle_cambia_tema = ft.Switch(label="Tema scuro", value=True, on_change=cambia_tema)
    pulsante_conferma_responsabile = ft.Button("Conferma", on_click=conferma_responsabile)

    # Pulsanti per la gestione dell'inserimento di un nuovo strumento
    btn_meno = ft.IconButton(ft.Icons.REMOVE, on_click=decrementa_valore)
    btn_piu = ft.IconButton(ft.Icons.ADD, on_click=incrementa_valore)
    pulsante_aggiungi_strumento = ft.Button("Aggiungi strumento", on_click=aggiungi_nuovo_strumento)

    # --- LAYOUT ---
    page.add(
        toggle_cambia_tema,

        # Sezione 1
        txt_titolo,
        txt_responsabile,
        ft.Divider(),

        # Sezione 2
        ft.Text("Modifica Informazioni", size=20),
        ft.Row(spacing=200,
               controls=[input_responsabile, pulsante_conferma_responsabile],
               alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 3
        ft.Divider(),
        ft.Text("Aggiungi Nuovo Strumento", size=20),
        ft.Row([input_tipo, input_marca, input_anno], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([btn_meno, input_valore, btn_piu], alignment=ft.MainAxisAlignment.CENTER),
        ft.Row([pulsante_aggiungi_strumento], alignment=ft.MainAxisAlignment.CENTER),

        # Sezione 4
        ft.Divider(),
        ft.Text("Strumenti", size=20),
        lista_strumenti,
    )
    aggiorna_lista_strumenti()

#ft.app(target=main)
ft.run(main)