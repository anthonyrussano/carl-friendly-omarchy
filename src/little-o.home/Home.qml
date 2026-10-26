import Quickshell
import Quickshell.Io
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
  readonly property string activitiesPath: manifest && manifest.__sourceDir
    ? manifest.__sourceDir + "/activities.json" : ""

  property var fallbackActivities: [
    { activityId: "draw", label: "Draw", asset: "assets/activity-draw.png", tileColor: "#f25b3f" },
    { activityId: "letters", label: "Letters", asset: "assets/activity-letters.png", tileColor: "#25b9b7" },
    { activityId: "numbers", label: "Numbers", asset: "assets/activity-numbers.png", tileColor: "#f7c928" },
    { activityId: "stories", label: "Stories", asset: "assets/activity-stories.png", tileColor: "#86bd35" },
    { activityId: "music", label: "Music", asset: "assets/activity-music.png", tileColor: "#8c65bd" },
    { activityId: "my-things", label: "My Things", asset: "assets/activity-my-things.png", tileColor: "#308ed1" }
  ]

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

  function select(index) {
    if (activities.count === 0) return
    selectedIndex = Math.max(0, Math.min(index, activities.count - 1))
    keyCatcher.forceActiveFocus()
  }

  function replaceActivities(items) {
    activities.clear()
    for (var i = 0; i < items.length; i++) activities.append(items[i])
    selectedIndex = 0
  }

  function loadActivities(raw) {
    try {
      var parsed = JSON.parse(String(raw || ""))
      if (!Array.isArray(parsed) || parsed.length !== 6) throw new Error("expected six activities")

      var safe = []
      var allowedIds = ["draw", "letters", "numbers", "stories", "music", "my-things"]
      var seenIds = {}
      for (var i = 0; i < parsed.length; i++) {
        var item = parsed[i]
        if (!item || allowedIds.indexOf(item.id) === -1) throw new Error("unknown activity id")
        if (seenIds[item.id]) throw new Error("duplicate activity id")
        seenIds[item.id] = true
        if (!String(item.asset || "").match(/^assets\/[a-z0-9-]+\.png$/)) throw new Error("unsafe asset path")
        if (!String(item.color || "").match(/^#[0-9a-fA-F]{6}$/)) throw new Error("invalid color")
        safe.push({
          activityId: String(item.id),
          label: String(item.label || "Activity"),
          asset: String(item.asset),
          tileColor: String(item.color)
        })
      }
      replaceActivities(safe)
    } catch (error) {
      console.warn("little-o.home: activities.json is invalid; using safe defaults:", error)
      replaceActivities(fallbackActivities)
    }
  }

  ListModel {
    id: activities
  }

  FileView {
    id: activitiesFile
    path: root.activitiesPath
    watchChanges: true
    printErrors: false
    onLoaded: root.loadActivities(text())
    onFileChanged: reload()
    onLoadFailed: root.replaceActivities(root.fallbackActivities)
  }

  Component.onCompleted: replaceActivities(fallbackActivities)

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
        if (count === 0) return
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
          id: homeButton
          anchors.left: parent.left
          anchors.verticalCenter: parent.verticalCenter
          width: header.height
          height: header.height
          radius: width / 2
          color: "#fff9ee"
          border.color: "#d8b98b"
          Text { anchors.centerIn: parent; text: "󰋜"; color: "#082859"; font.family: "JetBrainsMono Nerd Font"; font.pixelSize: parent.height * 0.48 }
          Accessible.role: Accessible.Button
          Accessible.name: "Start with Draw"
          activeFocusOnTab: true
          border.width: activeFocus ? 6 : 3
          Keys.onPressed: function(event) {
            if (event.key === Qt.Key_Return || event.key === Qt.Key_Enter || event.key === Qt.Key_Space) {
              root.select(0)
              event.accepted = true
            }
          }
          MouseArea {
            anchors.fill: parent
            cursorShape: Qt.PointingHandCursor
            onClicked: root.select(0)
          }
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
          id: volumeButton
          anchors.right: parent.right
          anchors.verticalCenter: parent.verticalCenter
          width: header.height
          height: header.height
          radius: width / 2
          color: "#fff9ee"
          border.color: "#d8b98b"
          Text { anchors.centerIn: parent; text: "󰕾"; color: "#082859"; font.family: "JetBrainsMono Nerd Font"; font.pixelSize: parent.height * 0.42 }
          Accessible.role: Accessible.Button
          Accessible.name: "Sound settings"
          activeFocusOnTab: true
          border.width: activeFocus ? 6 : 3
          Keys.onPressed: function(event) {
            if (event.key === Qt.Key_Return || event.key === Qt.Key_Enter || event.key === Qt.Key_Space) {
              root.launch("volume")
              event.accepted = true
            }
          }
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
            selected: index === root.selectedIndex
            onPreviewed: root.selectedIndex = index
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
          id: grownButton
          property real holdProgress: 0
          anchors.right: parent.right
          anchors.verticalCenter: parent.verticalCenter
          width: Math.min(250, content.width * 0.25)
          height: footer.height
          radius: 22
          color: grownMouse.pressed ? "#e7dcc8" : "#eadcc5"
          border.width: activeFocus ? 6 : 3
          border.color: activeFocus ? "#082859" : "#c4a879"
          clip: true
          Accessible.role: Accessible.Button
          Accessible.name: "Hold for grown-ups"
          Accessible.description: "Press and hold for two seconds"
          activeFocusOnTab: true

          Rectangle {
            anchors.left: parent.left
            anchors.bottom: parent.bottom
            width: parent.width * grownButton.holdProgress
            height: 10
            color: "#205ea6"
          }
          Text {
            anchors.centerIn: parent
            width: parent.width - 24
            text: grownButton.holdProgress > 0 ? "Keep holding…" : "Hold for grown-ups"
            color: "#082859"
            horizontalAlignment: Text.AlignHCenter
            wrapMode: Text.WordWrap
            font.family: "Noto Sans"
            font.pixelSize: Math.max(16, parent.height * 0.21)
            font.bold: true
          }
          NumberAnimation {
            id: grownHold
            target: grownButton
            property: "holdProgress"
            from: 0
            to: 1
            duration: 1800
            onFinished: root.launch("grown-ups")
          }
          function startHold() {
            holdProgress = 0
            grownHold.restart()
          }
          function cancelHold() {
            grownHold.stop()
            holdProgress = 0
          }
          Keys.onPressed: function(event) {
            if (!event.isAutoRepeat && (event.key === Qt.Key_Return || event.key === Qt.Key_Enter || event.key === Qt.Key_Space)) {
              startHold()
              event.accepted = true
            }
          }
          Keys.onReleased: function(event) {
            if (event.key === Qt.Key_Return || event.key === Qt.Key_Enter || event.key === Qt.Key_Space) {
              cancelHold()
              event.accepted = true
            }
          }
          MouseArea {
            id: grownMouse
            anchors.fill: parent
            cursorShape: Qt.PointingHandCursor
            onPressed: grownButton.startHold()
            onReleased: grownButton.cancelHold()
            onCanceled: grownButton.cancelHold()
          }
        }
      }
    }
  }
}
