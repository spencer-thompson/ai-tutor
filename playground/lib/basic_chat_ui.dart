import 'package:flutter/material.dart';
import 'dart:convert';
import 'dart:math';
import 'package:flutter_chat_types/flutter_chat_types.dart' as types;
import 'package:flutter_chat_ui/flutter_chat_ui.dart';
import 'package:flutter_markdown/flutter_markdown.dart';
import 'package:http/http.dart' as http;

String randomString() {
  final random = Random.secure();
  final values = List<int>.generate(16, (i) => random.nextInt(255));
  return base64UrlEncode(values);
}

class BasicApp extends StatelessWidget {
  const BasicApp({super.key});

  @override
  Widget build(BuildContext context) => const MaterialApp(
        debugShowCheckedModeBanner: false,
        home: MyHomePage(),
      );
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key});

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  final List<types.Message> _messages = [];
  final _user = const types.User(id: '82091008-a484-4a89-ae75-a22bf8d6f3ac');
  final _user2 = const types.User(id: '82091008-a484-4a89-ae75-a22bf8d6f20v');
  double screen_width = 0.0;

  final myCustomTheme = DefaultChatTheme(messageMaxWidth: double.infinity);
  @override
  Widget build(BuildContext context) => Scaffold(
        body: LayoutBuilder(
          builder: (context, constraints) {
            return Chat(
              theme: myCustomTheme,
              messageWidthRatio: 10.0,
              messages: _messages,
              onSendPressed: _handleSendPressed,
              user: _user,
              customMessageBuilder: (message, {required messageWidth}) =>
                  _buildMarkdownMessage(message,
                      messageWidth: messageWidth,
                      maxWidth: constraints.maxWidth),
              bubbleRtlAlignment: BubbleRtlAlignment.left,
              showUserAvatars: true,
              showUserNames: true,
            );
          },
        ),
      );

  Widget _avatarBuilder() {
    return Scaffold();
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
      //text: message.text,
      metadata: {'markdown': message.text},
    );
    _addMessage(currentMessage);

    _sendUserMessage(message.text, currentMessage.id);
  }

  void _sendUserMessage(String userMessage, String messageId) async {
    String response = await _sendToGPT(userMessage, messageId);
    _displayGPTMessage(response);
  }

  Future<String> _sendToGPT(String userMessage, String messageId) async {
    final body = jsonEncode([
      {"role": "user", "content": userMessage, "name": "Guts"}
    ]);

    final headers = {
      "Content-Type": "application/json",
      "AITUTOR-API-KEY": "test_key"
    };

    final response = await http.post(
      Uri.parse("http://localhost:8080/v1/chat"),
      headers: headers,
      body: body,
    );

    return response.body;
  }

  Future<void> _displayGPTMessage(String response) {
    final parsedJson = jsonDecode(response);
    final content = parsedJson['content'];

    final aiMessage = types.CustomMessage(
      author: _user2,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      id: randomString(),
      showStatus: true,
      status: types.Status.sent,
      //text: content,
      metadata: {'markdown': content},
    );

    _addMessage(aiMessage);
    return Future.value();
  }

  Widget _buildMarkdownMessage(types.CustomMessage message,
      {required int messageWidth, required double maxWidth}) {
    final markdownText = message.metadata?['markdown'] as String? ?? '';
    //final Size size = MediaQuery.sizeOf(context);
    //final double width = size.width;
    //final double height = size.height;
    //print("${width * .72}");
    //messageWidth = (messageWidth * 1.5).toInt();
    //print("$messageWidth");

    double bubbleWidth = maxWidth * 0.75;

    if (bubbleWidth > 1000) bubbleWidth = 1000;

    if (bubbleWidth < 200) bubbleWidth = 200;

    return Container(
      constraints: BoxConstraints(
        maxWidth: bubbleWidth,
      ),
      padding: const EdgeInsets.all(10),
      margin: const EdgeInsets.symmetric(vertical: 5),
      child: MarkdownBody(
        data: markdownText,
      ),
    );
  }
}
