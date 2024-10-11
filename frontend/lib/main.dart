import 'package:flutter/material.dart';
import 'package:frontend/utils/constants.dart';
import 'package:supabase_flutter/supabase_flutter.dart';
import 'package:frontend/pages/splash_page.dart';
import 'package:flutter_dotenv/flutter_dotenv.dart';

// A Future<void> Means that the function will be performed asynchronously ('Future')
// the 'void' means that nothing will be returned by the function
// every widget has a 'key' to identify it, which is why we do super(key: key)
// every widget in flutter gets a BuildContext as an arguement to the build method
// The BuildContext helps flutter know what do to with the widget inside the widget tree
// The BuildContext tells the widget about the app's configuration, theme data, and localization
// App configuration refers to things like the platform the app is running on the screen size, orientation and such forth
// The Theme Data for the app is defined globally and widgets can access the theme using the 'context' parameter
// You can do so by doing something like Theme.of(context).textTheme
// Localization refers to adapting the app to different languages, regions, or cultures.
// So BuildContext uses these properties received through the context object
// ALMOST ALL user-created widgets extend either statelesswidget or statefulWidget

// An App's 'layout' or where the widget appears on the screen can be determined by Widgets like:
// Column{} Row{} or Stack{}

// When a widget is first created, flutter callss the build() method to construct the visual representation,
// and the build method returns a widget tree (the widget tree is then rendered on the screen)

// a StatelessWidget doesn't need to be rebuilt unless its parent changes.
// a StatefulWidget can trigger rebuilds when an internal state changes.
// flutter triggers the build method again to refresh the UI based on the new state with something like this:
// SetState(() { counter++; }); -- Every time the SetState() is called the widget is rebuilt
// A StatefulWidget is linked to a 'State' object
// A State object manages mutable data and can trigger rebuilds when the data changes.

// StatefulWidgets have lifecycles that follow these steps (and more):
// initState() this is called once when the widget is inserted into the widget tree
// dispose() is called when the widget is removed from the tree, this is used to clean up recources and close streams
// didUpdateWidget() is called when the parent widget changes and the state needs to be updated.

// For a StatefulWidget initState() is called first (before the build method)

// The Painting process referes to how UI elements are rendered on the screen
// Widgets are immutable descriptions (part of the UI)
// Elements are instances of widgets that flutter manages.

Future<void> main() async {
  // this will return something of type Future<void>
  WidgetsFlutterBinding
      .ensureInitialized(); // Before we start make sure the widgets have been initialized

  await dotenv.load(
      fileName:
          "secrets.env"); // load in the dotenv file with our environment variables

  String? supabase_url = dotenv.env['SUPABASE_URL'];
  String? anon_key = dotenv.env['SUPABASE_ANON_KEY'];

  if (supabase_url != null && anon_key != null) {
    await Supabase.initialize(
      // initialized connection with supabase
      url: supabase_url,
      anonKey: anon_key,
    );
  }
  runApp(
      const MyApp()); // Alright, not I want you to run the app called 'MyApp'
}

class MyApp extends StatelessWidget {
  // We've got a class that will not contain anything that changes
  const MyApp({Key? key})
      : super(key: key); // inherit everything from the stateless widget class

  @override // stateless widget already has a build widget defined, so we need to overrid this method
  Widget build(BuildContext context) {
    // We are returning a type 'Widget'
    // build is the name of the method
    // BuildContext is a class, this contains info about where our widget falls in the widget tree
    // BuildContext also can access things like appConfiguration, theme data, and localization
    // the 'context' object is passed by flutter when the widget is built
    return MaterialApp(
      // this is the root of the application
      debugShowCheckedModeBanner: false,
      title:
          'My Chat App', // this is the title that appears on the tab of the application
      theme:
          appTheme, // kind of acts like the default external stylesheet (like CSS but for flutter)
      home:
          const SplashPage(), // home is the default route of where the application will go
      // by calling an instance of SplashPage() we call
    );
  }
}


//Widgets are just blueprints (as are classes) of what flutter will be told to render on the screen
//Because Widgets are just classes, this means they do not have a mutable state (they aren't instances)

//Elements are the instances of widgets. An element represents a specific location in the widget tree
// and holds the mutable state associated with the widget.

// RenderObjects calculate the size and position of widgets, are responsible for making the objects appear on screen,
// and they actually manage the rendering (and rerendering pipeline)

// Build methods can return any widget. The Widgets that they commonly return are:
// => MaterialApp -> this is often returned by the root widget of the application (usually only used once)
// => CupertinoApp -> this is for apps taht user Cupertino (iOS-style) design elements.
// => Scaffold -> this provides a structure fo material design layouts that utilize widgets like: app bar, body, & floating action button
// => Container/Colummn/Row/ListView -> These are all used for layout and positioning of child widgets
// => Custom Widgets => Whatever else you may have defined in the code. Could be something like SplashPage()

// the theme references appTheme, and appTheme is a ThemeData object, appTheme is like the CSS for flutter
// by putting the theme in the MaterialApp (root application) we are making the appTheme data globally accessible
// a 'Theme' widget can be declared later and its child/children widgets will inherit the most recent definitions of the theme
// ThemeData can also be used instead of Theme(data: )




// Scaffold does not have any required Arguements, all parameters are optional. Some commonly used parameters are:
// appBar > this will accept any widget that implements the PreferredSizeWidget interface, not just the AppBar widget
// -> however AppBar is the most commonly used Widget that is used as an arguement for appBar
// body > 
// floatingActionButton >
// drawer > a Panel that slides in from the side
// bottomNavigationBar: This is a widget that is displayed at the bottom of the widget
// backgroundColor: This is the color of the Scaffold's background
// resizeToAvoidBottomInset: This controls whether the body should resize when the keyboard appears

// Scaffold lets you provide functionality like displaying snack bars, bottom sheets, and dialogs using its ScaffoldState
//

// Maybe defining multiple themes like 'dark mode', 'classic', and custom to the customer would be a good idea.
