import 'package:flutter/material.dart';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;

//this.backgroundColor,
//    this.elevation,
//    this.shadowColor,
//    this.surfaceTintColor,
//    this.shape,
//

//Widget SideDrawerLight(final List<types.Message> _messages) {
Widget SideDrawerLight(bool _isLightMode, final Function clearMessages) {
  return Drawer(
    width: 250.0,
    shadowColor: Colors.blue,
    backgroundColor: _isLightMode ? Colors.white60 : Colors.blueGrey,
    child: ListView(
      padding: EdgeInsets.zero,
      children: [
        Container(
          height: 100,
          decoration: _isLightMode
              ? const BoxDecoration(color: Colors.blue)
              : const BoxDecoration(color: Colors.purple),
          child: const DrawerHeader(
            margin: EdgeInsets.zero,
            padding: EdgeInsets.all(16.0),
            child: Center(
              child: Text('Drawer header'),
            ),
          ),
        ),
        ListTile(
          title: const Text('Item 1'),
          onTap: () {},
        ),
        ListTile(
          title: const Text('Item 2'),
          onTap: () {},
        ),
        ListTile(
          title: const Text('New Chat'),
          onTap: () {
            clearMessages();
          },
        ),
      ],
    ),
  );
}

//this.style,
//    this.selectedColor,
//    this.iconColor,
//    this.textColor,
//    this.titleTextStyle,
//    this.subtitleTextStyle,
//    this.leadingAndTrailingTextStyle,
//    this.contentPadding,
//    this.enabled = true,
//    this.onTap,
//    this.onLongPress,
//    this.onFocusChange,
//    this.mouseCursor,
//    this.selected = false,
//    this.focusColor,
//    this.hoverColor,
//    this.splashColor,
//    this.focusNode,
//    this.autofocus = false,
//    this.tileColor,
//    this.selectedTileColor,
//
//
