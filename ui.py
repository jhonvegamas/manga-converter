import os
import threading
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk
import customtkinter as ctk

from converter import (
    convert_pdf_to_cbz, detect_mode,
    get_all_profiles, save_profile, delete_saved_profile,
    DEVICE_PROFILES, process_image,
)

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

NOTION_COLORS = {
    "primary": "#5645d4",
    "primary_hover": "#4534b3",
    "primary_light": "#e6e0f5",
    "navy": "#0a1530",
    "navy_mid": "#1a2a52",
    "canvas": "#ffffff",
    "surface": "#f6f5f4",
    "surface_soft": "#fafaf9",
    "hairline": "#e5e3df",
    "hairline_soft": "#f0eeec",
    "ink": "#000000",
    "charcoal": "#37352f",
    "steel": "#5d5b54",
    "muted": "#a4a097",
    "muted_light": "#bbb8b1",
    "card_mint": "#d9f3e1",
    "card_peach": "#ffe8d4",
    "card_sky": "#dcecfa",
    "card_lavender": "#e6e0f5",
    "card_rose": "#fde0ec",
    "success": "#1aae39",
    "warning": "#dd5b00",
    "error": "#e03131",
    "link": "#0075de",
    "on_dark": "#ffffff",
    "on_dark_muted": "#a4a097",
}

FONTS = {
    "display": ("Segoe UI", 28, "bold"),
    "heading": ("Segoe UI", 18, "bold"),
    "subtitle": ("Segoe UI", 14, "normal"),
    "body": ("Segoe UI", 13, "normal"),
    "body_bold": ("Segoe UI", 13, "bold"),
    "caption": ("Segoe UI", 12, "normal"),
    "caption_bold": ("Segoe UI", 12, "bold"),
    "small": ("Segoe UI", 11, "normal"),
    "button": ("Segoe UI", 13, "bold"),
    "mono": ("Consolas", 12, "normal"),
}


class NotionButton(ctk.CTkButton):
    def __init__(self, master, text="", variant="primary", **kwargs):
        if variant == "primary":
            fg = NOTION_COLORS["primary"]
            hov = NOTION_COLORS["primary_hover"]
            txt = NOTION_COLORS["on_dark"]
        elif variant == "secondary":
            fg = "transparent"
            hov = NOTION_COLORS["surface"]
            txt = NOTION_COLORS["charcoal"]
            kwargs.setdefault("border_width", 1)
            kwargs.setdefault("border_color", NOTION_COLORS["hairline"])
        elif variant == "ghost":
            fg = "transparent"
            hov = NOTION_COLORS["surface"]
            txt = NOTION_COLORS["steel"]
        elif variant == "danger":
            fg = NOTION_COLORS["error"]
            hov = "#c62828"
            txt = NOTION_COLORS["on_dark"]
        else:
            fg = NOTION_COLORS["primary"]
            hov = NOTION_COLORS["primary_hover"]
            txt = NOTION_COLORS["on_dark"]
        kwargs.setdefault("height", 38)
        super().__init__(
            master, text=text, fg_color=fg, hover_color=hov,
            text_color=txt, font=FONTS["button"], corner_radius=8,
            **kwargs
        )


class NotionTag(ctk.CTkLabel):
    def __init__(self, master, text="", color="purple", **kwargs):
        bg_map = {
            "purple": NOTION_COLORS["card_lavender"],
            "orange": NOTION_COLORS["card_peach"],
            "green": NOTION_COLORS["card_mint"],
            "pink": NOTION_COLORS["card_rose"],
            "sky": NOTION_COLORS["card_sky"],
        }
        txt_map = {
            "purple": NOTION_COLORS["primary"],
            "orange": NOTION_COLORS["warning"],
            "green": NOTION_COLORS["success"],
            "pink": "#a02e6d",
            "sky": "#005bab",
        }
        bg = bg_map.get(color, NOTION_COLORS["card_lavender"])
        tc = txt_map.get(color, NOTION_COLORS["primary"])
        super().__init__(
            master, text=text, fg_color=bg,
            text_color=tc, font=FONTS["caption_bold"],
            corner_radius=6, padx=8, pady=2, **kwargs
        )


class DropZone(ctk.CTkFrame):
    def __init__(self, master, on_drop, **kwargs):
        super().__init__(
            master, fg_color=NOTION_COLORS["surface_soft"],
            corner_radius=12, border_width=2,
            border_color=NOTION_COLORS["hairline"], **kwargs
        )
        self.on_drop = on_drop
        self.configure(cursor="hand2")

        self.label_icon = ctk.CTkLabel(
            self, text="+", font=("Segoe UI", 36, "normal"),
            text_color=NOTION_COLORS["muted_light"]
        )
        self.label_icon.pack(pady=(20, 0))

        self.label_text = ctk.CTkLabel(
            self, text="Arrastra un PDF aqu\u00ed\no haz clic para buscar",
            font=FONTS["body"], text_color=NOTION_COLORS["steel"],
            justify="center"
        )
        self.label_text.pack(pady=(4, 4))

        self.label_support = ctk.CTkLabel(
            self, text="Soporta PDF de manga y manhwa",
            font=FONTS["small"], text_color=NOTION_COLORS["muted_light"]
        )
        self.label_support.pack(pady=(0, 20))

        self.label_tag = ctk.CTkLabel(
            self, text="", font=FONTS["caption"],
            text_color=NOTION_COLORS["steel"], wraplength=350
        )
        self.label_tag.pack(pady=(0, 10))

        self.bind("<Button-1>", self.on_click)
        self.label_icon.bind("<Button-1>", self.on_click)
        self.label_text.bind("<Button-1>", self.on_click)

    def update_paths(self, paths):
        count = len(paths)
        if count == 0:
            self.reset()
        elif count == 1:
            self.label_tag.configure(text=os.path.basename(paths[0]), text_color=NOTION_COLORS["charcoal"])
        else:
            self.label_tag.configure(text=f"{count} archivos seleccionados", text_color=NOTION_COLORS["charcoal"])
        self.label_icon.configure(text="\u2713")
        self.label_icon.configure(text_color=NOTION_COLORS["success"])

    def reset(self):
        self.label_tag.configure(text="")
        self.label_icon.configure(text="+")
        self.label_icon.configure(text_color=NOTION_COLORS["muted_light"])

    def on_click(self, event=None):
        paths = filedialog.askopenfilenames(
            title="Seleccionar PDFs",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        if paths:
            self.update_paths(list(paths))
            self.on_drop(list(paths))


class ModeSelector(ctk.CTkFrame):
    def __init__(self, master, on_change=None, **kwargs):
        super().__init__(
            master, fg_color=NOTION_COLORS["surface_soft"],
            corner_radius=10, **kwargs
        )
        self.on_change = on_change
        self._mode = tk.StringVar(value="auto")

        ctk.CTkLabel(
            self, text="Modo", font=FONTS["caption_bold"],
            text_color=NOTION_COLORS["steel"]
        ).pack(anchor="w", padx=12, pady=(10, 6))

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(padx=8, pady=(0, 10), fill="x")

        self.buttons = {}
        for key, label in [("auto", "Auto"), ("manga", "Manga"), ("manhwa", "Manhwa")]:
            btn = ctk.CTkButton(
                btn_frame, text=label, font=FONTS["button"],
                corner_radius=8, height=32,
                fg_color=NOTION_COLORS["canvas"],
                text_color=NOTION_COLORS["charcoal"],
                hover_color=NOTION_COLORS["primary_light"],
                border_width=1, border_color=NOTION_COLORS["hairline"],
                command=lambda k=key: self.set_mode(k)
            )
            btn.pack(side="left", padx=2, fill="x", expand=True)
            self.buttons[key] = btn
        self.set_mode("auto")

    def set_mode(self, mode):
        self._mode.set(mode)
        for key, btn in self.buttons.items():
            if key == mode:
                btn.configure(
                    fg_color=NOTION_COLORS["primary"],
                    text_color=NOTION_COLORS["on_dark"],
                    border_color=NOTION_COLORS["primary"],
                    hover_color=NOTION_COLORS["primary_hover"],
                )
            else:
                btn.configure(
                    fg_color=NOTION_COLORS["canvas"],
                    text_color=NOTION_COLORS["charcoal"],
                    border_color=NOTION_COLORS["hairline"],
                    hover_color=NOTION_COLORS["primary_light"],
                )
        if self.on_change:
            self.on_change(mode)

    def get(self):
        return self._mode.get()


class SettingsCard(ctk.CTkFrame):
    def __init__(self, master, on_settings_change=None, **kwargs):
        super().__init__(
            master, fg_color=NOTION_COLORS["surface_soft"],
            corner_radius=10, **kwargs
        )
        self.on_settings_change = on_settings_change
        self._current_custom = (0, 0)
        self._ignore_next_change = False

        ctk.CTkLabel(
            self, text="Ajustes de salida", font=FONTS["caption_bold"],
            text_color=NOTION_COLORS["steel"]
        ).pack(anchor="w", padx=12, pady=(10, 6))

        self._build_device_row()
        self._build_custom_row()
        self._build_gamma_row()
        self._build_toggles()
        self._build_profile_btn()
        self._on_device_change(self._device_var.get())

    def _build_device_row(self):
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=2)
        ctk.CTkLabel(
            row, text="Dispositivo", font=FONTS["small"],
            text_color=NOTION_COLORS["muted"]
        ).pack(side="left")

        self.all_profiles = get_all_profiles()
        names = list(self.all_profiles.keys())
        self._device_var = tk.StringVar(value=names[0] if names else "Custom")

        self.device_menu = ctk.CTkOptionMenu(
            row, variable=self._device_var, values=names,
            font=FONTS["small"], corner_radius=6,
            fg_color=NOTION_COLORS["canvas"],
            text_color=NOTION_COLORS["charcoal"],
            button_color=NOTION_COLORS["muted_light"],
            button_hover_color=NOTION_COLORS["muted"],
            dropdown_fg_color=NOTION_COLORS["canvas"],
            dropdown_text_color=NOTION_COLORS["charcoal"],
            dropdown_hover_color=NOTION_COLORS["primary_light"],
            dropdown_font=FONTS["small"],
            command=self._on_device_change
        )
        self.device_menu.pack(side="right")

    def _build_custom_row(self):
        self._custom_frame = ctk.CTkFrame(self, fg_color="transparent")
        row = ctk.CTkFrame(self._custom_frame, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=2)

        ctk.CTkLabel(
            row, text="Ancho", font=FONTS["small"],
            text_color=NOTION_COLORS["muted"]
        ).pack(side="left", padx=(0, 4))

        self._w_entry = ctk.CTkEntry(
            row, width=60, height=28, font=FONTS["small"],
            corner_radius=6, fg_color=NOTION_COLORS["canvas"],
            border_color=NOTION_COLORS["hairline"]
        )
        self._w_entry.pack(side="left", padx=(0, 8))
        self._w_entry.bind("<KeyRelease>", lambda e: self._on_custom_change())

        ctk.CTkLabel(
            row, text="Alto", font=FONTS["small"],
            text_color=NOTION_COLORS["muted"]
        ).pack(side="left", padx=(0, 4))

        self._h_entry = ctk.CTkEntry(
            row, width=60, height=28, font=FONTS["small"],
            corner_radius=6, fg_color=NOTION_COLORS["canvas"],
            border_color=NOTION_COLORS["hairline"]
        )
        self._h_entry.pack(side="left")
        self._h_entry.bind("<KeyRelease>", lambda e: self._on_custom_change())
        self._custom_frame.pack_forget()

    def _build_gamma_row(self):
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=2)

        self._gamma_label = ctk.CTkLabel(
            row, text="Gamma  1.00", font=FONTS["small"],
            text_color=NOTION_COLORS["muted"]
        )
        self._gamma_label.pack(side="left")

        self._gamma_var = tk.DoubleVar(value=1.0)
        self.gamma_slider = ctk.CTkSlider(
            row, from_=0.5, to=2.0, number_of_steps=150,
            variable=self._gamma_var,
            fg_color=NOTION_COLORS["hairline"],
            progress_color=NOTION_COLORS["primary"],
            button_color=NOTION_COLORS["primary"],
            button_hover_color=NOTION_COLORS["primary_hover"],
            command=self._on_gamma_change,
            width=140
        )
        self.gamma_slider.pack(side="right")

    def _build_toggles(self):
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=2)

        self._grayscale_var = tk.BooleanVar(value=False)
        self._autocontrast_var = tk.BooleanVar(value=False)

        self.grayscale_cb = ctk.CTkCheckBox(
            row, text="Grises", font=FONTS["small"],
            variable=self._grayscale_var,
            fg_color=NOTION_COLORS["primary"],
            hover_color=NOTION_COLORS["primary_hover"],
            text_color=NOTION_COLORS["charcoal"],
            command=self._notify_change,
            corner_radius=4, checkbox_width=18, checkbox_height=18
        )
        self.grayscale_cb.pack(side="left", padx=(0, 12))

        self.autocontrast_cb = ctk.CTkCheckBox(
            row, text="Autocontraste", font=FONTS["small"],
            variable=self._autocontrast_var,
            fg_color=NOTION_COLORS["primary"],
            hover_color=NOTION_COLORS["primary_hover"],
            text_color=NOTION_COLORS["charcoal"],
            command=self._notify_change,
            corner_radius=4, checkbox_width=18, checkbox_height=18
        )
        self.autocontrast_cb.pack(side="left")

    def _build_profile_btn(self):
        row = ctk.CTkFrame(self, fg_color="transparent")
        row.pack(fill="x", padx=12, pady=(6, 8))

        self.save_profile_btn = NotionButton(
            row, text="Guardar perfil", variant="ghost",
            height=28, command=self._save_profile_dialog
        )
        self.save_profile_btn.pack(side="left", padx=(0, 4))

        self.del_profile_btn = NotionButton(
            row, text="Eliminar perfil", variant="ghost",
            height=28, command=self._del_profile_dialog
        )
        self.del_profile_btn.pack(side="left")

    def _on_device_change(self, name):
        self._device_var.set(name)
        profiles = get_all_profiles()
        w, h = profiles.get(name, (0, 0))
        if name == "Custom":
            self._custom_frame.pack(fill="x")
            if self._current_custom != (0, 0):
                self._w_entry.delete(0, "end")
                self._w_entry.insert(0, str(self._current_custom[0]))
                self._h_entry.delete(0, "end")
                self._h_entry.insert(0, str(self._current_custom[1]))
        else:
            self._custom_frame.pack_forget()
        self._notify_change()

    def _on_custom_change(self):
        try:
            w = int(self._w_entry.get()) if self._w_entry.get() else 0
            h = int(self._h_entry.get()) if self._h_entry.get() else 0
            if w > 0 and h > 0:
                self._current_custom = (w, h)
        except ValueError:
            pass
        self._notify_change()

    def _on_gamma_change(self, val):
        self._gamma_label.configure(text=f"Gamma  {val:.2f}")
        self._notify_change()

    def _notify_change(self):
        if self.on_settings_change and not self._ignore_next_change:
            self.on_settings_change()

    def _save_profile_dialog(self):
        w, h = self._get_resolution()
        if w <= 0 or h <= 0:
            messagebox.showwarning("Perfil inv\u00e1lido", "Establece una resoluci\u00f3n v\u00e1lida primero.")
            return
        name = simpledialog.askstring(
            "Guardar perfil",
            f"Nombre para {w}x{h}:",
            parent=self.winfo_toplevel()
        )
        if name and name.strip():
            save_profile(name.strip(), w, h)
            self._refresh_device_list()
            messagebox.showinfo("Perfil guardado", f"Perfil \"{name}\" guardado.")

    def _del_profile_dialog(self):
        name = self._device_var.get()
        built_in = set(DEVICE_PROFILES.keys())
        if name in built_in:
            messagebox.showwarning(
                "No se puede eliminar",
                "Los perfiles incorporados no se pueden eliminar."
            )
            return
        if messagebox.askyesno("Eliminar perfil", f"\u00bfEliminar \"{name}\"?"):
            delete_saved_profile(name)
            self._refresh_device_list()

    def _refresh_device_list(self):
        profiles = get_all_profiles()
        names = list(profiles.keys())
        current = self._device_var.get()
        self.device_menu.configure(values=names)
        if current not in names:
            self._device_var.set(names[0] if names else "Custom")
            self._on_device_change(self._device_var.get())
        else:
            self._device_var.set(current)

    def _get_resolution(self):
        name = self._device_var.get()
        profiles = get_all_profiles()
        w, h = profiles.get(name, (0, 0))
        if name == "Custom":
            try:
                w = int(self._w_entry.get()) if self._w_entry.get() else 0
                h = int(self._h_entry.get()) if self._h_entry.get() else 0
            except ValueError:
                w, h = 0, 0
        return w, h

    def get_settings(self):
        w, h = self._get_resolution()
        return {
            "gamma": self._gamma_var.get(),
            "grayscale": self._grayscale_var.get(),
            "autocontrast": self._autocontrast_var.get(),
            "target_w": w,
            "target_h": h,
        }


class PreviewPanel(ctk.CTkScrollableFrame):
    def __init__(self, master, on_processed_ready=None, **kwargs):
        super().__init__(
            master, fg_color=NOTION_COLORS["canvas"],
            corner_radius=12, border_width=1,
            border_color=NOTION_COLORS["hairline"], **kwargs
        )
        self.orig_thumbnails = []
        self.proc_thumbnails = []
        self._cached_pages = []
        self._loading = False

        self._orig_label = ctk.CTkLabel(
            self, text="Original", font=FONTS["caption_bold"],
            text_color=NOTION_COLORS["steel"]
        )
        self._orig_label.pack(anchor="w", padx=12, pady=(10, 2))

        self._orig_frame = ctk.CTkFrame(self, fg_color="transparent")
        self._orig_frame.pack(fill="x", padx=8, pady=(0, 12))

        sep = ctk.CTkFrame(self, fg_color=NOTION_COLORS["hairline"], height=1)
        sep.pack(fill="x", padx=12, pady=0)

        self._proc_label = ctk.CTkLabel(
            self, text="Vista previa (procesado)", font=FONTS["caption_bold"],
            text_color=NOTION_COLORS["primary"]
        )
        self._proc_label.pack(anchor="w", padx=12, pady=(10, 2))

        self._proc_frame = ctk.CTkFrame(self, fg_color=NOTION_COLORS["surface_soft"],
                                        corner_radius=8)
        self._proc_frame.pack(fill="x", padx=8, pady=(0, 12), ipady=4)

        self._loading_label = ctk.CTkLabel(
            self, text="", font=FONTS["body"],
            text_color=NOTION_COLORS["muted"]
        )
        self._loading_label.pack(expand=True, pady=40)
        self._loading_label.configure(text="Selecciona un PDF\npara ver sus p\u00e1ginas")
        self._loading_label.pack(expand=True, pady=60)

    def load_pdf(self, pdf_path):
        self._loading = True
        self._cached_pages = []
        self._clear_frames()
        self._loading_label.configure(text="Cargando vista previa...")
        self._loading_label.pack(expand=True, pady=60)

        threading.Thread(target=self._load_pages, args=(pdf_path,), daemon=True).start()

    def _clear_frames(self):
        for w in self._orig_frame.winfo_children():
            w.destroy()
        for w in self._proc_frame.winfo_children():
            w.destroy()
        self.orig_thumbnails.clear()
        self.proc_thumbnails.clear()

    def _load_pages(self, pdf_path):
        import fitz
        try:
            doc = fitz.open(pdf_path)
            total = min(5, doc.page_count)
            for i in range(total):
                page = doc[i]
                pix = page.get_pixmap(dpi=72)
                img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
                img.thumbnail((160, 230), Image.LANCZOS)
                self._cached_pages.append(img)
                self.after(0, self._add_orig_thumb, img.copy(), i, total)
            doc.close()
            self.after(0, self._loading_done, total)
        except Exception as e:
            self.after(0, self._loading_error, str(e))

    def _add_orig_thumb(self, pil_img, idx, total):
        self._add_thumb_to_frame(self._orig_frame, pil_img, idx, total, "#5645d4",
                                 self.orig_thumbnails)

    def _add_proc_thumb(self, pil_img, idx, total):
        self._add_thumb_to_frame(self._proc_frame, pil_img, idx, total, "#1aae39",
                                 self.proc_thumbnails)

    def _add_thumb_to_frame(self, frame, pil_img, idx, total, border_color, storage):
        tk_img = ImageTk.PhotoImage(pil_img)
        f = ctk.CTkFrame(frame, fg_color="transparent")
        f.pack(side="left", padx=4, pady=4)

        lbl = tk.Label(
            f, image=tk_img, bg="#ffffff",
            borderwidth=2, relief="solid",
            highlightbackground=border_color,
            highlightcolor=border_color,
            highlightthickness=2 if border_color == "#1aae39" else 0
        )
        lbl.image = tk_img
        lbl.pack()

        ctk.CTkLabel(
            f, text=f"p.{idx+1}",
            font=FONTS["small"], text_color=NOTION_COLORS["muted"]
        ).pack()

        storage.append(lbl)

    def _loading_done(self, total):
        self._loading = False
        self._loading_label.pack_forget()
        self._render_processed()

    def _loading_error(self, msg):
        self._loading = False
        self._loading_label.configure(text=f"Error: {msg}")

    def _render_processed(self):
        if not self._cached_pages:
            return
        self._clear_proc()
        for i, orig in enumerate(self._cached_pages):
            img = orig.copy()
            thumb = img.resize((160, 230), Image.LANCZOS)
            self._add_proc_thumb(thumb, i, len(self._cached_pages))

    def refresh_processed(self, settings=None):
        if not self._cached_pages:
            return
        self._clear_proc()
        if settings is None:
            settings = {}
        for i, orig in enumerate(self._cached_pages):
            processed = process_image(orig, settings)
            processed.thumbnail((160, 230), Image.LANCZOS)
            self._add_proc_thumb(processed, i, len(self._cached_pages))

    def _clear_proc(self):
        for w in self._proc_frame.winfo_children():
            w.destroy()
        self.proc_thumbnails.clear()

    def has_pages(self):
        return len(self._cached_pages) > 0


class FileInfoCard(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master, fg_color=NOTION_COLORS["surface_soft"],
            corner_radius=10, **kwargs
        )
        self._info_labels = {}

        ctk.CTkLabel(
            self, text="Informaci\u00f3n", font=FONTS["caption_bold"],
            text_color=NOTION_COLORS["steel"]
        ).pack(anchor="w", padx=12, pady=(10, 6))

        for key, label in [
            ("file", "Archivo"),
            ("pages", "P\u00e1ginas"),
            ("detected", "Modo detectado"),
            ("resolution", "Resoluci\u00f3n"),
            ("size", "Tama\u00f1o"),
        ]:
            row = ctk.CTkFrame(self, fg_color="transparent")
            row.pack(fill="x", padx=12, pady=1)
            ctk.CTkLabel(
                row, text=label, font=FONTS["small"],
                text_color=NOTION_COLORS["muted"]
            ).pack(side="left")
            val = ctk.CTkLabel(
                row, text="\u2014", font=FONTS["small"],
                text_color=NOTION_COLORS["charcoal"]
            )
            val.pack(side="right")
            self._info_labels[key] = val
        self._info_labels["file"].configure(wraplength=200)

    def set_info(self, path, pages=None, detected=None, resolution=None, size=None):
        self._info_labels["file"].configure(text=os.path.basename(path)[:35])
        if pages is not None:
            self._info_labels["pages"].configure(text=str(pages))
        if detected is not None:
            tag_colors = {"manga": "sky", "manhwa": "orange", "auto": "purple"}
            self._info_labels["detected"].configure(
                text=detected.capitalize(),
                text_color=NOTION_COLORS.get(
                    tag_colors.get(detected, "purple"),
                    NOTION_COLORS["primary"]
                )
            )
        if resolution is not None:
            self._info_labels["resolution"].configure(text=resolution)
        if size is not None:
            if size > 1024 * 1024:
                self._info_labels["size"].configure(text=f"{size/(1024*1024):.1f} MB")
            elif size > 1024:
                self._info_labels["size"].configure(text=f"{size/1024:.1f} KB")
            else:
                self._info_labels["size"].configure(text=f"{size} B")

    def reset(self):
        for key in self._info_labels:
            self._info_labels[key].configure(text="\u2014")


class ResultCard(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        super().__init__(
            master, fg_color=NOTION_COLORS["surface_soft"],
            corner_radius=10, **kwargs
        )
        self._visible = False

        self._icon = ctk.CTkLabel(
            self, text="", font=("Segoe UI", 24),
            text_color=NOTION_COLORS["success"]
        )
        self._icon.pack(pady=(12, 2))

        self._title = ctk.CTkLabel(
            self, text="", font=FONTS["heading"],
            text_color=NOTION_COLORS["charcoal"]
        )
        self._title.pack()

        self._detail = ctk.CTkLabel(
            self, text="", font=FONTS["body"],
            text_color=NOTION_COLORS["steel"], wraplength=350,
            justify="center"
        )
        self._detail.pack(pady=(2, 12))

        self._open_btn = NotionButton(
            self, text="Abrir carpeta", variant="secondary",
            command=self._open_folder
        )
        self.pack_forget()

    def show_success(self, cbz_path, pages, images):
        self._icon.configure(text="\u2713", text_color=NOTION_COLORS["success"])
        self._title.configure(text="\u00a1Conversi\u00f3n completada!")
        self._detail.configure(
            text=f"{pages} p\u00e1ginas \u2192 {images} im\u00e1genes\n"
                 f"{os.path.basename(cbz_path)}"
        )
        self._cbz_path = cbz_path
        self._open_btn.pack(pady=(0, 12))
        self.pack(fill="x", padx=20, pady=8)
        self._visible = True

    def show_error(self, msg):
        self._icon.configure(text="!", text_color=NOTION_COLORS["error"])
        self._title.configure(text="Error")
        self._detail.configure(text=msg)
        self._open_btn.pack_forget()
        self.pack(fill="x", padx=20, pady=8)
        self._visible = True

    def hide(self):
        self.pack_forget()
        self._visible = False

    def _open_folder(self):
        path = os.path.dirname(self._cbz_path)
        os.startfile(path)


class MangaConvUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("MangaConv")
        self.geometry("1000x700")
        self.minsize(900, 600)

        self._pdf_files = []
        self._converting = False
        self._preview_timer = None

        self._setup_window()
        self._build_ui()

        self.bind("<Control-o>", lambda e: self._browse_files())
        self.bind("<Control-O>", lambda e: self._browse_files())

    def _setup_window(self):
        self.configure(fg_color=NOTION_COLORS["canvas"])

    def _build_ui(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.pack(fill="both", expand=True, padx=0, pady=0)

        self._build_header(main)
        self._build_body(main)
        self._build_footer(main)

    def _build_header(self, parent):
        header = ctk.CTkFrame(
            parent, fg_color=NOTION_COLORS["navy"],
            corner_radius=0, height=64
        )
        header.pack(fill="x")
        header.pack_propagate(False)

        inner = ctk.CTkFrame(header, fg_color="transparent")
        inner.pack(fill="both", padx=24)

        title_frame = ctk.CTkFrame(inner, fg_color="transparent")
        title_frame.pack(side="left")

        ctk.CTkLabel(
            title_frame, text="MangaConv",
            font=("Segoe UI", 20, "bold"),
            text_color=NOTION_COLORS["on_dark"]
        ).pack(side="left")

        tag = NotionTag(title_frame, text="Beta", color="purple")
        tag.pack(side="left", padx=(8, 0), pady=(4, 0))

        right_frame = ctk.CTkFrame(inner, fg_color="transparent")
        right_frame.pack(side="right")

        ctk.CTkLabel(
            right_frame, text="PDF \u2192 CBZ para PocketBook",
            font=FONTS["small"],
            text_color=NOTION_COLORS["on_dark_muted"]
        ).pack()

    def _build_body(self, parent):
        body = ctk.CTkFrame(parent, fg_color="transparent")
        body.pack(fill="both", expand=True, padx=24, pady=(16, 0))

        left_outer = ctk.CTkFrame(body, fg_color="transparent")
        left_outer.pack(side="left", fill="both", expand=False, padx=(0, 12))
        left_outer.configure(width=380)
        left_outer.pack_propagate(False)

        left = ctk.CTkScrollableFrame(left_outer, fg_color="transparent",
                                       corner_radius=0, scrollbar_button_color=NOTION_COLORS["hairline"],
                                       scrollbar_button_hover_color=NOTION_COLORS["muted_light"])
        left.pack(fill="both", expand=True)

        right = ctk.CTkFrame(body, fg_color="transparent")
        right.pack(side="right", fill="both", expand=True)

        self.drop_zone = DropZone(left, on_drop=self._on_files_dropped)
        self.drop_zone.pack(fill="x", pady=(0, 12))

        self.mode_selector = ModeSelector(left, on_change=self._on_mode_change)
        self.mode_selector.pack(fill="x", pady=(0, 12))

        self.settings_card = SettingsCard(left, on_settings_change=self._on_settings_change)
        self.settings_card.pack(fill="x", pady=(0, 12))

        self.file_info = FileInfoCard(left)
        self.file_info.pack(fill="x", pady=(0, 12))

        self.output_frame = ctk.CTkFrame(left, fg_color="transparent")
        self.output_frame.pack(fill="x", pady=(0, 12))

        ctk.CTkLabel(
            self.output_frame, text="Destino", font=FONTS["caption_bold"],
            text_color=NOTION_COLORS["steel"]
        ).pack(anchor="w")

        out_row = ctk.CTkFrame(self.output_frame, fg_color="transparent")
        out_row.pack(fill="x", pady=(4, 0))

        self.output_path = os.path.expanduser("~\\Downloads")
        self._output_label = ctk.CTkLabel(
            out_row, text=self.output_path,
            font=FONTS["small"], text_color=NOTION_COLORS["steel"],
            anchor="w"
        )
        self._output_label.pack(side="left", fill="x", expand=True)

        ctk.CTkButton(
            out_row, text="...", width=32, height=28,
            font=FONTS["body_bold"],
            fg_color=NOTION_COLORS["canvas"],
            text_color=NOTION_COLORS["charcoal"],
            hover_color=NOTION_COLORS["surface"],
            corner_radius=6, border_width=1,
            border_color=NOTION_COLORS["hairline"],
            command=self._browse_output
        ).pack(side="right", padx=(4, 0))

        self.result_card = ResultCard(left)

        self.preview = PreviewPanel(right)
        self.preview.pack(fill="both", expand=True)

    def _build_footer(self, parent):
        footer = ctk.CTkFrame(
            parent, fg_color=NOTION_COLORS["surface_soft"],
            corner_radius=0, height=60
        )
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)

        inner = ctk.CTkFrame(footer, fg_color="transparent")
        inner.pack(fill="both", padx=24, pady=8)

        self.progress = ctk.CTkProgressBar(
            inner, height=6, corner_radius=3,
            fg_color=NOTION_COLORS["hairline"],
            progress_color=NOTION_COLORS["primary"]
        )
        self.progress.pack(fill="x", pady=(0, 6))
        self.progress.set(0)

        row = ctk.CTkFrame(inner, fg_color="transparent")
        row.pack(fill="x")

        self.status_label = ctk.CTkLabel(
            row, text="Listo \u2014 arrastra un PDF para empezar",
            font=FONTS["small"], text_color=NOTION_COLORS["muted"],
            anchor="w"
        )
        self.status_label.pack(side="left")

        self.convert_btn = NotionButton(
            row, text="Convertir a CBZ", variant="primary",
            command=self._start_conversion
        )
        self.convert_btn.pack(side="right")

    def _on_files_dropped(self, paths):
        if not paths:
            return
        self._pdf_files = sorted(paths)
        self.result_card.hide()

        first = self._pdf_files[0]
        import fitz
        try:
            doc = fitz.open(first)
            pages = doc.page_count
            size = os.path.getsize(first)
            detected = detect_mode(first)
            doc.close()

            file_label = first if len(self._pdf_files) == 1 else f"{first} +{len(self._pdf_files)-1} m\u00e1s"
            res = self._get_resolution_str()
            self.file_info.set_info(file_label, pages, detected, res, size)
            self.mode_selector.set_mode("auto")
            total = len(self._pdf_files)
            files_text = f"{total} archivo" if total == 1 else f"{total} archivos"
            self.status_label.configure(
                text=f"{files_text} \u2014 1er: {pages} p\u00e1ginas \u2014 Modo: {detected}",
                text_color=NOTION_COLORS["charcoal"]
            )
            self.convert_btn.configure(state="normal",
                text=f"Convertir {total} a CBZ" if total > 1 else "Convertir a CBZ")

            self.preview.load_pdf(first)
        except Exception as e:
            self.file_info.reset()
            self.status_label.configure(
                text=f"Error al abrir: {e}",
                text_color=NOTION_COLORS["error"]
            )

    def _get_resolution_str(self):
        w, h = self.settings_card.get_settings()["target_w"], self.settings_card.get_settings()["target_h"]
        if w > 0 and h > 0:
            return f"{w}x{h}"
        return "Original"

    def _on_mode_change(self, mode):
        if self._pdf_files:
            labels = {
                "auto": "Auto (detecta autom\u00e1ticamente)",
                "manga": "Manga \u2014 p\u00e1ginas normales",
                "manhwa": "Manhwa \u2014 scroll infinito",
            }
            self.status_label.configure(text=labels.get(mode, mode))

    def _on_settings_change(self):
        if hasattr(self, "file_info"):
            res = self._get_resolution_str()
            self.file_info._info_labels["resolution"].configure(text=res)
        if not hasattr(self, "preview") or not self.preview.has_pages():
            return
        if self._preview_timer:
            self.after_cancel(self._preview_timer)
        self._preview_timer = self.after(100, self._do_update_preview)

    def _do_update_preview(self):
        try:
            settings = self.settings_card.get_settings()
            self.preview.refresh_processed(settings)
        except Exception as e:
            import traceback
            traceback.print_exc()
        self._preview_timer = None

    def _browse_files(self):
        paths = filedialog.askopenfilenames(
            title="Seleccionar PDFs",
            filetypes=[("Archivos PDF", "*.pdf")]
        )
        if paths:
            paths = sorted(paths)
            self.drop_zone.update_paths(paths)
            self._on_files_dropped(paths)

    def _browse_output(self):
        path = filedialog.askdirectory(
            title="Carpeta de destino",
            initialdir=self.output_path
        )
        if path:
            self.output_path = path
            self._output_label.configure(text=path)

    def _start_conversion(self):
        if not self._pdf_files or self._converting:
            return

        output_dir = filedialog.askdirectory(
            title="Seleccionar carpeta de destino para los CBZ",
            initialdir=self.output_path
        )
        if not output_dir:
            return
        self.output_path = output_dir
        self._output_label.configure(text=output_dir)

        self._converting = True
        total_files = len(self._pdf_files)
        self.convert_btn.configure(state="disabled", text=f"Convirtiendo 0/{total_files}...")
        self.status_label.configure(
            text="Convirtiendo...", text_color=NOTION_COLORS["charcoal"]
        )
        self.progress.set(0)
        self.result_card.hide()

        mode = self.mode_selector.get()
        settings = self.settings_card.get_settings()
        results = []

        def update_progress(current, total):
            self.after(0, lambda: self.progress.set(current / total))

        def done():
            self._converting = False
            self.convert_btn.configure(state="normal",
                text=f"Convertir {total_files} a CBZ" if total_files > 1 else "Convertir a CBZ")

        def run():
            try:
                for idx, pdf in enumerate(self._pdf_files):
                    self.after(0, lambda i=idx+1: self.convert_btn.configure(
                        text=f"Convirtiendo {i}/{total_files}..."))
                    self.after(0, lambda: self.status_label.configure(
                        text=f"Procesando {os.path.basename(pdf)}..."))
                    result = convert_pdf_to_cbz(
                        pdf, output_dir=output_dir, mode=mode,
                        settings=settings, on_progress=update_progress,
                    )
                    results.append(result)

                total_pages = sum(r["total_pages"] for r in results)
                total_images = sum(r["total_images"] for r in results)
                self.after(0, lambda: self.progress.set(1))
                self.after(0, lambda: self.status_label.configure(
                    text=f"\u00a1{total_files} archivos convertidos! {total_images} im\u00e1genes",
                    text_color=NOTION_COLORS["success"]
                ))
                last = results[-1]["cbz_path"]
                self.after(0, lambda: self.result_card.show_success(
                    last, total_pages, total_images
                ))
            except Exception as e:
                import traceback
                traceback.print_exc()
                self.after(0, lambda: self.status_label.configure(
                    text=f"Error: {e}", text_color=NOTION_COLORS["error"]
                ))
                self.after(0, lambda: self.result_card.show_error(str(e)))
            self.after(0, done)

        threading.Thread(target=run, daemon=True).start()
