import 'package:flutter/material.dart';
import 'dart:convert';
import 'dart:math';
import 'dart:core';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:http/http.dart' as http;
import 'package:playground/drawer.dart';
import 'package:flutter/services.dart';

String randomString() {
  final random = Random.secure();
  final values = List<int>.generate(16, (i) => random.nextInt(255));
  return base64UrlEncode(values);
}

//
//class BasicApp extends StatelessWidget {
//  const BasicApp({super.key});
//
//  @override
//  Widget build(BuildContext context) => const MaterialApp(
//        debugShowCheckedModeBanner: false,
//        home: MyHomePage(),
//      );
//}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final List<types.Message> _messages = [];
  final _user = const types.User(id: '82091008-a484-4a89-ae75-a22bf8d6f3ac');
  final _user2 = const types.User(
      id: '82091008-a484-4a89-ae75-a22bf8d6f20v',
      firstName: 'Roofus',
      lastName: 'hamburger',
      role: types.Role.user);
  final List<types.User> typingUsers = [];
  bool _isLightMode = true;
  final GlobalKey<ScaffoldState> _scaffoldKey = GlobalKey<ScaffoldState>();

  void _toggleBotTyping() {
    setState(() {
      if (typingUsers.isEmpty) {
        typingUsers.add(_user2);
      } else {
        typingUsers.clear();
      }
    });
  }

  void _toggleTheme() {
    setState(() {
      _isLightMode = !_isLightMode;
    });
  }

  AppBar appBarLight(bool isLightMode, Function toggleTheme) {
    return AppBar(
      leading: IconButton(
        icon: Icon(Icons.accessible,
            color: isLightMode ? Colors.black : Colors.white),
        onPressed: () => _scaffoldKey.currentState?.openDrawer(),
      ),
      backgroundColor: isLightMode ? Colors.white : Colors.black,
      toolbarHeight: 50.0,
      systemOverlayStyle: SystemUiOverlayStyle(
        statusBarColor: isLightMode ? Colors.white : Colors.red,
        statusBarIconBrightness: Brightness.dark,
        statusBarBrightness: Brightness.dark,
        systemNavigationBarColor: isLightMode ? Colors.white : Colors.black,
        systemNavigationBarIconBrightness:
            isLightMode ? Brightness.dark : Brightness.light,
      ),
      actions: [
        IconButton(
          icon: _isLightMode
              ? const Icon(Icons.light_mode, color: Colors.blue)
              : const Icon(Icons.dark_mode, color: Colors.white),
          onPressed: () => toggleTheme(),
        ),
      ],
      title: const Text(
        "Chat",
        style: TextStyle(
          fontStyle: FontStyle.italic,
          fontWeight: FontWeight.bold,
          color: Colors.red,
        ),
      ),
    );
  }

  final chatDarkTheme = const DarkChatTheme(
    backgroundColor: Colors.pink,
    userAvatarNameColors: [Colors.red],
    messageMaxWidth: double.infinity,
    primaryColor: Colors.blue,
    secondaryColor: Colors.cyanAccent,
  );

  final chatLightTheme = const DefaultChatTheme(
    //receivedEmojiMessageTextStyle: TextStyle(fontSize: 1000),
    //receivedMessageBodyTextStyle: TextStyle(color: Colors.indigoAccent),
    //sentMessageCaptionTextStyle: TextStyle(color: Colors.deepOrange, fontWeight: FontWeight.w900),

    typingIndicatorTheme: TypingIndicatorTheme(
        bubbleBorder: BorderRadius.all(Radius.circular(20.0)),
        bubbleColor: Colors.grey,
        animatedCirclesColor: Colors.lime,
        animatedCircleSize: 20.0,
        multipleUserTextStyle: TextStyle(),
        countTextColor: Colors.red,
        countAvatarColor: Colors.black),
    inputSurfaceTintColor: Colors.lime,
    dateDividerTextStyle: TextStyle(
        color: Colors.tealAccent, fontSize: 15, fontWeight: FontWeight.w800),
    emptyChatPlaceholderTextStyle:
        TextStyle(color: Colors.brown, fontSize: 200, height: 100.0),
    backgroundColor: Colors.orange,
    messageMaxWidth: double.infinity,
    inputBackgroundColor: Colors.red,
    inputTextColor: Colors.white,
    inputTextCursorColor: Colors.yellow,
    primaryColor: Colors.blue,
    secondaryColor: Colors.purple,
    userAvatarImageBackgroundColor: Colors.red,
  );

  @override
  Widget build(BuildContext context) => Scaffold(
        key: _scaffoldKey,
        //LayoutBuilder adjusts width baseed on the current size of the window...
        //this changes the constraints.maxWidth
        appBar: appBarLight(_isLightMode, _toggleTheme),
        drawer: SideDrawerLight(_isLightMode, _deleteAllMessages),
        body: LayoutBuilder(
          builder: (context, constraints) {
            return Chat(
              theme: _isLightMode ? chatLightTheme : chatDarkTheme,
              //typingIndicatorOptions: TypingIndicatorOptions(customTypingIndicatorBuilder({required BubbleRtlAlignment}),
              messageWidthRatio: 10.0,
              messages: _messages,
              onSendPressed: _handleSendPressed,
              user: _user,
              customMessageBuilder: (message, {required messageWidth}) =>
                  _buildMarkdownMessage(message,
                      messageWidth: messageWidth,
                      maxWidth: constraints.maxWidth),
              bubbleRtlAlignment: BubbleRtlAlignment.right,
              emptyState: Center(
                  child: Text(
                      "Welcome! I am your AI tutor: type '--help' for avaiable options")),
              showUserAvatars: false,
              showUserNames: true,
              typingIndicatorOptions: TypingIndicatorOptions(
                typingUsers: typingUsers,
                customTypingIndicator: const TypingIndicator(
                  showIndicator: true,
                  bubbleAlignment: BubbleRtlAlignment.right,
                ),
              ),
              onMessageLongPress: (context, message) {
                showModalBottomSheet(
                  context: context,
                  builder: (context) {
                    return Container(
                      padding: const EdgeInsets.all(16.0),
                      child: Column(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Text(
                            'Message Options',
                            style: Theme.of(context).textTheme.headlineMedium,
                          ),
                          const SizedBox(height: 8.0),
                          ListTile(
                            leading: const Icon(Icons.copy),
                            title: const Text('Copy Message'),
                            onTap: () {
                              Navigator.pop(context);
                              Clipboard.setData(ClipboardData(
                                  text: message.metadata?['markdown']));
                            },
                          ),
                        ],
                      ),
                    );
                  },
                );
              },
            );
          },
        ),
      );

  Widget _avatarBuilder() {
    return Scaffold();
  }

  void _deleteAllMessages() {
    setState(() {
      _messages.clear();
    });
  }

  void _addMessage(types.Message message) {
    setState(() {
      _messages.insert(0, message);
    });
  }

  void _handleSendPressed(types.PartialText message) async {
    final currentMessage = types.CustomMessage(
      author: _user,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: randomString(),
      showStatus: true,
      status: types.Status.sent,
      metadata: {'markdown': message.text},
    );
    _addMessage(currentMessage);
    _toggleBotTyping();

    await _sendToGPT(message.text);
  }

  Future<void> _sendToGPT(String userMessage) async {
    final messages = _messages.reversed
        .map((message) {
          if (message is types.CustomMessage) {
            return {
              "role": message.author.id == _user.id ? "user" : "assistant",
              "content": message.metadata?['markdown'] ?? '',
              "name": message.author.id == _user.id ? "Guts" : "Assistant"
            };
          }
          return null;
        })
        .whereType<Map<String, dynamic>>()
        .toList();

    final data = jsonEncode(messages);

    final headers = {
      "Content-Type": "application/json",
      "AITUTOR-API-KEY": "test_key",
      //"Authorization: "$Bearer ${qr_token}"
    };

    final response = await http.post(
      //Uri.parse("http://localhost:8080/v1/chat"),
      Uri.parse("http://localhost:8080/v1/chat"),
      headers: headers,
      body: data,
    );

    _displayGPTMessage(response.body);
  }

  Future<void> _displayGPTMessage(String response) {
    final parsedJson = jsonDecode(utf8.decode(response.runes.toList()));
    final content = parsedJson['content'];

    final aiMessage = types.CustomMessage(
      author: _user2,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: randomString(),
      showStatus: true,
      status: types.Status.sent,
      metadata: {'markdown': content},
    );

    _addMessage(aiMessage);
    _toggleBotTyping();
    return Future.value();
  }

  Widget _buildMarkdownMessage(types.CustomMessage message,
      {required int messageWidth, required double maxWidth}) {
    final markdownText = message.metadata?['markdown'] as String? ?? '';
    double bubbleWidth = maxWidth * 0.75;
    if (bubbleWidth > 1000) bubbleWidth = 1000;
    if (bubbleWidth < 200) bubbleWidth = 200;
    return Container(
      constraints: BoxConstraints(
        maxWidth: bubbleWidth,
      ),
      padding: const EdgeInsets.all(10),
      margin: const EdgeInsets.symmetric(vertical: 5),
      // MarkdownBody widget knows how to size the height properly
      child: MarkdownBody(
        data: markdownText,
      ),
    );
  }
}

// LayoutBuilder --> if you are writing a build method but want to know/specify how big it will be.
