import flet as ft
import json
import os
from datetime import datetime, timedelta

# Názov lokálneho súboru, kde budeme držať dáta
DATA_FILE = "pause_and_buy_data.json"

# Pomocné funkcie na načítanie a ukladanie dát
def load_items():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_items(items):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=4)

def main(page: ft.Page):
    page.title = "Pause & Buy"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.START
    
    items_list = ft.ListView(expand=1, spacing=10, padding=20)
    
    # Načítame uložené dáta hneď pri štarte aplikácie
    saved_items = load_items()

    # Funkcia na prekreslenie zoznamu na obrazovke
    def build_list():
        items_list.controls.clear()
        
        for index, item in enumerate(saved_items):
            # Výpočet zostávajúceho času (72 hodín od vytvorenia)
            created_at = datetime.fromisoformat(item["created_at"])
            deadline = created_at + timedelta(hours=72)
            now = datetime.now()
            
            if now >= deadline:
                time_str = "Čas vypršal! Je moment pravdy."
                time_color = ft.colors.GREEN_600
            else:
                remaining = deadline - now
                hours, remainder = divmod(remaining.seconds, 3600)
                minutes, _ = divmod(remainder, 60)
                # Zobrazenie v tvare: Dni, hodiny, minúty
                time_str = f"Zostáva: {remaining.days}d {hours}h {minutes}m"
                time_color = ft.colors.RED_ACCENT

            # Tlačidlá na interakciu (Odkaz na e-shop)
            trailing_actions = []
            if item.get("url"):
                trailing_actions.append(
                    ft.IconButton(
                        icon=ft.icons.LINK,
                        icon_color=ft.colors.BLUE_700,
                        url=item["url"],
                        tooltip="Otvoriť obchod"
                    )
                )

            items_list.controls.append(
                ft.Card(
                    content=ft.Container(
                        content=ft.Column(
                            [
                                ft.ListTile(
                                    leading=ft.Icon(ft.icons.SHOPPING_BAG, color=ft.colors.BLUE_ACCENT),
                                    title=ft.Text(item["name"], weight=ft.FontWeight.BOLD, size=18),
                                    subtitle=ft.Text(f"Cena: {item['price']} €", size=16),
                                    trailing=ft.Row(trailing_actions, wrap=False) if trailing_actions else None
                                ),
                                ft.Padding(
                                    ft.Row(
                                        [
                                            ft.Icon(ft.icons.TIMER, color=time_color, size=16),
                                            ft.Text(time_str, color=time_color, weight=ft.FontWeight.W_500),
                                        ]
                                    ),
                                    padding=ft.padding.only(left=16, bottom=16)
                                )
                            ]
                        ),
                        padding=5,
                    )
                )
            )
        page.update()

    # Funkcia na pridanie novej položky
    def add_clicked(e):
        if not item_name.value or not item_price.value:
            return
        
        # Vytvoríme štruktúrovaný slovník s dátami
        new_item = {
            "name": item_name.value,
            "price": item_price.value,
            "url": item_url.value,
            "created_at": datetime.now().isoformat() # Uložíme presný aktuálny čas
        }
        
        saved_items.append(new_item)
        save_items(saved_items) # Zapíšeme do JSON súboru
        
        # Vyčistíme polia
        item_name.value = ""
        item_price.value = ""
        item_url.value = ""
        
        build_list()

    # Definícia UI komponentov
    item_name = ft.TextField(label="Čo si chceš kúpiť?", expand=True, border_radius=10)
    item_price = ft.TextField(label="Cena (€)", width=100, keyboard_type=ft.KeyboardType.NUMBER, border_radius=10)
    item_url = ft.TextField(label="Odkaz na web (voliteľné)", expand=True, border_radius=10)
    
    add_button = ft.FloatingActionButton(
        icon=ft.icons.ADD, 
        on_click=add_clicked, 
        bgcolor=ft.colors.BLUE_ACCENT, 
        icon_color=ft.colors.WHITE
    )

    # Poskladanie celej aplikácie
    page.add(
        ft.AppBar(
            title=ft.Text("Pause & Buy", color=ft.colors.WHITE, weight=ft.FontWeight.BOLD),
            bgcolor=ft.colors.BLUE_900,
            center_title=True
        ),
        ft.Padding(ft.Row([item_name, item_price], alignment=ft.MainAxisAlignment.SPACE_BETWEEN), padding=10),
        ft.Padding(ft.Row([item_url]), padding=10),
        ft.Padding(ft.Text("Aktuálne pokušenia v čakárni:", size=16, weight=ft.FontWeight.W_600), padding=ft.padding.only(left=15, top=10)),
        items_list,
        add_button
    )
    
    # Prvé vykreslenie zoznamu pri načítaní appky
    build_list()

# Spustenie aplikácie
ft.app(target=main)