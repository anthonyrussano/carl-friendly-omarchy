import QtQuick

Rectangle {
  id: tile

  required property string activityId
  required property string label
  required property string asset
  required property color tileColor
  required property int index
  signal chosen(string activityId)

  radius: Math.min(width, height) * 0.075
  color: tileColor
  border.width: activeFocus ? 6 : 0
  border.color: "#082859"
  scale: mouseArea.pressed ? 0.97 : (mouseArea.containsMouse ? 1.015 : 1.0)

  Behavior on scale {
    NumberAnimation { duration: 90 }
  }

  Image {
    id: picture
    anchors.top: parent.top
    anchors.topMargin: parent.height * 0.035
    anchors.horizontalCenter: parent.horizontalCenter
    width: parent.width * 0.82
    height: parent.height * 0.70
    source: Qt.resolvedUrl(tile.asset)
    fillMode: Image.PreserveAspectCrop
    asynchronous: true
    mipmap: true
  }

  Text {
    anchors.left: parent.left
    anchors.right: parent.right
    anchors.bottom: parent.bottom
    anchors.bottomMargin: parent.height * 0.045
    text: tile.label
    color: "#082859"
    horizontalAlignment: Text.AlignHCenter
    verticalAlignment: Text.AlignVCenter
    font.family: "Noto Sans"
    font.pixelSize: Math.max(24, Math.min(42, parent.height * 0.13))
    font.weight: Font.Bold
  }

  MouseArea {
    id: mouseArea
    anchors.fill: parent
    hoverEnabled: true
    cursorShape: Qt.PointingHandCursor
    onClicked: tile.chosen(tile.activityId)
  }
}
