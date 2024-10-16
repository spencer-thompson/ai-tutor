import 'package:flutter/material.dart';
import 'dart:convert';
import 'dart:math';

import 'package:flutter_chat_types/flutter_chat_types.dart' as types;
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
// it would be cool to have the user press a key for which 'version' of main they want to run. That way I could have multiple
// main.dart's within the same flutter project. I'm thinking of adding a terminal command of sorts
//flutter run -d chrome web-server --web-port 1234

String randomString() {
  final random = Random
      .secure(); // create a cryptographicall secure random number generator
  final values = List<int>.generate(16, (i) => random.nextInt(255));
  // generate a list of 16 integers that are all between 0 and 255
  return base64UrlEncode(values); // this converts ascii numbers to ascii values
}

void main() {
  // start here and do the thing
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key}); //inherit everything from the statelesswidget

  @override
  Widget build(BuildContext context) => const MaterialApp(
        // the build context will now render the MaterialApp
        home: MyHomePage(), // the default page is the MyHomePage() widget
      );
}

class MyHomePage extends StatefulWidget {
  const MyHomePage(
      {super.key}); // inherit all the stuff from the statefulwidget class

  @override
  State<MyHomePage> createState() =>
      _MyHomePageState(); // all of the State (mutable) values will be in the _MyHomePageState() class
}

class _MyHomePageState extends State<MyHomePage> {
  final List<types.Message> _messages =
      []; // _messages can't be changed once it is initialized
  // types.Message refers to the Message type fro the flutter_chat_types.dart imported package
  final _user = const types.User(
      id: '82091008-a484-4a89-ae75-a22bf8d6f3ac'); // _user is a private variable that won't change
  // we have a 'User' type in types.User. The id is a UUID which is a Universally Unique Identifier is a 32 character
  // string with 4 hyphens in it. This means that it is 128 bits, or 32x4 bits because it is in hex.
  @override
  Widget build(BuildContext context) => Scaffold(
        //the build method defines the UI of the widget
        // the BuildContext specifies where the Widget lies in the widget tree
        // the Scaffold provides a structure with special parameters to recognize other widgets and there places within the UI
        body: Chat(
          //this is a custom widget from the flutter_chat_ui.dart package
          // the Chat has specific parameter fields as it is designed to make the Chat interfaces easy to work with
          messages:
              _messages, // messages contain the most recent list of types.Message
          onSendPressed:
              _handleSendPressed, // this is what we do when the button is pressed. Enter also works by default
          user:
              _user, // probably a necessary element for the chat ui is the user's id (the UUID) seen earlier
        ),
      );

  void _addMessage(types.Message message) {
    // change the state of the private _messages variable
    setState(() {
      _messages.insert(
          0, message); // we will insert this at the beginning of the list
      // if the message is blank we are adding nothing to the messages I guess. Not really sure how we are filtering
      // for empty texts
    });
  }

  void _handleSendPressed(types.PartialText message) {
    // if the enter or send button is pressed
    // we accept a PartialText message because our text may be empty, or it may not
    final textMessage = types.TextMessage(
      author: _user,
      createdAt: DateTime.now()
          .millisecondsSinceEpoch, // this is a time format that is independent of the time zone
      id: randomString(), // this is the id of the text message, a 16 character 8-bit ascii id
      text: message.text,
    );
    _addMessage(textMessage);
  }
}
