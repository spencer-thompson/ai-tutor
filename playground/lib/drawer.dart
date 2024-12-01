import 'package:flutter/material.dart';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;

Widget SideDrawerLight(final List<types.Message> _messages) {
  return Drawer(
    width: 250.0,
    child: ListView(
      padding: EdgeInsets.zero,
      children: [
        Container(
          height: 100,
          decoration: const BoxDecoration(color: Colors.blue),
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
          onTap: _messages.clear,
        ),
      ],
    ),
  );
}

Widget SideDrawerDark(final List<types.Message> _messages) {
  return Drawer(
    width: 250.0,
    child: ListView(
      padding: EdgeInsets.zero,
      children: [
        Container(
          height: 100,
          decoration: const BoxDecoration(color: Colors.purple),
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
      ],
    ),
  );
}
