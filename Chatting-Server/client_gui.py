"""
PyChat Client — End-to-End Encrypted Private Messages
======================================================
DMs are encrypted with RSA-OAEP before leaving this device.
The server only forwards opaque ciphertext and cannot read DMs.

Requires: pip install cryptography
"""

import socket
import threading
import base64
import tkinter as tk
from tkinter import scrolledtext, font, simpledialog, messagebox
from datetime import datetime
from collections import defaultdict

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend

HOST = "127.0.0.1"
PORT = 55555
EVERYONE = "Everyone 📢"


def generate_keypair():
    """Generate a fresh RSA-2048 key pair."""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    return private_key, private_key.public_key()


def pubkey_to_b64(public_key) -> str:
    """Serialize public key to base64 PEM string for transmission."""
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return base64.b64encode(pem).decode()


def b64_to_pubkey(b64: str):
    """Deserialize a received base64 public key."""
    pem = base64.b64decode(b64.encode())
    return serialization.load_pem_public_key(pem, backend=default_backend())


def encrypt_message(public_key, plaintext: str) -> str:
    """Encrypt a message with recipient's public key → base64 ciphertext."""
    ciphertext = public_key.encrypt(
        plaintext.encode("utf-8"),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(ciphertext).decode()


def decrypt_message(private_key, b64_ciphertext: str) -> str:
    """Decrypt a received ciphertext with own private key."""
    ciphertext = base64.b64decode(b64_ciphertext.encode())
    plaintext = private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return plaintext.decode("utf-8")


class ClientApp:
    BG      = "#0f0f13"
    PANEL   = "#1a1a24"
    PANEL2  = "#14141e"
    ACCENT  = "#7c6af7"
    ACCENT2 = "#f76a8c"
    TEXT    = "#e8e6f0"
    MUTED   = "#5a5870"
    GREEN   = "#4dffb0"
    RED     = "#ff6b6b"
    YELLOW  = "#fbbf24"
    BORDER  = "#2a2a3a"
    SELF_C  = "#a78bfa"
    DM_C    = "#f9a8d4"

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("PyChat")
        self.root.configure(bg=self.BG)
        self.root.geometry("840x640")
        self.root.minsize(600, 460)

        # Crypto setup
        self.root.title("PyChat — generating keys…")
        self.private_key, self.public_key = generate_keypair()
        self.my_pubkey_b64 = pubkey_to_b64(self.public_key)
        self.peer_pubkeys: dict[str, object] = {}    # nick → public_key object
        self.pending_msgs: dict[str, list[str]] = defaultdict(list)  # nick → queued msgs waiting for key

        # State
        self.sock = None
        self.connected = False
        self.nickname = ""
        self.active_chat = EVERYONE
        self.histories: dict[str, list] = defaultdict(list)
        self.unread: dict[str, int] = defaultdict(int)
        self._online_nicks: list[str] = []

        self._build_ui()
        self.root.title("PyChat")

    # ── UI ───────────────────────────────────────────────────────────────────
    def _build_ui(self):
        tf = font.Font(family="Courier New", size=18, weight="bold")
        lf = font.Font(family="Courier New", size=10, weight="bold")
        mf = font.Font(family="Courier New", size=10)
        sf = font.Font(family="Courier New", size=9)
        self._mf = mf; self._lf = lf

        # Header
        hdr = tk.Frame(self.root, bg=self.PANEL, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="◈  PyChat", font=tf, bg=self.PANEL, fg=self.ACCENT2).pack(side="left", padx=20)
        tk.Label(hdr, text="🔒 E2E Encrypted DMs", font=sf, bg=self.PANEL, fg=self.YELLOW).pack(side="left", padx=4)
        self.status_lbl = tk.Label(hdr, text="● DISCONNECTED", font=lf, bg=self.PANEL, fg=self.RED)
        self.status_lbl.pack(side="right", padx=20)
        self.nick_badge = tk.Label(hdr, text="", font=lf, bg=self.PANEL, fg=self.GREEN)
        self.nick_badge.pack(side="right", padx=10)

        # Connection bar
        bar = tk.Frame(self.root, bg=self.BG, pady=10)
        bar.pack(fill="x", padx=20)
        tk.Label(bar, text="HOST", font=sf, bg=self.BG, fg=self.MUTED).pack(side="left")
        self.host_var = tk.StringVar(value=HOST)
        tk.Entry(bar, textvariable=self.host_var, width=14, bg=self.PANEL, fg=self.TEXT,
                 insertbackground=self.TEXT, relief="flat", font=mf, bd=0
                 ).pack(side="left", padx=(4, 14), ipady=4)
        tk.Label(bar, text="PORT", font=sf, bg=self.BG, fg=self.MUTED).pack(side="left")
        self.port_var = tk.StringVar(value=str(PORT))
        tk.Entry(bar, textvariable=self.port_var, width=7, bg=self.PANEL, fg=self.TEXT,
                 insertbackground=self.TEXT, relief="flat", font=mf, bd=0
                 ).pack(side="left", padx=(4, 20), ipady=4)
        self.conn_btn = tk.Button(bar, text="⚡  CONNECT", font=lf,
            bg=self.ACCENT, fg="#fff", relief="flat", cursor="hand2",
            padx=16, pady=6, command=self.toggle_connect)
        self.conn_btn.pack(side="left")

        # Main area
        main = tk.Frame(self.root, bg=self.BG)
        main.pack(fill="both", expand=True, padx=20, pady=(0, 0))

        # Sidebar
        sidebar = tk.Frame(main, bg=self.BG, width=180)
        sidebar.pack(side="left", fill="y", padx=(0, 14))
        sidebar.pack_propagate(False)
        tk.Label(sidebar, text="CONVERSATIONS", font=sf, bg=self.BG, fg=self.MUTED).pack(anchor="w", pady=(0, 4))
        self.conv_lb = tk.Listbox(sidebar, bg=self.PANEL, fg=self.TEXT, font=mf,
            relief="flat", bd=0, selectbackground=self.ACCENT,
            selectforeground="#fff", activestyle="none")
        self.conv_lb.pack(fill="both", expand=True)
        self.conv_lb.bind("<<ListboxSelect>>", self._on_conv_select)

        # Chat area
        chat_area = tk.Frame(main, bg=self.BG)
        chat_area.pack(side="left", fill="both", expand=True)
        self.chat_title = tk.Label(chat_area, text="Select a conversation",
            font=lf, bg=self.PANEL2, fg=self.ACCENT, anchor="w", padx=12, pady=8)
        self.chat_title.pack(fill="x")
        self.enc_badge = tk.Label(chat_area, text="",
            font=sf, bg=self.PANEL2, fg=self.YELLOW, anchor="e", padx=12, pady=0)
        self.enc_badge.pack(fill="x")

        self.chat = scrolledtext.ScrolledText(chat_area, bg=self.PANEL, fg=self.TEXT,
            font=mf, relief="flat", bd=0, state="disabled", wrap="word", padx=12, pady=10)
        self.chat.pack(fill="both", expand=True)
        for tag, clr in [("ts", self.MUTED), ("self", self.SELF_C), ("other", self.TEXT),
                         ("dm_in", self.DM_C), ("sys", self.ACCENT),
                         ("err", self.RED), ("info", self.YELLOW)]:
            self.chat.tag_config(tag, foreground=clr)

        # Input bar
        in_frame = tk.Frame(self.root, bg=self.BG, pady=12)
        in_frame.pack(fill="x", padx=20)
        self.msg_entry = tk.Entry(in_frame, bg=self.PANEL, fg=self.MUTED,
            insertbackground=self.TEXT, relief="flat", font=mf, bd=0, state="disabled")
        self.msg_entry.insert(0, "Connect to start chatting...")
        self.msg_entry.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 10))
        self.msg_entry.bind("<Return>", self.send_message)
        self.send_btn = tk.Button(in_frame, text="SEND ▶", font=lf,
            bg=self.ACCENT2, fg="#fff", relief="flat", cursor="hand2",
            padx=14, pady=7, state="disabled", command=self.send_message)
        self.send_btn.pack(side="right")

        self._rebuild_sidebar([])

    # ── Sidebar ──────────────────────────────────────────────────────────────
    def _rebuild_sidebar(self, online_nicks: list):
        self.conv_lb.delete(0, "end")
        badge_e = f" {EVERYONE}"
        if self.unread.get(EVERYONE, 0):
            badge_e += f"  ({self.unread[EVERYONE]})"
        self.conv_lb.insert("end", badge_e)
        self.conv_lb.itemconfig(0, fg=self.ACCENT)

        for nick in online_nicks:
            if nick == self.nickname:
                continue
            has_key = "🔒" if nick in self.peer_pubkeys else "  "
            label = f" {has_key} {nick}"
            if self.unread.get(nick, 0):
                label += "  ●"
            self.conv_lb.insert("end", label)

        self._highlight_active()

    def _highlight_active(self):
        for i in range(self.conv_lb.size()):
            raw = self.conv_lb.get(i)
            # Extract nick: strip lock icon and badges
            name = raw.strip().replace("🔒", "").replace("●", "").strip()
            # Remove unread count like "(3)"
            if "  (" in name:
                name = name[:name.index("  (")].strip()
            if name == self.active_chat or (name == EVERYONE and self.active_chat == EVERYONE):
                self.conv_lb.selection_clear(0, "end")
                self.conv_lb.selection_set(i)
                self.conv_lb.see(i)
                break

    def _on_conv_select(self, _):
        sel = self.conv_lb.curselection()
        if not sel: return
        raw = self.conv_lb.get(sel[0]).strip().replace("🔒", "").replace("●", "").strip()
        if "  (" in raw:
            raw = raw[:raw.index("  (")].strip()
        name = raw.strip()
        if not name: return
        self.active_chat = name
        self.unread[name] = 0
        self._rebuild_sidebar(self._online_nicks)
        self._load_history(name)

        if name == EVERYONE:
            self.chat_title.config(text="  📢 Everyone — Broadcast")
            self.enc_badge.config(text="")
        else:
            self.chat_title.config(text=f"  🔒 Private chat with {name}")
            if name in self.peer_pubkeys:
                self.enc_badge.config(text="✓ End-to-end encrypted — server cannot read this conversation")
            else:
                self.enc_badge.config(text="⏳ Fetching encryption key…")
                if self.connected:
                    self._request_key(name)

        self.msg_entry.config(state="normal" if self.connected else "disabled")
        if self.connected:
            self.msg_entry.focus()

    # ── Chat display ─────────────────────────────────────────────────────────
    def _append(self, conv: str, text: str, tag: str):
        ts = datetime.now().strftime("%H:%M")
        entry = (tag, f"[{ts}] {text}")
        self.histories[conv].append(entry)
        if conv == self.active_chat:
            self._write_line(tag, f"[{ts}] {text}")

    def _write_line(self, tag: str, text: str):
        self.chat.config(state="normal")
        self.chat.insert("end", text + "\n", tag)
        self.chat.config(state="disabled")
        self.chat.see("end")

    def _load_history(self, conv: str):
        self.chat.config(state="normal")
        self.chat.delete("1.0", "end")
        self.chat.config(state="disabled")
        for tag, text in self.histories[conv]:
            self._write_line(tag, text)

    def _mark_unread(self, conv: str):
        if conv != self.active_chat:
            self.unread[conv] += 1
            self._rebuild_sidebar(self._online_nicks)

    # ── Key exchange ─────────────────────────────────────────────────────────
    def _request_key(self, nick: str):
        """Ask the server for nick's public key."""
        if not self.connected or not self.sock: return
        try:
            self.sock.send(f"GETKEY:{nick}".encode())
        except OSError:
            pass

    def _store_peer_key(self, nick: str, b64key: str):
        """Store a received public key and flush any pending messages."""
        try:
            self.peer_pubkeys[nick] = b64_to_pubkey(b64key)
        except Exception:
            return
        self._append(EVERYONE, f"🔑 Key received for {nick} — DMs are now encrypted", "info")
        # Update enc badge if this is the active chat
        if self.active_chat == nick:
            self.enc_badge.config(text="✓ End-to-end encrypted — server cannot read this conversation")
        # Flush pending messages
        self._rebuild_sidebar(self._online_nicks)
        if nick in self.pending_msgs:
            for msg in self.pending_msgs.pop(nick):
                self._send_dm(nick, msg)

    # ── Connection ───────────────────────────────────────────────────────────
    def toggle_connect(self):
        (self._connect if not self.connected else self._disconnect)()

    def _connect(self):
        host = self.host_var.get().strip()
        try:
            port = int(self.port_var.get().strip())
        except ValueError:
            messagebox.showerror("Error", "Invalid port."); return

        nick = simpledialog.askstring("Nickname", "Enter your nickname:", parent=self.root)
        if not nick or not nick.strip(): return
        self.nickname = nick.strip()

        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((host, port))
        except ConnectionRefusedError:
            messagebox.showerror("Error", f"Cannot connect to {host}:{port}\nIs the server running?")
            return

        # Nickname handshake
        prompt = self.sock.recv(1024).decode()
        if prompt == "NICK":
            self.sock.send(self.nickname.encode())

        # Register our public key with the server
        self.sock.send(f"MYPUBKEY:{self.my_pubkey_b64}".encode())

        self.connected = True
        self._online_nicks = []
        self.root.title(f"PyChat — {self.nickname}")
        self.status_lbl.config(text="● CONNECTED", fg=self.GREEN)
        self.nick_badge.config(text=f"  {self.nickname}")
        self.conn_btn.config(text="✕  DISCONNECT", bg=self.RED)
        self.msg_entry.config(state="normal")
        self.msg_entry.delete(0, "end")
        self.send_btn.config(state="normal")

        threading.Thread(target=self._recv_loop, daemon=True).start()

    def _disconnect(self, reason=None):
        self.connected = False
        if self.sock:
            try:
                self.sock.send("/quit".encode())
                self.sock.close()
            except: pass
            self.sock = None
        self.root.after(0, self._ui_disconnected)
        if reason:
            self.root.after(0, lambda: self._append(self.active_chat, reason, "err"))

    def _ui_disconnected(self):
        self.status_lbl.config(text="● DISCONNECTED", fg=self.RED)
        self.nick_badge.config(text="")
        self.conn_btn.config(text="⚡  CONNECT", bg=self.ACCENT)
        self.msg_entry.config(state="disabled")
        self.msg_entry.delete(0, "end")
        self.msg_entry.insert(0, "Connect to start chatting...")
        self.msg_entry.config(fg=self.MUTED)
        self.send_btn.config(state="disabled")
        self.root.title("PyChat")

    # ── Receive ──────────────────────────────────────────────────────────────
    def _recv_loop(self):
        while self.connected:
            try:
                raw = self.sock.recv(65536).decode("utf-8", errors="replace")
                if not raw:
                    self._disconnect("Server closed the connection."); break
                self.root.after(0, lambda r=raw: self._process(r))
            except OSError:
                if self.connected:
                    self._disconnect("Connection lost.")
                break

    def _process(self, raw: str):
        # User list update
        if raw.startswith("USERS:"):
            nicks = [n for n in raw[6:].split(",") if n and n != self.nickname]
            self._online_nicks = nicks
            self._rebuild_sidebar(nicks)

        # Incoming public key
        elif raw.startswith("PUBKEY:"):
            parts = raw[7:].split(":", 1)
            if len(parts) == 2:
                nick, b64key = parts
                self._store_peer_key(nick, b64key)

        # Encrypted DM — decrypt with our private key
        elif raw.startswith("DM:"):
            parts = raw[3:].split(":", 1)
            if len(parts) == 2:
                frm, b64_cipher = parts
                try:
                    plaintext = decrypt_message(self.private_key, b64_cipher)
                    self._append(frm, f"[{frm}] {plaintext}", "dm_in")
                    self._mark_unread(frm)
                except Exception:
                    self._append(frm, f"[{frm}] [Could not decrypt message]", "err")
                    self._mark_unread(frm)

        # Broadcast message
        elif raw.startswith("MSG:"):
            parts = raw[4:].split(":", 1)
            if len(parts) == 2:
                frm, msg = parts
                self._append(EVERYONE, f"[{frm}] {msg}", "other")
                self._mark_unread(EVERYONE)

        # System message
        elif raw.startswith("SYS:"):
            msg = raw[4:]
            self._append(EVERYONE, f"⚙  {msg}", "sys")
            self._mark_unread(EVERYONE)

    # ── Send ─────────────────────────────────────────────────────────────────
    def send_message(self, _=None):
        if not self.connected: return
        msg = self.msg_entry.get().strip()
        if not msg: return
        self.msg_entry.delete(0, "end")

        if self.active_chat == EVERYONE:
            try:
                self.sock.send(f"MSG:{msg}".encode())
                self._append(EVERYONE, f"[You] {msg}", "self")
            except OSError:
                self._disconnect("Send failed.")
        else:
            self._send_dm(self.active_chat, msg)

        if msg.lower() == "/quit":
            self._disconnect()

    def _send_dm(self, to: str, msg: str):
        """Encrypt and send a DM. If we don't have their key yet, queue it."""
        if to not in self.peer_pubkeys:
            self.pending_msgs[to].append(msg)
            self._append(to, f"⏳ Fetching {to}'s key, message queued…", "info")
            self._request_key(to)
            return
        try:
            ciphertext = encrypt_message(self.peer_pubkeys[to], msg)
            self.sock.send(f"DM:{to}:{ciphertext}".encode())
            self._append(to, f"[You → {to}] {msg}", "self")
        except Exception as e:
            self._append(to, f"[Encrypt error: {e}]", "err")


if __name__ == "__main__":
    root = tk.Tk()
    ClientApp(root)
    root.mainloop()