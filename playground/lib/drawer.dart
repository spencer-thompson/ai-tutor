import 'package:flutter/material.dart';
import 'package:group_button/group_button.dart';

Widget SideDrawerLight(bool _isLightMode, final Function clearMessages) {
  final controller = GroupButtonController();

  return Drawer(
    width: 250.0,
    shadowColor: Colors.blue,
    backgroundColor: _isLightMode ? Colors.white60 : Colors.blueGrey,
    child: Column(
      //padding: EdgeInsets.zero,
      children: [
        Container(
          height: 100,
          decoration: _isLightMode
              ? const BoxDecoration(
                  color: Colors.blue,
                )
              : const BoxDecoration(color: Colors.purple),
          child: DrawerHeader(
            margin: EdgeInsets.zero,
            padding: const EdgeInsets.fromLTRB(0.0, 16.0, 16.0, 8.0),
            //padding: EdgeInsets.all(16.0),
            child: Row(
              children: [
                IconButton(
                  icon: Icon(Icons.settings, size: 40.0),
                  onPressed: () {},
                ),
                Center(
                  child:
                      Text('Drawer header', style: TextStyle(fontSize: 20.0)),
                ),
              ],
            ),
          ),
        ),
        SizedBox(
          height: 10.0,
        ),
        SizedBox(
          width: 200.0,
          height: 20.0,
          child: TextButton(
            style: TextButton.styleFrom(
              backgroundColor: Colors.blue,
              shadowColor: Colors.red,
              minimumSize: Size.zero,
            ),
            onPressed: () {},
            child: const Text("The button"),
          ),
        ),
        GroupButton(
          controller: controller,
          isRadio: false,
          buttons: [
            "CS 439R",
            "CS 479R",
            "CS 4450",
            "Math 4610",
            "Math Lab Training",
          ],
          onSelected: (val, i, selected) =>
              debugPrint('$val = $selected (#$i)'),
        ),
        GroupButton(
          options: GroupButtonOptions(
            selectedShadow: const [],
            selectedTextStyle: TextStyle(
              fontSize: 20,
              color: Colors.pink[900],
            ),
            selectedColor: Colors.pink[100],
            unselectedShadow: const [],
            unselectedColor: Colors.amber[100],
            unselectedTextStyle: TextStyle(
              fontSize: 20,
              color: Colors.amber[900],
            ),
            selectedBorderColor: Colors.pink[900],
            unselectedBorderColor: Colors.amber[900],
            borderRadius: BorderRadius.circular(100),
            spacing: 10,
            runSpacing: 10,
            groupingType: GroupingType.wrap,
            direction: Axis.horizontal,
            buttonHeight: 60,
            buttonWidth: 60,
            mainGroupAlignment: MainGroupAlignment.start,
            crossGroupAlignment: CrossGroupAlignment.start,
            groupRunAlignment: GroupRunAlignment.start,
            textAlign: TextAlign.center,
            textPadding: EdgeInsets.zero,
            alignment: Alignment.center,
            elevation: 0,
          ),
          controller: controller,
          isRadio: false,
          buttons: [
            "CS 439R",
            "CS 479R",
            "CS 4450",
            "Math 4610",
            "Math Lab Training",
          ],
          onSelected: (val, i, selected) =>
              debugPrint('$val = $selected (#$i)'),
        ),
      ],
    ),
  );
}
