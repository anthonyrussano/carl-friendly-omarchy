import Quickshell
import Quickshell.Wayland
import QtQuick

Item {
  id: root

  property var shell: null
  property var manifest: null
  property bool opened: true
  property int selectedIndex: 0
  readonly property string pluginId: (manifest && manifest.id) || "little-o.home"
  readonly property string launcher: Quickshell.env("HOME") + "/.local/bin/little-o-launch"

  function open(payloadJson) {
    opened = true
    selectedIndex = 0
    Qt.callLater(function() { keyCatcher.forceActiveFocus() })
  }

  function close() { opened = false }
  function toggle() { opened ? close() : open("{}") }

  function dismiss() {
    opened = false
    if (shell && typeof shell.hide === "function") shell.hide(pluginId)
  }

  function launch(activityId) {
    if (activityId !== "volume") dismiss()
    Quickshell.execDetached([launcher, activityId])
  }

  ListModel {
    id: activities
    ListElement { activityId: "draw"; label: "Draw"; asset: "assets/activity-draw.png"; tileColor: "#f25b3f" }
    ListElement { activityId: "letters"; label: "Letters"; asset: "assets/activity-letters.png"; tileColor: "#25b9b7" }
    ListElement { activityId: "numbers"; label: "Numbers"; asset: "assets/activity-numbers.png"; tileColor: "#f7c928" }
    ListElement { activityId: "stories"; label: "Stories"; asset: "assets/activity-stories.png"; tileColor: "#86bd35" }
    ListElement { activityId: "music"; label: "Music"; asset: "assets/activity-music.png"; tileColor: "#8c65bd" }
    ListElement { activityId: "my-things"; label: "My Things"; asset: "assets/activity-my-things.png"; tileColor: "#308ed1" }
  }

  PanelWindow {
    id: panel
    visible: root.opened
    anchors { top: true; bottom: true; left: true; right: true }
    color: "#f5e7d0"
    WlrLayershell.namespace: "little-o-home"
    // Keep the child home above ordinary windows, but below Omarchy's overlay
    // panels. This ensures the audio flyout exclusively owns pointer input.
    WlrLayershell.layer: WlrLayer.Top
    WlrLayershell.keyboardFocus: WlrKeyboardFocus.Exclusive
    exclusionMode: ExclusionMode.Ignore

    Image {
      anchors.fill: parent
      source: "assets/playroom-background.png"
      fillMode: Image.PreserveAspectCrop
      asynchronous: true
      mipmap: true
    }

    Item {
      id: keyCatcher
      anchors.fill: parent
      focus: true

      Keys.onPressed: function(event) {
        var count = activities.count
        if (event.key === Qt.Key_Left) root.selectedIndex = (root.selectedIndex + count - 1) % count
        else if (event.key === Qt.Key_Right) root.selectedIndex = (root.selectedIndex + 1) % count
        else if (event.key === Qt.Key_Up) root.selectedIndex = (root.selectedIndex + count - 3) % count
        else if (event.key === Qt.Key_Down) root.selectedIndex = (root.selectedIndex + 3) % count
        else if (event.key === Qt.Key_Return || event.key === Qt.Key_Enter || event.key === Qt.Key_Space)
          root.launch(activities.get(root.selectedIndex).activityId)
        else if (event.key === Qt.Key_Escape) root.launch("grown-ups")
        else return
        event.accepted = true
      }
    }

    Item {
      id: content
      anchors.fill: parent
      anchors.leftMargin: Math.max(28, parent.width * 0.045)
      anchors.rightMargin: Math.max(28, parent.width * 0.045)
      anchors.topMargin: Math.max(18, parent.height * 0.025)
      anchors.bottomMargin: Math.max(18, parent.height * 0.025)

      Item {
        id: header
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        height: Math.min(92, Math.max(64, content.height * 0.12))

        Rectangle {
          anchors.left: parent.left
          anchors.verticalCenter: parent.verticalCenter
          width: header.height
          height: header.height
          radius: width / 2
          color: "#fff9ee"
          border.width: 3
          border.color: "#d8b98b"
          Text { anchors.centerIn: parent; text: "󰋜"; color: "#082859"; font.family: "JetBrainsMono Nerd Font"; font.pixelSize: parent.height * 0.48 }
        }

        Text {
          anchors.left: parent.left
          anchors.right: parent.right
          anchors.verticalCenter: parent.verticalCenter
          text: "Carl's Computer"
          color: "#082859"
          horizontalAlignment: Text.AlignHCenter
          font.family: "Noto Sans"
          font.pixelSize: Math.max(34, Math.min(58, header.height * 0.62))
          font.weight: Font.Black
        }

        Rectangle {
          anchors.right: parent.right
          anchors.verticalCenter: parent.verticalCenter
          width: header.height
          height: header.height
          radius: width / 2
          color: "#fff9ee"
          border.width: 3
          border.color: "#d8b98b"
          Text { anchors.centerIn: parent; text: "󰕾"; color: "#082859"; font.family: "JetBrainsMono Nerd Font"; font.pixelSize: parent.height * 0.42 }
          MouseArea { anchors.fill: parent; cursorShape: Qt.PointingHandCursor; onClicked: root.launch("volume") }
        }
      }

      Grid {
        id: grid
        anchors.top: header.bottom
        anchors.topMargin: 14
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: footer.top
        anchors.bottomMargin: 14
        columns: 3
        rows: 2
        spacing: Math.max(12, panel.width * 0.012)

        Repeater {
          model: activities
          delegate: ActivityTile {
            width: (grid.width - grid.spacing * 2) / 3
            height: (grid.height - grid.spacing) / 2
            activeFocusOnTab: true
            border.width: index === root.selectedIndex ? 6 : 0
            onChosen: function(id) { root.selectedIndex = index; root.launch(id) }
          }
        }
      }

      Item {
        id: footer
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        height: Math.min(90, Math.max(68, content.height * 0.12))

        Rectangle {
          anchors.horizontalCenter: parent.horizontalCenter
          anchors.verticalCenter: parent.verticalCenter
          width: Math.min(520, content.width * 0.52)
          height: footer.height
          radius: height / 2
          color: helperMouse.pressed ? "#e7dcc8" : "#fff9ee"
          border.width: 4
          border.color: "#d8b98b"

          Row {
            anchors.centerIn: parent
            spacing: 14
            Text { text: "󰍬"; color: "#205ea6"; font.family: "JetBrainsMono Nerd Font"; font.pixelSize: Math.min(38, footer.height * 0.46) }
            Text { text: "Talk to Helper"; color: "#082859"; font.family: "Noto Sans"; font.pixelSize: Math.min(30, footer.height * 0.34); font.bold: true }
          }
          MouseArea { id: helperMouse; anchors.fill: parent; cursorShape: Qt.PointingHandCursor; onClicked: root.launch("helper") }
        }

        Rectangle {
          anchors.right: parent.right
          anchors.verticalCenter: parent.verticalCenter
          width: Math.min(170, content.width * 0.17)
          height: footer.height
          radius: 22
          color: grownMouse.pressed ? "#e7dcc8" : "#eadcc5"
          border.width: 3
          border.color: "#c4a879"
          Text { anchors.centerIn: parent; text: "Grown-ups"; color: "#082859"; font.family: "Noto Sans"; font.pixelSize: Math.max(18, parent.height * 0.25); font.bold: true }
          MouseArea { id: grownMouse; anchors.fill: parent; cursorShape: Qt.PointingHandCursor; onClicked: root.launch("grown-ups") }
        }
      }
    }
  }
}
