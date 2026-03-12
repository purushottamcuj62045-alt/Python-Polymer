"""
PyChat Server — End-to-End Encrypted Private Messages
======================================================
The server CANNOT read DM content. It only routes opaque ciphertext.

Protocol:
  Client → Server:
      NICK:<nickname>             — set nickname
      MYPUBKEY:<b64_pubkey>       — register RSA public key
      GETKEY:<nick>               — request someone's public key
      DM:<to>:<b64_ciphertext>    — send encrypted private message
      MSG:<text>                  — send plaintext broadcast
      /quit                       — disconnect

  Server → Client:
      NICK                        — ask for nickname
      PUBKEY:<nick>:<b64_pubkey>  — deliver requested public key
      USERS:<n1>,<n2>,...         — updated online user list
      DM:<from>:<b64_ciphertext>  — forwarded encrypted DM (server can't read)
      MSG:<from>:<text>           — broadcast message
      SYS:<text>                  — system notification
"""

import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, font
from datetime import datetime

HOST = "127.0.0.1"
PORT = 55555

clients: dict[str, socket.socket] = {}   # nick → socket
pubkeys: dict[str, str] = {}             # nick → base64 public key
lock = threading.Lock()


class ServerApp:
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

    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("PyChat — Server")
        self.root.configure(bg=self.BG)
        self.root.geometry("860x640")
        self.root.minsize(640, 480)
        self.server_socket = None
        self.running = False
        self._build_ui()

    # ── UI ──────────────────────────────────────────────────────────────────
    def _build_ui(self):
        tf = font.Font(family="Courier New", size=18, weight="bold")
        lf = font.Font(family="Courier New", size=10, weight="bold")
        mf = font.Font(family="Courier New", size=10)
        sf = font.Font(family="Courier New", size=9)

        # Header
        hdr = tk.Frame(self.root, bg=self.PANEL, pady=14)
        hdr.pack(fill="x")
        tk.Label(hdr, text="⬡  PyChat Server", font=tf,
                 bg=self.PANEL, fg=self.ACCENT).pack(side="left", padx=20)
        # E2E badge
        tk.Label(hdr, text="🔒 E2E ENCRYPTED DMs", font=sf,
                 bg=self.PANEL, fg=self.YELLOW).pack(side="left", padx=10)
        self.status_lbl = tk.Label(hdr, text="● OFFLINE", font=lf,
                                   bg=self.PANEL, fg=self.RED)
        self.status_lbl.pack(side="right", padx=20)

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

        self.toggle_btn = tk.Button(bar, text="▶  START SERVER", font=lf,
            bg=self.ACCENT, fg="#fff", relief="flat", cursor="hand2",
            padx=16, pady=6, command=self.toggle_server)
        self.toggle_btn.pack(side="left")
        self.kick_btn = tk.Button(bar, text="✕  KICK", font=lf,
            bg=self.BORDER, fg=self.MUTED, relief="flat", cursor="hand2",
            padx=12, pady=6, command=self.kick_selected, state="disabled")
        self.kick_btn.pack(side="left", padx=(10, 0))

        # Main panes
        panes = tk.Frame(self.root, bg=self.BG)
        panes.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        # Log
        lf2 = tk.Frame(panes, bg=self.BG)
        lf2.pack(side="left", fill="both", expand=True)
        tk.Label(lf2, text="SERVER LOG", font=sf, bg=self.BG, fg=self.MUTED).pack(anchor="w", pady=(0, 4))
        self.log = scrolledtext.ScrolledText(lf2, bg=self.PANEL, fg=self.TEXT,
            font=mf, relief="flat", bd=0, state="disabled", wrap="word", padx=10, pady=10)
        self.log.pack(fill="both", expand=True)
        for tag, clr in [("ts", self.MUTED), ("join", self.GREEN), ("leave", self.RED),
                         ("msg", self.TEXT), ("dm", self.YELLOW),
                         ("key", "#60a5fa"), ("sys", self.ACCENT)]:
            self.log.tag_config(tag, foreground=clr)

        # Online list
        right = tk.Frame(panes, bg=self.BG, width=190)
        right.pack(side="right", fill="y", padx=(14, 0))
        right.pack_propagate(False)
        tk.Label(right, text="ONLINE", font=sf, bg=self.BG, fg=self.MUTED).pack(anchor="w", pady=(0, 4))
        self.client_lb = tk.Listbox(right, bg=self.PANEL, fg=self.GREEN, font=mf,
            relief="flat", bd=0, selectbackground=self.ACCENT,
            selectforeground="#fff", activestyle="none")
        self.client_lb.pack(fill="both", expand=True)
        self.client_lb.bind("<<ListboxSelect>>", self._on_select)

        # Broadcast bar
        bc = tk.Frame(self.root, bg=self.BG)
        bc.pack(fill="x", padx=20, pady=(0, 14))
        self.bc_entry = tk.Entry(bc, bg=self.PANEL, fg=self.MUTED,
            insertbackground=self.TEXT, relief="flat", font=mf, bd=0)
        self.bc_entry.insert(0, "Broadcast to all clients...")
        self.bc_entry.bind("<FocusIn>",  lambda e: self._ph(True))
        self.bc_entry.bind("<FocusOut>", lambda e: self._ph(False))
        self.bc_entry.bind("<Return>", self.broadcast_message)
        self.bc_entry.pack(side="left", fill="x", expand=True, ipady=7, padx=(0, 10))
        tk.Button(bc, text="BROADCAST", font=lf, bg=self.ACCENT2, fg="#fff",
            relief="flat", cursor="hand2", padx=12, pady=6,
            command=self.broadcast_message).pack(side="right")

    def _ph(self, focused):
        ph = "Broadcast to all clients..."
        if focused and self.bc_entry.get() == ph:
            self.bc_entry.delete(0, "end"); self.bc_entry.config(fg=self.TEXT)
        elif not focused and not self.bc_entry.get():
            self.bc_entry.insert(0, ph); self.bc_entry.config(fg=self.MUTED)

    def _on_select(self, _):
        sel = self.client_lb.curselection()
        self.kick_btn.config(
            state="normal" if sel else "disabled",
            bg=self.ACCENT2 if sel else self.BORDER,
            fg="#fff" if sel else self.MUTED)

    def log_msg(self, text, tag="msg"):
        ts = datetime.now().strftime("%H:%M:%S")
        self.log.config(state="normal")
        self.log.insert("end", f"[{ts}] ", "ts")
        self.log.insert("end", text + "\n", tag)
        self.log.config(state="disabled")
        self.log.see("end")

    # ── Client list ─────────────────────────────────────────────────────────
    def refresh_clients(self):
        self.client_lb.delete(0, "end")
        with lock:
            for nick in clients:
                has_key = "🔑" if nick in pubkeys else "  "
                self.client_lb.insert("end", f" {has_key} {nick}")
        self._push_user_list()

    def _push_user_list(self):
        with lock:
            nicks = list(clients.keys())
            msg = "USERS:" + ",".join(nicks)
            for sock in clients.values():
                try: sock.send(msg.encode())
                except: pass

    # ── Server control ───────────────────────────────────────────────────────
    def toggle_server(self):
        (self._start if not self.running else self._stop)()

    def _start(self):
        host = self.host_var.get().strip()
        try:
            port = int(self.port_var.get().strip())
        except ValueError:
            self.log_msg("Invalid port.", "leave"); return
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((host, port))
            self.server_socket.listen()
        except OSError as e:
            self.log_msg(f"Error: {e}", "leave"); return
        self.running = True
        self.status_lbl.config(text="● ONLINE", fg=self.GREEN)
        self.toggle_btn.config(text="■  STOP SERVER", bg=self.RED)
        self.log_msg(f"Server started on {host}:{port}", "sys")
        threading.Thread(target=self._accept_loop, daemon=True).start()

    def _stop(self):
        self.running = False
        if self.server_socket:
            try: self.server_socket.close()
            except: pass
        with lock:
            for s in clients.values():
                try: s.close()
                except: pass
            clients.clear()
            pubkeys.clear()
        self.root.after(0, self.refresh_clients)
        self.status_lbl.config(text="● OFFLINE", fg=self.RED)
        self.toggle_btn.config(text="▶  START SERVER", bg=self.ACCENT)
        self.log_msg("Server stopped.", "sys")

    def _accept_loop(self):
        while self.running:
            try:
                sock, addr = self.server_socket.accept()
                threading.Thread(target=self._handle, args=(sock, addr), daemon=True).start()
            except OSError:
                break

    # ── Per-client handler ───────────────────────────────────────────────────
    def _handle(self, sock: socket.socket, addr):
        # Step 1: ask for nickname
        try:
            sock.send("NICK".encode())
            nick = sock.recv(4096).decode().strip() or "Anonymous"
        except OSError:
            sock.close(); return

        # Ensure unique nick
        with lock:
            base, i = nick, 1
            while nick in clients:
                nick = f"{base}_{i}"; i += 1
            clients[nick] = sock

        self.root.after(0, self.refresh_clients)
        self.root.after(0, lambda: self.log_msg(f"{nick} joined from {addr[0]}", "join"))
        sock.send(f"SYS:Welcome {nick}! DMs are end-to-end encrypted 🔒".encode())
        self._sys_all(f"{nick} joined.", exclude=nick)

        # Main message loop
        while True:
            try:
                raw = sock.recv(65536).decode("utf-8", errors="replace")
                if not raw or raw.strip() == "/quit":
                    break

                # ── Register public key ──────────────────────────────────
                if raw.startswith("MYPUBKEY:"):
                    b64key = raw[9:]
                    with lock:
                        pubkeys[nick] = b64key
                    self.root.after(0, lambda n=nick: self.log_msg(
                        f"🔑 {n} registered public key", "key"))
                    self.root.after(0, self.refresh_clients)

                # ── Key request ──────────────────────────────────────────
                elif raw.startswith("GETKEY:"):
                    target_nick = raw[7:].strip()
                    with lock:
                        key = pubkeys.get(target_nick)
                    if key:
                        try:
                            sock.send(f"PUBKEY:{target_nick}:{key}".encode())
                        except OSError:
                            pass
                    else:
                        try:
                            sock.send(f"SYS:No key found for '{target_nick}'.".encode())
                        except OSError:
                            pass

                # ── Encrypted DM — server routes but CANNOT read ─────────
                elif raw.startswith("DM:"):
                    parts = raw[3:].split(":", 1)
                    if len(parts) == 2:
                        to, ciphertext = parts[0].strip(), parts[1].strip()
                        self._route_dm(nick, to, ciphertext)

                # ── Plaintext broadcast ──────────────────────────────────
                elif raw.startswith("MSG:"):
                    msg = raw[4:]
                    self.root.after(0, lambda m=f"[{nick}→ALL] {msg}": self.log_msg(m, "msg"))
                    self._broadcast_msg(nick, msg)

            except OSError:
                break

        # Cleanup
        with lock:
            clients.pop(nick, None)
            pubkeys.pop(nick, None)
        try: sock.close()
        except: pass
        self.root.after(0, self.refresh_clients)
        self.root.after(0, lambda: self.log_msg(f"{nick} disconnected.", "leave"))
        self._sys_all(f"{nick} left the chat.")

    # ── Routing ──────────────────────────────────────────────────────────────
    def _route_dm(self, frm: str, to: str, ciphertext: str):
        """Forward encrypted DM — server sees only opaque base64, not the message."""
        with lock:
            target_sock = clients.get(to)
            sender_sock = clients.get(frm)
        if target_sock:
            try:
                target_sock.send(f"DM:{frm}:{ciphertext}".encode())
            except OSError:
                pass
            # Server log shows ENCRYPTED placeholder — cannot read content
            self.root.after(0, lambda: self.log_msg(
                f"🔒 [DM] {frm} → {to}: [ENCRYPTED — server cannot read]", "dm"))
        else:
            if sender_sock:
                try:
                    sender_sock.send(f"SYS:'{to}' is offline or not found.".encode())
                except OSError:
                    pass

    def _broadcast_msg(self, frm: str, msg: str):
        with lock:
            targets = [(n, s) for n, s in clients.items() if n != frm]
        for _, sock in targets:
            try: sock.send(f"MSG:{frm}:{msg}".encode())
            except: pass

    def _sys_all(self, msg: str, exclude: str = None):
        with lock:
            targets = [(n, s) for n, s in clients.items() if n != exclude]
        for _, sock in targets:
            try: sock.send(f"SYS:{msg}".encode())
            except: pass

    # ── UI actions ───────────────────────────────────────────────────────────
    def broadcast_message(self, _=None):
        msg = self.bc_entry.get().strip()
        if not msg or msg == "Broadcast to all clients...": return
        self._sys_all(f"[SERVER] {msg}")
        self.log_msg(f"Broadcasted: {msg}", "sys")
        self.bc_entry.delete(0, "end")

    def kick_selected(self):
        sel = self.client_lb.curselection()
        if not sel: return
        entry = self.client_lb.get(sel[0]).strip()
        nick = entry.split()[-1]   # last token is the nick
        with lock:
            target = clients.get(nick)
        if target:
            try:
                target.send("SYS:You have been kicked.".encode())
                target.close()
            except: pass
            self.log_msg(f"Kicked {nick}.", "leave")


if __name__ == "__main__":
    root = tk.Tk()
    ServerApp(root)
    root.mainloop()
