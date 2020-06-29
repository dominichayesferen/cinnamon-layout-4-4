#!/usr/bin/python3

import subprocess
import os

from gi.repository.Gtk import SizeGroup, SizeGroupMode

from xapp.GSettingsWidgets import *
from CinnamonGtkSettings import CssRange, CssOverrideSwitch, GtkSettingsSwitch, PreviewWidget, Gtk2ScrollbarSizeEditor
from SettingsWidgets import LabelRow, SidePage, walk_directories
from ChooserButtonWidgets import PictureChooserButton
from ExtensionCore import DownloadSpicesPage
from Spices import Spice_Harvester

import glob

ICON_SIZE = 48

class Module:
    comment = _("Change the layout of your desktop")
    name = "ubuntucinnamondesktoplayout"
    category = "appear"

    def __init__(self, content_box):
        self.keywords = _("layout, cinnamon")
        self.icon = "cinnamon-layout"
        self.window = None
        sidePage = SidePage(_("Desktop Layout"), self.icon, self.keywords, content_box, module=self)
        self.sidePage = sidePage

    def on_module_selected(self):
        if not self.loaded:
            print("Loading Desktop Layout module")

            self.sidePage.stack = SettingsStack()
            self.sidePage.add_widget(self.sidePage.stack)

            self.layout_settings = Gio.Settings.new("com.ubuntu-cinnamon-remix.cinnamon-layout")

            self.scale = self.window.get_scale_factor()

            self.layout_chooser = self.create_button_chooser(self.layout_settings, 'current-layout', button_picture_size=100*self.scale, menu_pictures_size=100*self.scale, num_cols=4)
            #You can change the thumbnail size by editing button_picture_size and menu_pictures_size. e.g.: '140*self.scale' for Feren OS's 'Theme' button but with scaling support

            page = SettingsPage()
            self.sidePage.stack.add_titled(page, "layout", _("Desktop Layout"))

            settings = page.add_section(_(""))

            widget = self.make_group(_("Desktop Layout"), self.layout_chooser)
            settings.add_row(widget)

            widget = SettingsWidget()
            widget.set_spacing(5)
            image = Gtk.Image()
            image.set_from_icon_name( "security-high-symbolic", Gtk.IconSize.BUTTON );
            buttonroot = Gtk.Button(label="Set as Default Layout", image=image)
            buttonroot.connect("clicked", self.save_to_system)
            widget.pack_start(buttonroot, True, True, 0)
            widget.pack_end(buttonroot, True, True, 0)
            settings.add_row(widget)

            self.refresh()

    def refresh(self):
        #Cinnamon Settings Module Coding is weird, man. Ended up sorta butchering it so had to do it this way. Sorry about that. :/
        self.layout_chooser.clear_menu()

        self.layout_chooser.add_picture("/usr/share/cinnamon-layout/resources/thumbnails/default.png", self._on_layout_selected, title="Default", id="default")
        self.layout_chooser.add_picture("/usr/share/cinnamon-layout/resources/thumbnails/traditional.png", self._on_layout_selected, title="Traditional", id="traditional")
        self.layout_chooser.add_picture("/usr/share/cinnamon-layout/resources/thumbnails/redmond7.png", self._on_layout_selected, title="Redmond 7", id="redmond7")
        self.layout_chooser.add_picture("/usr/share/cinnamon-layout/resources/thumbnails/cupertino.png", self._on_layout_selected, title="Cupertino", id="cupertino")
        self.layout_chooser.add_picture("/usr/share/cinnamon-layout/resources/thumbnails/unity.png", self._on_layout_selected, title="Unity", id="unity")
        self.layout_chooser.add_picture("/usr/share/cinnamon-layout/resources/thumbnails/widescreen.png", self._on_layout_selected, title="Widescreen", id="widescreen")
        self.layout_chooser.add_picture("/usr/share/cinnamon-layout/resources/thumbnails/gnome2.png", self._on_layout_selected, title="GNOME 2", id="gnome2")

        theme = self.layout_settings.get_string("current-layout")
        #Change the strings and descriptions to be more-so fashionable
        if theme == 'default':
            self.layout_chooser.set_button_label("Default")
            self.layout_chooser.set_tooltip_text("System default Cinnamon layout")
        elif theme == 'traditional':
            self.layout_chooser.set_button_label("Traditional")
            self.layout_chooser.set_tooltip_text("Windows XP inspired layout with non-grouped window list")
        elif theme == 'redmond7':
            self.layout_chooser.set_button_label("Redmond 7")
            self.layout_chooser.set_tooltip_text("Windows 7 inspired layout with grouped window list")
        elif theme == 'cupertino':
            self.layout_chooser.set_button_label("Cupertino")
            self.layout_chooser.set_tooltip_text("macOS/OSX inspired layout")
        elif theme == 'unity':
            self.layout_chooser.set_button_label("Unity")
            self.layout_chooser.set_tooltip_text("Ubuntu Unity inspired layout")
        elif theme == 'widescreen':
            self.layout_chooser.set_button_label("Widescreen")
            self.layout_chooser.set_tooltip_text("Left panel widescreen layout")
        elif theme == 'gnome2':
            self.layout_chooser.set_button_label("GNOME 2")
            self.layout_chooser.set_tooltip_text("GNOME 2 inspired top and bottom dual-panel layout")
        
        try:
            for path in ["/usr/share/cinnamon-layout/resources/thumbnails/%s.png" % (theme)]:
                self.layout_chooser.set_picture_from_file(path)
        except:
            pass
            #IDK, feel free to add a generic missing thumbnail thumbnail if needs ever be and make it set to that image.

    def _setParentRef(self, window):
        self.window = window

    def make_group(self, group_label, widget, add_widget_to_size_group=True):
        self.size_groups = getattr(self, "size_groups", [Gtk.SizeGroup.new(Gtk.SizeGroupMode.HORIZONTAL) for x in range(2)])
        box = SettingsWidget()
        label = Gtk.Label()
        label.set_markup(group_label)
        label.props.xalign = 0.0
        self.size_groups[0].add_widget(label)
        box.pack_start(label, False, False, 0)
        if add_widget_to_size_group:
            self.size_groups[1].add_widget(widget)
        box.pack_end(widget, False, False, 0)

        return box

    def create_button_chooser(self, settings, key, button_picture_size, menu_pictures_size, num_cols):
        chooser = PictureChooserButton(num_cols=num_cols, button_picture_size=button_picture_size, menu_pictures_size=menu_pictures_size, has_button_label=True)
        
        return chooser

    def _on_layout_selected(self, path, theme):
        #Layout applying code, here.
        try:
            self.layout_settings.set_string("current-layout", theme)
            layoutapply = subprocess.Popen(["/usr/bin/cinnamon-layout", theme])
            layoutapply.communicate()[0]
            self.refresh()
        except Exception as detail:
            print(detail)
        return True

    def save_to_system(self, button):
        #button is required, much as it's unused
        theme = self.layout_settings.get_string("current-layout")
        layoutsave = subprocess.Popen(["/usr/bin/pkexec", "/usr/bin/cinnamon-layout-system", theme])
        layoutsave.communicate()[0]
        #Code for checking for exit code being 0, if you want to use it, below right here:
        #if layoutsave.returncode != 0:
        #   print("Success")
        #else:
        #   print("Failure")
