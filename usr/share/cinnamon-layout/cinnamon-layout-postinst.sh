#!/bin/bash

# ==============================================================================
# cinnamon-layout-postinst.sh
#
#   This script is automatically run by the postinst configure step on
#       installation of cinnamon-layout. It can be manually re-run, but
#       is only intended to be run at package installation.
#
#   2018-01-05 rik: initial release
#   2018-01-18 rik: transparent-panels: set first-launch default to false
#   - ITM thumbnail-size default=8
#   2018-02-28 rik: ITM - include-all-windows: set to "false"
#   - ITM: thumbnail-padding: set to 5
#   2018-05-23 rik: setting ITM setting file to 3.8
#   2018-05-23 rik: correcting transparent-panels adjustment
#   2018-09-19 rik: adjusting default ITM pinned-apps
#   2019-07-28 rik: adding collapsible-systray@feuerfuchs.eu tweaks
#   2019-11-17 rik: updating name to cinnamon-layout
#   2019-11-21 rik: removing ITM adjustments
#   2019-12-28 rik: installing menu-icon to update-alternatives
#
# ==============================================================================

# ------------------------------------------------------------------------------
# Check to ensure running as root
# ------------------------------------------------------------------------------
#   No fancy "double click" here because normal user should never need to run
if [ $(id -u) -ne 0 ]
then
	echo
	echo "You must run this script with sudo." >&2
	echo "Exiting...."
	sleep 5s
	exit 1
fi

# ------------------------------------------------------------------------------
# Initial setup
# ------------------------------------------------------------------------------

echo
echo "*** Script Entry: cinnamon-layout-postinst.sh"
echo

# Setup Directory for later reference
DIR=/usr/share/cinnamon-layout

# ------------------------------------------------------------------------------
# Applet / Extension adjustments
# ------------------------------------------------------------------------------

# Making adjustments here since only we place these
#   applets at the system level so don't need to be concerned they will be
#   overridden by any updates to cinnamon, etc.

# applet: calendar@simonwiles.net
JSON_FILE=/usr/share/cinnamon/applets/calendar@simonwiles.net/settings-schema.json
echo "updating JSON_FILE: $JSON_FILE"
# updates:
# - use-custom-format: custom panel clock format
# - custom-format: set to "%l:%M %p"
# - note: jq can't do "sed -i" inplace update, so need to re-create file, then
#     update ownership (in case run as root)
NEW_FILE=$(jq '.["use-custom-format"].default=true | .["custom-format"].default="%l:%M %p"' \
    < $JSON_FILE)
echo "$NEW_FILE" > $JSON_FILE

# applet: collapsible-systray@feuerfuchs.eu
JSON_FILE=/usr/share/cinnamon/applets/collapsible-systray@feuerfuchs.eu/4.0/settings-schema.json
echo "updating JSON_FILE: $JSON_FILE"
# updates:
# - tray-icon-padding: set to 2
# - note: jq can't do "sed -i" inplace update, so need to re-create file, then
#     update ownership (in case run as root)
NEW_FILE=$(jq '.["tray-icon-padding"].default=2' \
    < $JSON_FILE)
echo "$NEW_FILE" > $JSON_FILE

# applet: places-bookmarks@dmo60.de
JSON_FILE=/usr/share/cinnamon/applets/places-bookmarks@dmo60.de/settings-schema.json
echo "updating JSON_FILE: $JSON_FILE"
# updates:
# - pref_applet_icon: set to user-home-symbolic
# - note: jq can't do "sed -i" inplace update, so need to re-create file, then
#     update ownership (in case run as root)
NEW_FILE=$(jq '.["pref_applet_icon"].default="user-home-symbolic"' \
    < $JSON_FILE)
echo "$NEW_FILE" > $JSON_FILE

# extension: transparent-panels@germanfr
JSON_FILE=/usr/share/cinnamon/extensions/transparent-panels@germanfr/settings-schema.json
echo "updating JSON_FILE: $JSON_FILE"
# updates:
# - transparency-type: panel-semi-transparent
# - first-launch: false (so won't show prompt)
# - note: jq can't do "sed -i" inplace update, so need to re-create file, then
#     update ownership (in case run as root)
NEW_FILE=$(jq '.["transparency-type"].default="panel-semi-transparent" | .["first-launch"].default=false' \
    < $JSON_FILE)
echo "$NEW_FILE" > $JSON_FILE

# ------------------------------------------------------------------------------
# Dconf / Gsettings Default Value adjustments
# ------------------------------------------------------------------------------
echo
echo "*** Updating dconf / gsettings default values"
echo

# MAIN System schemas: we have placed our override file in this directory
# Sending any "error" to null (if key not found don't want to worry user)
glib-compile-schemas /usr/share/glib-2.0/schemas/ > /dev/null 2>&1 || true;

# ------------------------------------------------------------------------------
# Finished
# ------------------------------------------------------------------------------
echo
echo "*** Script Exit: cinnamon-layout-postinst.sh"
echo

exit 0
