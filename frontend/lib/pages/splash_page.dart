import 'package:flutter/material.dart';
import 'package:frontend/pages/chat_page.dart';
import 'package:frontend/utils/constants.dart';

class SplashPage extends StatefulWidget {
  const SplashPage({Key? key})
      : super(key: key); // this is the SplashPage constructor
  // the only field in SplashPage's constuctor is key, which is an optional constant,
  // this means that the only parameter accepted is constant and therefore SplashPage can be
  // instantiated as a constant like so: const SplashPage()

  // const indicates that this is a constant constructor
  //

  @override // we are intentionally overriding a the method createState() from the StatefulWidget class
  SplashPageState createState() =>
      SplashPageState(); // instantiate SplashPageState() which returns a type SplashPageState()
  // this creates a mutable state for this widget
}

class SplashPageState extends State<SplashPage> {
  // this state class is associated with the SplashPage widget
  @override
  void initState() {
    // initState() is the first thing called when the class is instantiated
    super.initState(); // ensure that any inherited intialization is performed
    WidgetsBinding.instance.addPostFrameCallback((_) {
      // add a callback ('a function passed as an arguement')
      // that will be executed after the current frame is rendered.
      // WidgetsBinding.instance provides access to the Flutter engines' event loop and rendering pipeline
      // addPostFrameCallback: Schedules the privded callback to run after the current frame
      _redirect();
      // this calls the redirect method inside the post-frame callback
      // this is a callback because we need to ensure the navigation occurs after the build method has completed
      // and the first frame has rendered
    });
  }

  Future<void> _redirect() async {
    // this is an asynchronous private method that returns a Future<void>
    await Future.delayed(Duration
        .zero); // this will ensure any pending UI updates are processed before
    // performing navigation. It gives the event loop a chance to complete the current operations.

    Navigator.of(context)
        .pushAndRemoveUntil(ChatPage.route(), (route) => false);
  } // navigate to the ChatPage and remove all previous routes
  // We call ChatPage.route() because there is a static method route() in ChatPage that returns a route to the chat page

  @override
  Widget build(BuildContext context) {
    // build method takes in the context (which is passed into the widget when it is
    // instantiated) and this context contains widget tree info and other things
    return const Scaffold(
        body:
            preloader); // returns a Scaffold widget witha body containing 'preloader'
    // the preloader is a constant widget defined in constants.dart
  }
}

// When SplashPage is instantiated the constructor is called which initializes the code inside the constructor
// Because SplashPage is a StatefulWidget, after the constructor is called it then calls the
// createState() method which creates the mutable state for the widget, the StatefulWidget then calles the
// initState() method which initializes the state variables, start animations, and subscribes to streams. It finally calls the
// build() method which is called whenever the widget needs to be rendered
// it might eventually call didChangeDepenedicies(), or dispose() but not always

// SplashPage was instantiated in main.dart when we did: const SplashPage(), we were able to do this because
// all the instance fields were final, and the superclass had a constant constructor

// SplashPage can be instantiated as a constant because all of it's constructor fields are constant, and
// although SplashPage has mutable data this is O.K. because the State is managed seperately from the intantiation in the flutter framework

// the 'key' in const SplashPage({Key? key}) : super(key: key);  is actually a class inside this class are the following:
// key.Valuekey, key.ObjectKey, key.UniqueKey, key.GlobalKey

// When you instantiate a widget without providing a key, the key parameter defaults to null.
// The key is optional because it isn't always necessary to pass in a key, flutter can manage widgets like SplashPage
// efficiently based on their posistion in the widget tree.
// In fact, sometimes it is beneficial for performance reasons to not be passing key objects around.

// const SplashPage({Key? key}) : super(key: key); => this just means if you receive a key as an arguement, make
// sure to pass this key to the key up to the statefulWidget for proper management

// We could do something like this if we wanted to pass a key object to SplashPage -> const SplashPage(key: ValueKey('splash_page'));


// When we make a StatefulWidget, we are actually defining two classes.
// 1) The StatefulWidget subclass (SplashPage)
// this contains the immutable part of the widget that represents the configuration for the widget
// 2) The State subclass (SplashPageState)
// This holds the mutable state for the widget as well as the logic for changing the internal state overtime

// The purpose of SplashPage is to extend the StatefulWidget. It is simply supposed to create an instance of
// its associated State which is done by implementing the createState() method


// In flutter, a frame refers to one cycle of the rendering pipeline where the UI is potentially updated.

