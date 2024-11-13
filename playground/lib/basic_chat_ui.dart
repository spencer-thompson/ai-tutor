import 'package:flutter/material.dart';
import 'dart:convert';
import 'dart:math';
import 'dart:core';
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
  final cur_time = DateTime.now().millisecondsSinceEpoch;

  final myCustomTheme = DefaultChatTheme(messageMaxWidth: double.infinity);

  @override
  Widget build(BuildContext context) => Scaffold(
        //LayoutBuilder adjusts width baseed on the current size of the window...
        //this changes the constraints.maxWidth
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
  //
  //void _handleSendPressed(types.PartialText message) async {
  //  final currentMessage = types.CustomMessage(
  //    author: _user,
  //    createdAt: DateTime.now().millisecondsSinceEpoch,
  //    id: randomString(),
  //    showStatus: true,
  //    status: types.Status.sent,
  //    //text: message.text,
  //    metadata: {'markdown': message.text},
  //  );
  //  _addMessage(currentMessage);
  //  print('Made it here');
  //
  //  runner().listen((data) {
  //    print(data.runtimeType);
  //    print('Received data: $data');
  //  });
  //  //await runner();
  //
  //  //_sendToGPT(message.text, currentMessage.id);
  //}
  //

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

    final aiMessage = types.CustomMessage(
      author: _user2,
      createdAt: DateTime.now().millisecondsSinceEpoch,
      //id: randomString(),
      id: '234932',
      showStatus: true,
      status: types.Status.sent,
      metadata: {'markdown': ''},
    );
    _addMessage(aiMessage);

    String accumulatedResponse = '';

    runner().listen((chunk) {
      accumulatedResponse += chunk;
      print(chunk);
      setState(() {
        _messages[0] = (_messages[0] as types.CustomMessage).copyWith(
          metadata: {'markdown': accumulatedResponse},
        );
      });
    });
  }

  Stream<String> runner() async* {
    // Get all messages except the empty AI message we just added
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
      "AITUTOR-API-KEY": "test_key"
    };

    final request = http.Request(
      'POST',
      Uri.parse("http://localhost:8080/v1/chat_stream"),
    );

    request.headers.addAll(headers);
    request.body = data;

    final streamedResponse = await request.send();

    if (streamedResponse.statusCode != 200) {
      throw Exception(
          'Failed to connect to server: ${streamedResponse.statusCode}');
    }

    await for (final chunk in streamedResponse.stream.transform(utf8.decoder)) {
      try {
        // Try to parse as JSON
        final jsonData = jsonDecode(chunk);
        if (jsonData['content'] != null) {
          yield jsonData['content'];
        }
      } catch (e) {
        // If it's not valid JSON, try to extract content from the chunk
        final contentMatch =
            RegExp(r'"content":\s*"([^"]*)"').allMatches(chunk);
        //print(chunk);
        for (final match in contentMatch) {
          print(match.group(1));
          final aiMessage = types.CustomMessage(
            author: _user2,
            createdAt: DateTime.now().millisecondsSinceEpoch,
            id: randomString(),
            showStatus: true,
            status: types.Status.sent,
            metadata: {'markdown': match.group(1)},
          );
          _addMessage(aiMessage);

          yield match.group(1)!;
        }
      }
    }
  }

  //
  //Stream<String> runner() async* {
  //  final messages = _messages.reversed
  //      .map((message) {
  //        if (message is types.CustomMessage) {
  //          return {
  //            "role": message.author.id == _user.id ? "user" : "assistant",
  //            "content": message.metadata?['markdown'] ?? '',
  //            "name": message.author.id == _user.id ? "Guts" : "Assistant"
  //          };
  //        }
  //        return null;
  //      })
  //      .whereType<Map<String, dynamic>>()
  //      .toList();
  //  final data = jsonEncode(messages);
  //  final headers = {
  //    "Content-Type": "application/json",
  //    "AITUTOR-API-KEY": "test_key"
  //  };
  //  final request = http.Request(
  //    'POST',
  //    Uri.parse("http://localhost:8080/v1/chat_stream"),
  //  );
  //
  //  request.headers.addAll(headers);
  //  request.body = data;
  //
  //  final streamedResponse = await request.send();
  //  Stream<String> stream = streamedResponse.stream.transform(utf8.decoder);
  //
  //  await for (final chunk in stream) {
  //    print(chunk);
  //    yield chunk;
  //  }
  //}

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

  Future<void> _displayGPTMessage(String response) {
    final parsedJson = jsonDecode(response);
    final content = parsedJson['content'];

    final aiMessage = types.CustomMessage(
      author: _user2,
      //createdAt: DateTime.now().millisecondsSinceEpoch,
      createdAt: cur_time,
      id: randomString(),
      showStatus: true,
      status: types.Status.sent,
      //text: content,
      metadata: {'markdown': content},
    );
    setState(() {
      _messages.removeAt(0);
    });

    _addMessage(aiMessage);
    return Future.value();
  }
}
//
//  void _handleSendPressed(types.PartialText message) async {
//    final currentMessage = types.CustomMessage(
//      author: _user,
//      createdAt: DateTime.now().millisecondsSinceEpoch,
//      id: randomString(),
//      showStatus: true,
//      status: types.Status.sent,
//      metadata: {'markdown': message.text},
//    );
//    _addMessage(currentMessage);
//
//    final aiMessage = types.CustomMessage(
//      author: _user2,
//      createdAt: DateTime.now().millisecondsSinceEpoch,
//      id: randomString(),
//      showStatus: true,
//      status: types.Status.sending,
//      metadata: {'markdown': ''},
//    );
//    _addMessage(aiMessage);
//
//    String completion = '';
//    await for (final chunk in runner()) {
//      completion += chunk;
//      setState(() {
//        _messages[0] = (_messages[0] as types.CustomMessage).copyWith(
//          metadata: {'markdown': completion},
//          status: types.Status.sent,
//        );
//      });
//    }
//  }
//
//  Stream<String> runner() async* {
//    final messages = _messages.reversed
//        .map((message) {
//          if (message is types.CustomMessage) {
//            return {
//              "role": message.author.id == _user.id ? "user" : "assistant",
//              "content": message.metadata?['markdown'] ?? '',
//              "name": message.author.id == _user.id ? "Guts" : "Assistant"
//            };
//          }
//          return null;
//        })
//        .whereType<Map<String, dynamic>>()
//        .toList();
//    final data = jsonEncode(messages);
//    final headers = {
//      "Content-Type": "application/json",
//      "AITUTOR-API-KEY": "test_key"
//    };
//    final request = http.Request(
//      'POST',
//      Uri.parse("http://localhost:8080/v1/chat_stream"),
//    );
//
//    request.headers.addAll(headers);
//    request.body = data;
//
//    final streamedResponse = await request.send();
//    final stream = streamedResponse.stream.transform(utf8.decoder);
//
//    await for (var chunk in stream) {
//      try {
//        print(chunk);
//        final parsedChunk = jsonDecode(chunk);
//        print(parsedChunk);
//        yield parsedChunk;
//        //if (parsedChunk['content'] != null) {
//        //  yield parsedChunk['content'];
//        //}
//      } catch (e) {
//        yield chunk;
//      }
//    }
//  }
//
//  Future<void> _displayGPTMessage(String response) {
//    final parsedJson = jsonDecode(response);
//    final content = parsedJson['content'];
//
//    final aiMessage = types.CustomMessage(
//      author: _user2,
//      createdAt: DateTime.now().millisecondsSinceEpoch,
//      //id: randomString(),
//      id: "1309854jsladkf",
//      showStatus: true,
//      status: types.Status.sent,
//      //text: content,
//      metadata: {'markdown': content},
//    );
//
//    _addMessage(aiMessage);
//    return Future.value();
//  }
//
//  Widget _buildMarkdownMessage(types.CustomMessage message,
//      {required int messageWidth, required double maxWidth}) {
//    final markdownText = message.metadata?['markdown'] as String? ?? '';
//
//    double bubbleWidth = maxWidth * 0.75;
//
//    if (bubbleWidth > 1000) bubbleWidth = 1000;
//
//    if (bubbleWidth < 200) bubbleWidth = 200;
//
//    return Container(
//      constraints: BoxConstraints(
//        maxWidth: bubbleWidth,
//      ),
//      padding: const EdgeInsets.all(10),
//      margin: const EdgeInsets.symmetric(vertical: 5),
//      // MarkdownBody widget knows how to size the height properly
//      child: MarkdownBody(
//        data: markdownText,
//      ),
//    );
//  }
//}

