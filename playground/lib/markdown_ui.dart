import 'package:flutter/material.dart';
import 'package:flutter_markdown/flutter_markdown.dart';

class MarkdownUi extends StatelessWidget {
  const MarkdownUi({super.key});

  // This widget is the root of your application.
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Flutter Demo',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.deepPurple),
        useMaterial3: true,
      ),
      home: const MyHomePage(title: 'Flutter Markdown Page'),
    );
  }
}

class MyHomePage extends StatefulWidget {
  const MyHomePage({super.key, required this.title});

  final String title;

  @override
  State<MyHomePage> createState() => _MyHomePageState();
}

class _MyHomePageState extends State<MyHomePage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          backgroundColor: Theme.of(context).colorScheme.inversePrimary,
          title: Text(widget.title),
        ),
        body: Center(
          child: Markdown(
            selectable: true,
            data: """
# Hello, Flutter!

This is a simple markdown message with:

- **Bold** text
- *Italic* text
- [A link](https://flutter.dev)

> Markdown is fun and easy to use!
              """, //styleSheet: MarkdownStyleSheet(
            //  h1: const TextStyle(fontSize: 24, color: Colors.blue),
            //  code: const TextStyle(fontSize: 14, color: Colors.green),
            //),
          ),
        ));
  }
}
