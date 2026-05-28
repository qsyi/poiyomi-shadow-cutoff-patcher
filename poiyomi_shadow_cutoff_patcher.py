import os
import threading
import tkinter as tk
from tkinter import scrolledtext, font as tkfont, filedialog
from tkinterdnd2 import TkinterDnD, DND_FILES

PROPS_INSERT = (
    '\n'
    '\t\t//ifex _ShadowCasterCutoffEnabled==0 && isNotAnimated(_ShadowCasterCutoffEnabled)\n'
    '\t\t[HideInInspector] m_start_ShadowCasterCutoff (" Shadow Caster Cutoff--{reference_property:_ShadowCasterCutoffEnabled}", Float) = 0\n'
    '\t\t[ThryHideInInspector][ToggleUI] _ShadowCasterCutoffEnabled ("Enabled", Float) = 0\n'
    '\t\t_ShadowCasterCutoff ("Shadow Cutoff--{hover:Shadow pass alpha cutoff override. Set to 1 to prevent transparent surfaces from casting depth / being picked up by SSAO.}", Range(0, 1)) = 1\n'
    '\t\t[HideInInspector] m_end_ShadowCasterCutoff ("Shadow Caster Cutoff", Float) = 0\n'
    '\t\t//endex\n'
)

VARS_INSERT = (
    '\t\t\t//ifex _ShadowCasterCutoffEnabled==0 && isNotAnimated(_ShadowCasterCutoffEnabled)\n'
    '\t\t\tfloat _ShadowCasterCutoffEnabled;\n'
    '\t\t\tfloat _ShadowCasterCutoff;\n'
    '\t\t\t//endex\n'
)

CLIP_NEW = (
    '\t\t\t\t//ifex _ShadowCasterCutoffEnabled==0 && isNotAnimated(_ShadowCasterCutoffEnabled)\n'
    '\t\t\t\tUNITY_BRANCH\n'
    '\t\t\t\tif (_ShadowCasterCutoffEnabled)\n'
    '\t\t\t\t\tclip(poiFragData.alpha - _ShadowCasterCutoff);\n'
    '\t\t\t\telse\n'
    '\t\t\t\t\tclip(poiFragData.alpha - _Cutoff);\n'
    '\t\t\t\t//endex\n'
    '\t\t\t\t//ifex !(isNotAnimated(_ShadowCasterCutoffEnabled) && _ShadowCasterCutoffEnabled==0)\n'
    '\t\t\t\tclip(poiFragData.alpha - _Cutoff);\n'
    '\t\t\t\t//endex\n'
)


def already_patched(lines):
    return any('_ShadowCasterCutoffEnabled' in l for l in lines)


def find_props_insert_line(lines):
    for i, l in enumerate(lines):
        if 'm_end_StencilPassOptions' in l:
            return i
    raise RuntimeError("Properties の挿入ポイントが見つかりませんでした (m_end_StencilPassOptions)")


def find_shadow_pass_start(lines):
    for i, l in enumerate(lines):
        if '#define POI_PASS_SHADOW' in l:
            return i
    raise RuntimeError("#define POI_PASS_SHADOW が見つかりませんでした")


def find_vars_insert_line(lines, shadow_start):
    for i in range(shadow_start, len(lines)):
        if lines[i].strip() == 'float _Cutoff;':
            return i
    raise RuntimeError("ShadowCaster pass 内の float _Cutoff; が見つかりませんでした")


def find_clip_line(lines, shadow_start):
    for i in range(shadow_start, len(lines)):
        if 'clip(poiFragData.alpha - _Cutoff);' in lines[i]:
            return i
    raise RuntimeError("ShadowCaster pass 内の clip(poiFragData.alpha - _Cutoff); が見つかりませんでした")


def patch(shader_path, log):
    log(f"対象: {shader_path}")

    if not os.path.isfile(shader_path):
        raise FileNotFoundError(f"ファイルが見つかりません: {shader_path}")

    with open(shader_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    log(f"  行数: {len(lines)}")

    if already_patched(lines):
        log("  既にパッチ適用済みです。処理を中断します。")
        return

    props_idx    = find_props_insert_line(lines)
    shadow_start = find_shadow_pass_start(lines)
    vars_idx     = find_vars_insert_line(lines, shadow_start)
    clip_idx     = find_clip_line(lines, shadow_start)

    if not (props_idx < vars_idx < clip_idx):
        raise RuntimeError(
            "挿入ポイントの順序が不正です（バージョン非対応の可能性があります）\n"
            f"  Props={props_idx+1}, Vars={vars_idx+1}, Clip={clip_idx+1}"
        )

    log(f"  挿入ポイント: Properties={props_idx+1}, Variables={vars_idx+1}, Clip={clip_idx+1}")

    lines[clip_idx] = CLIP_NEW
    lines.insert(vars_idx + 1, VARS_INSERT)
    lines.insert(props_idx + 1, PROPS_INSERT)

    with open(shader_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)

    log("  パッチ適用完了!")
    log("  Unity でマテリアルを開くと Rendering Options に")
    log("  'Shadow Caster Cutoff' セクションが表示されます。")


HINT_TEXT = (
    "Poiyomi Pro.shader をドロップ またはクリックして選択\n\n"
    "シェーダーの場所 (どちらか):\n"
    "Assets\\_PoiyomiShaders\\Shaders\\10.0\\Pro\\Poiyomi Pro.shader\n"
    "Packages\\com.poiyomi.pro\\_PoiyomiShaders\\Shaders\\10.0\\Pro\\Poiyomi Pro.shader"
)


class App(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("Poiyomi Shadow Cutoff Patcher")
        self.geometry("720x360")
        self.resizable(False, False)
        self.configure(bg="#1e1e1e")
        self.lift()

        drop_font = tkfont.Font(family="Arial", size=11)
        self.drop_label = tk.Label(
            self,
            text=HINT_TEXT,
            bg="#2d2d2d", fg="#cccccc",
            font=drop_font,
            relief="flat",
            cursor="hand2",
        )
        self.drop_label.pack(fill=tk.BOTH, expand=True, padx=12, pady=(12, 6))

        self.log_box = scrolledtext.ScrolledText(
            self, height=7, bg="#1a1a1a", fg="#aaffaa",
            font=("Consolas", 9), relief="flat",
            state=tk.DISABLED,
        )
        self.log_box.pack(fill=tk.X, padx=12, pady=(0, 12))

        self.drop_label.drop_target_register(DND_FILES)
        self.drop_label.dnd_bind('<<Drop>>', self._on_drop)
        self.drop_label.bind('<Button-1>', self._on_click)

    def _log(self, msg):
        self.log_box.configure(state=tk.NORMAL)
        self.log_box.insert(tk.END, msg + "\n")
        self.log_box.see(tk.END)
        self.log_box.configure(state=tk.DISABLED)

    def _log_separator(self):
        self.log_box.configure(state=tk.NORMAL)
        self.log_box.insert(tk.END, "─" * 40 + "\n")
        self.log_box.see(tk.END)
        self.log_box.configure(state=tk.DISABLED)

    def _reset_label(self):
        self.drop_label.configure(text=HINT_TEXT)

    def _on_click(self, event):
        path = filedialog.askopenfilename(
            title="Poiyomi Pro.shader を選択",
            filetypes=[("Shader files", "*.shader"), ("All files", "*.*")],
        )
        if path:
            self._start(path)

    def _on_drop(self, event):
        raw = event.data.strip()
        if ' ' in raw and not raw.startswith('{'):
            self._log("複数ファイルのドロップには対応していません。1ファイルずつ処理してください。")
            return
        if raw.startswith('{') and raw.endswith('}'):
            path = raw[1:-1]
        else:
            path = raw
        if not path.lower().endswith('.shader'):
            self._log(f"スキップ: .shader ファイルをドロップしてください ({path})")
            return
        self._start(path)

    def _start(self, path):
        self._log_separator()
        self.drop_label.configure(text="処理中...")
        threading.Thread(target=self._run, args=(path,), daemon=True).start()

    def _run(self, path):
        try:
            patch(path, self._log)
            self.after(0, lambda: self.drop_label.configure(text="完了!"))
        except Exception as e:
            self._log(f"エラー: {e}")
            self.after(0, lambda: self.drop_label.configure(text="エラーが発生しました\nログを確認してください"))
        self.after(2000, self._reset_label)


if __name__ == '__main__':
    app = App()
    app.mainloop()
