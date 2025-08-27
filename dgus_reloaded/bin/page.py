'''A consolidation of Page classes'''
#
# Copyright (C) 2020  Desuuuu <contact@desuuuu.com>
#
# This file may be distributed under the terms of the GNU GPLv3 license.
from typing import Optional, List, Any

class T5UID1_Page:
    '''Handles the capture of all existing page definitions from pages.cfg'''
    def __init__(self, var_names, config):
        self.printer = config.get_printer()
        name_parts = config.get_name().split()
        if len(name_parts) != 2:
            raise config.error(f"Section name '{config.get_name()}' is not valid")

        self.name = name_parts[1]

        self.id = config.getint('id', minval=0, maxval=255)
        self.is_boot = config.getboolean('boot', False)
        self.is_timeout = config.getboolean('timeout', False)
        self.is_shutdown = config.getboolean('shutdown', False)
        self.var_auto = []
        self.var = []

        for var in config.get('var_auto', '').split(','):
            var = var.strip()
            if len(var) > 0 and var not in self.var_auto:
                if var not in var_names:
                    raise config.error(f"Invalid var '{var}' in section '{config.get_name()}'")
                self.var_auto.append(var)

        for var in config.get('var', '').split(','):
            var = var.strip()
            if (len(var) > 0
                and var not in self.var_auto and var not in self.var):
                if var not in var_names:
                    raise config.error(f"Invalid var '{var}' in section '{config.get_name()}'")
                self.var.append(var)

# Page/navigation manager extracted from t5uid1.py to reduce class size.
class PageManager:
    """Manage page switching, history and debounce logic on behalf of a T5UID1 instance."""

    def __init__(self, owner: Any):
        self.owner = owner
        self.history: List[str] = []
        self._debounce_timer = None
        self._pending_page: Optional[str] = None

    def switch_page(self, page_name: str, immediate: bool = False) -> None:
        """Switch to page_name. If immediate is False, use debounce_switch_page."""
        try:
            self.owner.logger.info("PageManager.switch_page requested: %s immediate=%s", page_name, immediate)
        except Exception:
            pass

        if page_name == getattr(self.owner, "page_name", None):
            try:
                self.owner.logger.info("PageManager.switch_page: already on %s", page_name)
            except Exception:
                pass
            return

        if not immediate:
            self.debounce_switch_page(page_name)
            return

        # push current page onto history
        cur = getattr(self.owner, "page_name", None)
        if cur:
            self.history.append(cur)

        # log page id if available (use public accessor if present)
        try:
            page_obj = getattr(self.owner, "pages", {}).get(page_name)
            pid = getattr(page_obj, "id", None)
            self.owner.logger.info("PageManager.switch_page: actually switching to %s (id=%r)", page_name, pid)
        except Exception:
            pass

        # set and request a full update
        self.owner.page_name = page_name
        # send the low-level page-change to the display (prefer direct write)
        try:
            pid = getattr(self.owner, "pages", {}).get(page_name)
            pid = getattr(pid, "id", None) if pid is not None else None

            if pid is None:
                self.owner.logger.info("PageManager.switch_page: pid is None")
                # fallback: try to lookup id from owner's _pages (internal)
                try:
                    pid = getattr(self.owner, "_pages", {}).get(page_name).id
                except Exception:
                    pid = None

            if pid is not None:
                self.owner.logger.info("PageManager.switch_page: pid is not None")
                addr = getattr(self.owner, "T5UID1_ADDR_PAGE", 0x84)
                self.owner.logger.info("PageManager.switch_page: addr=%s, pid=%s", addr, pid)
                try:
                    # correct DGUS page-switch payload: 0x5A 0x01 0x00 <page_id>
                    payload = bytearray([0x5A, 0x01, 0x00, pid])
                    self.owner.t5uid1_command_write(addr, payload, send=True)
                except Exception:
                    try:
                        self.owner.full_update()
                    except Exception:
                        pass
            else:
                # no page id known — fall back to owner.full_update()
                try:
                    self.owner.full_update()
                except Exception:
                    pass
        except Exception:
            try:
                self.owner.logger.exception("PageManager: error sending page change")
            except Exception:
                pass

    def return_to_previous_page(self) -> None:
        """Return to previous page from history if available."""
        if not self.history:
            return
        prev = self.history.pop()
        self.switch_page(prev, immediate=True)

    def debounce_switch_page(self, page_name: str, delay: float = 0.15) -> None:
        """Schedule a debounced page switch via the owner's reactor."""
        # store pending target
        self._pending_page = page_name

        # try to register or update a timer on the owner's reactor
        try:
            reactor = self.owner.reactor
            # register timer if not already present
            if self._debounce_timer is None:
                self._debounce_timer = reactor.register_timer(self._do_switch_cb)
            # schedule waketime
            reactor.update_timer(self._debounce_timer, reactor.monotonic() + delay)
            try:
                self.owner.logger.info("PageManager.debounce_switch_page: scheduling %s delay=%s", page_name, delay)
            except Exception:
                pass
        except Exception:
            # fallback: perform immediate switch if reactor unavailable
            self.switch_page(page_name, immediate=True)

    def abort_page_switch(self) -> None:
        """Abort any pending debounced switch."""
        try:
            if self._debounce_timer is not None:
                self.owner.reactor.remove_timer(self._debounce_timer)
        except Exception:
            pass
        self._debounce_timer = None
        self._pending_page = None

    def _do_switch_cb(self, eventtime):
        """Timer callback to perform the pending switch; returns NEVER to not reschedule."""
        try:
            if self._pending_page:
                page = self._pending_page
                self._pending_page = None
                self._debounce_timer = None
                self.switch_page(page, immediate=True)
        except Exception:
            try:
                self.owner.logger.exception("error in page switch callback")
            except Exception:
                pass
        return getattr(self.owner.reactor, "NEVER", None)

    def full_update(self) -> None:
        """Delegate to owner's full_update if present."""
        try:
            self.owner.full_update()
        except Exception:
            pass
