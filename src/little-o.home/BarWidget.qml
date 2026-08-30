import QtQuick
import qs.Ui

BarWidget {
  id: root
  moduleName: "little-o.home"
  implicitWidth: button.implicitWidth
  implicitHeight: button.implicitHeight

  BarIconButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    text: "󰋜"
    tooltipText: "Carl's Home"
    onPressed: function(b) {
      if (root.bar) root.bar.run("omarchy-shell shell summon little-o.home '{}'")
    }
  }
}
