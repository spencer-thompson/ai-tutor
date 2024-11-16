import 'package:flutter/material.dart';

Widget SideDrawer() {
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
      ],
    ),
  );
}
